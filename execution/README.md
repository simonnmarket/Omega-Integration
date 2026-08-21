# Execution

This is the only allowed boundary for broker-side execution.

Planned components:

- `ports/`: broker-neutral execution interfaces;
- `fake/`: deterministic test broker;
- `mt5/`: isolated MT5 adapter, disabled by default;
- `reconciliation/`: order, deal, position and exit lifecycle;
- `risk_gate/`: final authority before an order request.

No strategy or engine may call a broker API directly. Every request must carry an idempotency key and be reconciled by broker evidence.
