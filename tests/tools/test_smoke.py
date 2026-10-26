import importlib.util
from pathlib import Path

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

SPEC = importlib.util.spec_from_file_location(
    "smoke", Path(__file__).resolve().parents[2] / "tools" / "coinbase_smoke_test.py"
)
smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke)


@pytest.fixture(scope="module")
def keypair():
    priv = ec.generate_private_key(ec.SECP256R1())
    pem = priv.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    ).decode()
    pub = priv.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem, pub


def test_jwt_claims_with_and_without_uri(keypair):
    pem, pub = keypair
    tok = smoke.build_jwt("organizations/o/apiKeys/k", pem, "POST drb.coinbase.com/api/v2", now=1000)
    claims = jwt.decode(tok, pub, algorithms=["ES256"], options={"verify_exp": False, "verify_nbf": False})
    assert claims["iss"] == "cdp" and claims["sub"] == "organizations/o/apiKeys/k"
    assert claims["exp"] - claims["nbf"] == 120
    assert claims["uri"] == "POST drb.coinbase.com/api/v2"
    hdr = jwt.get_unverified_header(tok)
    assert hdr["kid"] == "organizations/o/apiKeys/k" and hdr["nonce"]
    no_uri = jwt.decode(smoke.build_jwt("n", pem, None, now=1000), pub, algorithms=["ES256"],
                        options={"verify_exp": False, "verify_nbf": False})
    assert "uri" not in no_uri


def test_round_to_tick():
    assert smoke.round_to_tick(81709.37, 0.5) == 81709.0
    assert smoke.round_to_tick(81709.37, 0.5, up=True) == 81709.5


SPEC_OK = {"instrument_name": "BTC_USDC-PERPETUAL", "min_trade_amount": 0.0001, "tick_size": 0.5}
TICKER = {"best_bid_price": 80000.0, "best_ask_price": 80001.0}


def test_plan_order_is_far_post_only_min_size():
    p = smoke.plan_order(SPEC_OK, TICKER, 3.0, 15.0)
    assert p["post_only"] is True and p["type"] == "limit"
    assert p["amount"] == 0.0001
    assert p["price"] <= 80000.0 * 0.97 + 0.5


def test_plan_order_refuses_big_notional_and_missing_data():
    with pytest.raises(smoke.GatewayError):
        smoke.plan_order({**SPEC_OK, "min_trade_amount": 1.0}, TICKER, 3.0, 15.0)
    with pytest.raises(smoke.GatewayError):
        smoke.plan_order({"tick_size": 0.5}, TICKER, 3.0, 15.0)
    with pytest.raises(smoke.GatewayError):
        smoke.plan_order(SPEC_OK, {}, 3.0, 15.0)


class FakeResp:
    status_code = 200

    def __init__(self, body):
        self._b = body

    def json(self):
        return self._b


class FakeSession:
    """Simulates the gateway; records every method called."""

    def __init__(self, fail_verify=False, reject_uri=False):
        self.calls, self.fail_verify, self.reject_uri = [], fail_verify, reject_uri

    def post(self, url, json=None, headers=None, timeout=None):
        m, p = json["method"], json["params"]
        self.calls.append((m, p, headers.get("Authorization")))
        r = lambda x: FakeResp({"jsonrpc": "2.0", "id": json["id"], "result": x})
        err = lambda msg: FakeResp({"jsonrpc": "2.0", "id": json["id"], "error": {"message": msg}})
        if m == "public/get_instrument":
            return r(SPEC_OK | {"kind": "future"})
        if m == "public/ticker":
            return r(TICKER | {"mark_price": 80000.5})
        if m == "public/auth":
            claims = jwt.decode(p["token"], options={"verify_signature": False})
            if self.reject_uri and "uri" in claims:
                return err("bad uri")
            return r({"access_token": "tok"})
        if m == "private/get_account_summary":
            return r({"equity": 10.0, "available_funds": 10.0})
        if m == "private/get_positions":
            return r([])
        if m == "private/buy":
            return r({"order": {"order_id": "o1", "order_state": "open"}})
        if m == "private/get_order_state":
            if self.fail_verify:
                return err("boom")
            return r({"order_state": "open"})
        if m == "private/cancel":
            return r({"order_id": "o1", "order_state": "cancelled"})
        raise AssertionError(m)


def methods(session):
    return [c[0] for c in session.calls]


def test_without_execute_no_order_is_ever_placed(keypair):
    s = FakeSession()
    rep = smoke.run(smoke.Gateway(s), ("n", keypair[0]), execute=False, offset_pct=3, max_notional=15)
    assert "private/buy" not in methods(s)
    assert rep["stages"]["1_auth_readonly"]["ok"]


def test_full_lifecycle_places_verifies_and_cancels(keypair):
    s = FakeSession()
    rep = smoke.run(smoke.Gateway(s), ("n", keypair[0]), execute=True, offset_pct=3, max_notional=15)
    st = rep["stages"]["2_order_lifecycle"]
    assert (st["placed_state"], st["verified_state"], st["cancel_state"]) == ("open", "open", "cancelled")
    assert methods(s).count("private/cancel") == 1
    bearer = [c[2] for c in s.calls if c[0].startswith("private/")]
    assert all(b == "Bearer tok" for b in bearer)


def test_order_is_cancelled_even_if_verification_fails(keypair):
    s = FakeSession(fail_verify=True)
    with pytest.raises(smoke.GatewayError):
        smoke.run(smoke.Gateway(s), ("n", keypair[0]), execute=True, offset_pct=3, max_notional=15)
    assert "private/cancel" in methods(s)


def test_auth_falls_back_to_no_uri_variant(keypair):
    s = FakeSession(reject_uri=True)
    gw = smoke.Gateway(s)
    assert gw.authenticate("n", keypair[0]) == "no uri claim"


def test_execute_refused_without_confirmation(monkeypatch, tmp_path, capsys):
    monkeypatch.delenv("LIVE_TRADING_CONFIRM", raising=False)
    assert smoke.main(["--execute", "--key-file", "x.json", "--report-dir", str(tmp_path)]) == 2
    assert "Refusing" in capsys.readouterr().out


def test_private_call_without_token_is_refused():
    with pytest.raises(smoke.GatewayError):
        smoke.Gateway(FakeSession()).rpc("private/buy", {})


def test_load_key_accepts_cdp_json_and_rejects_bad_files(tmp_path, keypair):
    import json as _json

    good = tmp_path / "k.json"
    good.write_text(_json.dumps({"name": "organizations/o/apiKeys/k", "privateKey": keypair[0]}))
    assert smoke.load_key(good) == ("organizations/o/apiKeys/k", keypair[0])

    bad_fields = tmp_path / "a.json"
    bad_fields.write_text(_json.dumps({"id": "x", "privateKey": "abc"}))
    with pytest.raises(smoke.GatewayError, match="name"):
        smoke.load_key(bad_fields)

    ed = tmp_path / "e.json"
    ed.write_text(_json.dumps({"name": "n", "privateKey": "c29tZWJhc2U2NA=="}))
    with pytest.raises(smoke.GatewayError, match="ECDSA"):
        smoke.load_key(ed)

    with pytest.raises(smoke.GatewayError, match="cannot read"):
        smoke.load_key(tmp_path / "missing.json")


def test_main_refuses_unreadable_key_file(tmp_path, capsys):
    assert smoke.main(["--key-file", str(tmp_path / "nope.json"), "--report-dir", str(tmp_path)]) == 2
    assert "Refusing" in capsys.readouterr().out
