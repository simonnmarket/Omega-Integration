# Candidate Ecosystem Matrix

Status: INITIAL STATIC TRIAGE - no economic claim and no broker execution.

| Candidate | Material inventory | Strongest candidate value | Main contamination or risk | Initial decision |
|---|---:|---|---|---|
| Theodora 13092025 BAB | 27,489 files / 1.77 GB including `.venv` | Python research/backend plus MQL5 EA and risk/analysis modules | `.venv`, backups and several direct MT5/order paths; multiple traders | ADAPT, exclude vendor and backups |
| Samsung Global Market 301125 | 16,564 files / 611 MB including `venv` | Numeia tactical EA, data providers, backtesting and orchestration patterns | many Python MT5 executors and direct `order_send`; duplicate backups | ADAPT, isolate execution |
| Prometheus Trading System | 15,944 files / 14.14 GB including dependencies/backups | Prometheus bridge, QuantumCore and multi-version EA candidates | very large duplicate/version tree and multiple execution paths | REDUCE, select one clean lineage |
| Projeto Aurora | 3,237 files / 39.05 MB | Python architecture, manifests and research modules | nested repeated backups; several MT5 executors | ADAPT, use architecture/research only first |
| Program Surveyor | 134 files / 1.19 MB | Apollo11/Quantum, market analysis, risk and scanner modules | direct `CTrade` and `OrderSend` in several EAs | ADAPT, strong analysis candidate |
| Genesis Trading System | 288 files / 7.08 MB | Genesis EA, Alglib/math and QuantumScan components | direct execution in EA and backend connectors | ADAPT, mathematics/research first |
| AURORA-Trading-System | 1,484 files / 12.99 MB | consolidated Aurora Python architecture and connectors | overlaps Projeto Aurora; direct MT5 connectors | DEDUPLICATE, compare against Projeto Aurora |

## Confirmed execution findings

- Theodora contains `Experts\\TheodoraEA.mq5` with `CTrade` Buy/Sell/PositionClose and Python `mt5.order_send` paths.
- Samsung contains `Experts\\Numeia_v6_0_Tactical_EA.mq5` and Python MT5 executors with `order_send`.
- Prometheus contains several `CTrade` EAs and `Prometheus_QuantumCore.mqh` with Buy/Sell/PositionClose.
- Program Surveyor contains Apollo11, Skyler and EURUSD EAs with `CTrade` and/or `OrderSend`.
- Genesis contains `Genesis_EA.mq5`, `QuantumScanGodmode.mqh` and Python MT5 connectors.
- Projeto Aurora and AURORA-Trading-System contain multiple Python MT5 executors.

These findings identify integration boundaries only. They do not prove that any component has edge or profit.

## Integration policy

1. Exclude `.venv`, `venv`, `__pycache__`, generated binaries and backup trees from candidate source manifests.
2. Select one canonical revision per candidate before copying any source.
3. Extract analysis, features, signal, veto, risk, execution and metrics separately.
4. Route all execution through `Omega-Integration/execution/`.
5. Compare candidates on the same data, costs, slippage, risk and reconciliation rules.
6. Preserve rejected and pending components in the matrix; do not silently discard them.
