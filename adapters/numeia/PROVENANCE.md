# Numeia 250625 Adapter Provenance

Status: `PENDING_ADAPTER_IMPLEMENTATION`

## Source snapshot

- Source: `C:\Users\Lenovo\Documents\Codex\2026-06-27\vo\Numeia-250625-working`
- Files: 104
- Bytes: 845421
- Original source folders remain untouched.

## Key files and hashes

| File | Bytes | SHA256 |
|---|---:|---|
| `Expert\NumeiaEA.mq5` | 17860 | `06C39F9EB67146689CF9ABEE7DABB975F9EA76652C55C9D9984FAFA1EF64D40F` |
| `Agents\TradingAgent.mqh` | 8126 | `0E14D756F45F32073D77EF92B2B94F183F9D29A6FAD2A67C96FC818AE0B78D96` |
| `Core\CoreBrainManager.mqh` | 6046 | `D0E572AEC60493AB07A75BBB2EA53CD2E60F4516FB6907690F8FDA2D43C28D91` |
| `Core\ExecutionOrchestrator.mqh` | 1976 | `C4BA0A75EA87BF270B3822092406BA37AD79B639D78DE97F6B7007EBF6171E1F` |
| `Include\ExecutionLogic\TradeExecutor.mqh` | 1025 | `7A1EEAF137DAE72024172059FFC3EA6FB8C670281FCF5218CBFB4F8CE16D1E16` |
| `Include\ExecutionLogic\PositionManager.mqh` | 3975 | `FF93AC3BAC886014EC9BFC94E548DA0CFA7DABB957A32E0B7927E37AFB6357BE` |
| `Include\DecisionEngine\SignalConsensusEngine.mqh` | 2686 | `8763D88A7DA230C5F5001ED9521B4033D6842D10908B2CF1A4C03AB681253BAE` |
| `Include\Analysis\MarketAnalyzer.mqh` | 3151 | `1C999A0AE9A6EAD654E2CFB32FD26DF96F460987309F96E87F88F09F0CEC7A25` |

## Scan result

- 18 broker-call matches across the source tree;
- 117 placeholder or permissive-return matches;
- direct broker paths exist in `Expert\NumeiaEA.mq5`, `Agents\TradingAgent.mqh`, `PositionManager.mqh`, `DefenseOrchestrator.mqh` and `TradeExecutorSkyIntel.mqh`;
- `Include\ExecutionLogic\TradeExecutor.mqh` contains placeholder behavior and cannot be treated as a real executor;
- `Core\ExecutionOrchestrator.mqh` is not evidence of a complete execution pipeline.

## Integration decision

Reuse candidates: analysis, signal consensus, configuration and selected risk logic, subject to contract tests.

Isolate for review: all broker calls, position management, defense orchestration and SkyIntel transport.

Reject as evidence: source comments claiming that tests or errors are complete, placeholder return values and any result not tied to reconciled broker history.

The adapter must expose only OMEGA contracts. It must not expose a second order path.
