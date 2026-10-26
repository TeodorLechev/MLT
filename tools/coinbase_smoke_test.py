#!/usr/bin/env python3
"""Coinbase Global Derivatives gateway smoke test (ADR 0002, check V3).

Answers ONE technical question: can this API key authenticate to the Deribit-powered
gateway and run an order lifecycle (place -> verify -> cancel) on BTC_USDC-PERPETUAL?
It does NOT prove that trading is permitted for the account holder (see ADR 0002, V1-V2).

Stages (each adds risk, nothing happens unless asked):
  0  public, no key      reachability, instrument spec, ticker
  1  auth, read-only     public/auth, account summary, positions
  2  --execute           ONE far-from-market, post-only, minimum-size limit order, then cancel

Safety:
  * Stage 2 needs --execute AND LIVE_TRADING_CONFIRM=YES_I_UNDERSTAND (same phrase as mlt.config).
  * No market orders. No leverage change. The order is cancelled in a `finally` block.
  * Notional is capped (--max-notional); the minimum size comes from the exchange, never guessed.
  * The key file must live OUTSIDE the repository. Secrets are never printed or saved.

Gateway facts used (Coinbase developer docs, see docs/evidence E36):
  JSON-RPC 2.0 over HTTP at https://drb.coinbase.com/api/v2; public/auth with
  grant_type "coinbase_cdp" and a CDP JWT (ES256, ~120 s) returns an access token that is
  sent as "Authorization: Bearer <token>" on private methods.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import secrets
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import jwt
import requests

GATEWAY = "https://drb.coinbase.com/api/v2"
HOST_PATH = "drb.coinbase.com/api/v2"
INSTRUMENT = "BTC_USDC-PERPETUAL"
LIVE_PHRASE = "YES_I_UNDERSTAND"


class GatewayError(RuntimeError):
    pass


# ------------------------------------------------------------------ credentials / JWT
def load_key(path: str | Path) -> tuple[str, str]:
    """CDP key file: {"name": "organizations/.../apiKeys/...", "privateKey": "-----BEGIN..."}.

    Raises GatewayError with a clear message (never echoing key material) on a bad file.
    """
    try:
        data = json.loads(Path(path).expanduser().read_text())
    except (OSError, ValueError) as exc:
        raise GatewayError(f"cannot read key file {path}: {type(exc).__name__}") from None
    name, pem = data.get("name"), data.get("privateKey")
    if not name or not pem:
        raise GatewayError("key file must contain 'name' and 'privateKey' (CDP secret API key)")
    if "BEGIN" not in pem:
        raise GatewayError(
            "privateKey is not a PEM EC key; the docs require an ECDSA (ES256) key, not Ed25519"
        )
    return name, pem


def build_jwt(name: str, pem: str, uri: str | None = None, now: int | None = None) -> str:
    """CDP JWT: ES256, kid = key name, random nonce, valid 120 s; `uri` claim only if given."""
    now = int(time.time()) if now is None else now
    payload = {"sub": name, "iss": "cdp", "nbf": now, "exp": now + 120}
    if uri:
        payload["uri"] = uri
    return jwt.encode(
        payload, pem, algorithm="ES256", headers={"kid": name, "nonce": secrets.token_hex()}
    )


# ------------------------------------------------------------------ JSON-RPC client
class Gateway:
    def __init__(self, session: requests.Session | None = None, url: str = GATEWAY) -> None:
        self.session = session or requests.Session()
        self.url = url
        self.token: str | None = None
        self._id = 0

    def rpc(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        body = {"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}}
        headers = {"Content-Type": "application/json"}
        if method.startswith("private/"):
            if not self.token:
                raise GatewayError("not authenticated")
            headers["Authorization"] = f"Bearer {self.token}"
        resp = self.session.post(self.url, json=body, headers=headers, timeout=30)
        try:
            data = resp.json()
        except ValueError:
            raise GatewayError(f"{method}: HTTP {resp.status_code}, non-JSON body") from None
        if "error" in data:
            raise GatewayError(f"{method}: {data['error']}")
        if resp.status_code != 200:
            raise GatewayError(f"{method}: HTTP {resp.status_code}")
        return data["result"]

    def authenticate(self, name: str, pem: str) -> str:
        """Try the documented flow. The JWT `uri` claim for this host is not documented, so the
        two plausible variants are tried in order; the one that works is returned."""
        variants = {"uri=POST host/path": f"POST {HOST_PATH}", "no uri claim": None}
        errors = []
        for label, uri in variants.items():
            token = build_jwt(name, pem, uri)
            try:
                result = self.rpc(
                    "public/auth", {"grant_type": "coinbase_cdp", "token": token}
                )
            except GatewayError as exc:
                errors.append(f"{label}: {exc}")
                continue
            self.token = result["access_token"]
            return label
        raise GatewayError("authentication failed: " + " | ".join(errors))


# ------------------------------------------------------------------ pure logic (tested)
def round_to_tick(price: float, tick: float, up: bool = False) -> float:
    steps = price / tick
    n = math.ceil(steps - 1e-9) if up else math.floor(steps + 1e-9)
    return round(n * tick, 10)


def plan_order(spec: dict, ticker: dict, offset_pct: float, max_notional: float) -> dict:
    """Minimum-size, post-only BUY limit order `offset_pct` % below the best bid."""
    for key in ("min_trade_amount", "tick_size"):
        if not spec.get(key):
            raise GatewayError(f"instrument spec has no '{key}': refusing to guess")
    bid = ticker.get("best_bid_price")
    if not bid:
        raise GatewayError("ticker has no best_bid_price: refusing to guess a price")
    price = round_to_tick(bid * (1 - offset_pct / 100), spec["tick_size"])
    amount = spec["min_trade_amount"]
    notional = amount * price
    if notional > max_notional:
        raise GatewayError(
            f"notional {notional:.2f} USDC exceeds --max-notional {max_notional:.2f}"
        )
    return {
        "instrument_name": spec.get("instrument_name", INSTRUMENT),
        "amount": amount,
        "type": "limit",
        "price": price,
        "post_only": True,
        "label": "mlt-smoke",
    }


# ------------------------------------------------------------------ the experiment
def run(gw: Gateway, key: tuple[str, str] | None, execute: bool, offset_pct: float,
        max_notional: float, instrument: str = INSTRUMENT) -> dict:
    report: dict = {"time": datetime.now(timezone.utc).isoformat(), "instrument": instrument,
                    "stages": {}}

    def stage(name: str, fn):
        try:
            report["stages"][name] = {"ok": True, **(fn() or {})}
        except GatewayError as exc:
            report["stages"][name] = {"ok": False, "error": str(exc)}
            raise

    # stage 0: public
    ctx: dict = {}

    def s0():
        ctx["spec"] = gw.rpc("public/get_instrument", {"instrument_name": instrument})
        ctx["ticker"] = gw.rpc("public/ticker", {"instrument_name": instrument})
        keys = ["instrument_name", "kind", "settlement_period", "quote_currency", "contract_size",
                "tick_size", "min_trade_amount", "max_leverage", "maker_commission",
                "taker_commission"]
        return {"spec": {k: ctx["spec"].get(k) for k in keys},
                "ticker": {k: ctx["ticker"].get(k) for k in
                           ("best_bid_price", "best_ask_price", "mark_price", "index_price")}}

    stage("0_public", s0)
    if key is None:
        return report

    # stage 1: auth + read-only
    def s1():
        variant = gw.authenticate(*key)
        summary = gw.rpc("private/get_account_summary", {"currency": "USDC"})
        positions = gw.rpc("private/get_positions", {"currency": "USDC", "kind": "future"})
        print(f"  account (console only): equity={summary.get('equity')} "
              f"available_funds={summary.get('available_funds')}")
        return {"auth_variant": variant, "open_positions": len(positions or [])}

    stage("1_auth_readonly", s1)
    if not execute:
        return report

    # stage 2: one resting order, then cancel
    def s2():
        params = plan_order(ctx["spec"], ctx["ticker"], offset_pct, max_notional)
        out = {"planned": {k: params[k] for k in ("amount", "price")}}
        order_id = None
        try:
            placed = gw.rpc("private/buy", params)
            order = placed.get("order", placed)
            order_id = order.get("order_id")
            out["placed_state"] = order.get("order_state")
            state = gw.rpc("private/get_order_state", {"order_id": order_id})
            out["verified_state"] = state.get("order_state")
        finally:
            if order_id:
                cancelled = gw.rpc("private/cancel", {"order_id": order_id})
                out["cancel_state"] = (cancelled.get("order") or cancelled).get("order_state")
        return out

    stage("2_order_lifecycle", s2)
    return report


def main(argv: list[str] | None = None, gateway: Gateway | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--key-file", help="CDP key JSON (outside the repo). Omit for stage 0 only.")
    ap.add_argument("--execute", action="store_true", help="stage 2: place and cancel ONE order")
    ap.add_argument("--offset-pct", type=float, default=3.0, help="how far below best bid")
    ap.add_argument("--max-notional", type=float, default=15.0, help="USDC cap for the order")
    ap.add_argument("--report-dir", default="logs")
    a = ap.parse_args(argv)

    if a.execute and os.environ.get("LIVE_TRADING_CONFIRM") != LIVE_PHRASE:
        print(f"Refusing: --execute needs LIVE_TRADING_CONFIRM={LIVE_PHRASE} in the environment.")
        return 2
    if a.execute and not a.key_file:
        print("Refusing: --execute needs --key-file.")
        return 2
    try:
        key = load_key(a.key_file) if a.key_file else None
    except GatewayError as exc:
        print(f"Refusing: {exc}")
        return 2
    gw = gateway or Gateway()
    try:
        report = run(gw, key, a.execute, a.offset_pct, a.max_notional)
        code = 0
    except GatewayError as exc:
        print(f"STOPPED: {exc}")
        code = 1
        report = {"stopped": str(exc)}
    out_dir = Path(a.report_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"smoke_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.json"
    path.write_text(json.dumps(report, indent=2, default=str))
    print(json.dumps(report, indent=2, default=str))
    print(f"report (no secrets, no balances): {path}")
    return code


if __name__ == "__main__":
    sys.exit(main())
