# Decision log

Every non-trivial choice is recorded here with the experiment that supports it.
Status: `proposed` (hypothesis, untested) -> `accepted` (tested, evidence linked) or `rejected`.
Nothing is `accepted` without a notebook/test link.

## Index

<!-- BEGIN:auto:index -->
| ID | Decision | Status | Evidence |
|---|---|---|---|
| [0001](0001-model-stack.md) | Model stack (NumPy core vs PyTorch) | proposed | – |
| [0002](0002-execution-venue.md) | Execution venue | proposed | [docs/evidence/venue-availability-2026-10-23.md](../../docs/evidence/venue-availability-2026-10-23.md) |
| [0003](0003-instrument-and-data-source.md) | Traded instrument and research data source | proposed | [docs/evidence/venue-availability-2026-10-23.md](../../docs/evidence/venue-availability-2026-10-23.md) |
| [0004](0004-evaluation-protocol.md) | Evaluation protocol: fixed data window and time split | accepted | [tests/test_protocol.py](../../tests/test_protocol.py) |
| [0005](0005-data-handling.md) | Data handling: zero-volume candles and missing funding | accepted | [tests/data/test_schema.py](../../tests/data/test_schema.py) |
<!-- END:auto:index -->
