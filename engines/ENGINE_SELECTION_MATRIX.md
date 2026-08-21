# Engine Selection Matrix

This is a working registry, not a performance certification.

| Candidate | Reported value | Current evidence status | Integration decision |
|---|---|---|---|
| Numeia 250625 | Positive observations on some assets | Source available; exact attribution and reproducibility pending | First candidate adapter |
| Artemis | Additional strategy/component source | Source identified; performance evidence pending | Candidate adapter |
| Quantum | Feature/indicator source | Source identified; performance evidence pending | Candidate adapter |
| Samsung Global Market | Signal transport and execution pattern | Source identified; operational review pending | Candidate adapter |
| Aurora Trading System | Repository-derived architecture/components | Repository identified; complete audit pending | Candidate adapter |

## Selection criteria

Each candidate is compared under the same data, cost, slippage, risk and reconciliation contracts. Signal count, order acceptance or an isolated historical PnL observation is insufficient for promotion.

## Decision vocabulary

- `RETAIN_COMPONENT`: passes contract and improves the common evaluation.
- `COMBINE_COMPONENT`: complementary behavior is demonstrated without duplicate decisions.
- `ISOLATE`: useful but asset- or regime-specific behavior must not enter the shared path.
- `REJECT`: fails contract, evidence or economic comparison.
- `PENDING_EVIDENCE`: not enough material data to decide.
