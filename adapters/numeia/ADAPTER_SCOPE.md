# Numeia Adapter Scope

## Mapping

| OMEGA boundary | Numeia candidate | Initial action |
|---|---|---|
| Market data | `Core\types.mqh`, analysis modules | map to `market_data.schema.json` |
| Features | `Include\Analysis\*`, `Agents\MarketAnalysisAgent.mqh` | isolate and fixture-test |
| Signal | `Include\DecisionEngine\SignalConsensusEngine.mqh`, `DecisionRouter.mqh` | map to `signal.schema.json` |
| Risk | `Agents\RiskAgent.mqh`, `Config\RiskConfig.mqh` | review for permissive defaults |
| Execution | `Expert\NumeiaEA.mq5`, `PositionManager.mqh`, `TradingAgent.mqh` | do not import; replace with OMEGA execution port |
| Reconciliation | no complete canonical adapter identified | implement in OMEGA |
| Metrics | `Auditor\*`, scripts | treat as diagnostic until evidence is reconciled |

## Acceptance gates

1. Contract conversion test passes for valid, stale and malformed data.
2. Signal replay reproduces the original decision without broker side effects.
3. Risk denial is observable and not converted to approval.
4. Fake execution proves order, deal, position and exit reconciliation.
5. Historical positive result is reproduced with matching data, costs and configuration.

Until all five gates pass, this adapter remains a research candidate and cannot be the canonical engine.
