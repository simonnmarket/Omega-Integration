# High-Frequency Code Discovery

Status: PRIORITY LEAD - execution history not yet reconciled.

## Strongest local lead

Source directory: `E:\Theodora 13092025 BAB`

Evidence file: `E:\Theodora 13092025 BAB\trading_debug.log`

Observed material facts:

- 13,880 log lines;
- window: 2025-09-09 22:08:00 to 2025-09-10 00:10:58;
- 4,402 order/trade-related log lines;
- 2,624 error-related lines;
- 1,076 scan cycles explicitly reporting `Trades: 0`;
- repeated `retcode=10016, comment=Invalid stops`;
- repeated `MetaTrader5.position_select` attribute errors;
- the scan loop reports a five-second interval.

This is the strongest explanation found so far for the memory of very high order activity. It proves a high-frequency attempt loop, not a high-frequency fill loop. The log currently supports repeated rejected attempts and zero reported trades, not thousands of completed orders or profit.

## Other high-frequency candidates

| Candidate | Relevant lead | Current interpretation |
|---|---|---|
| Samsung Global Market | `ForexCrossCurrencyArbitrageStrategy_Scientific.py`, `CryptoTriangularArbitrageStrategy_Scientific.py`, `HybridPlan\parallel_executor.py` | frequent opportunity scanning and queued execution; direct MT5 paths require isolation |
| AURORA-Trading-System | `AURORA_v6.0_MVP` rate limits, message bus and execution engine | scalable architecture pattern; not evidence of completed high-frequency trading |
| Program Surveyor | Apollo11, Skyler, EURUSD and physics scanners | multiple signal/execution candidates; direct `OrderSend` paths |
| Prometheus | multiple EA versions and `Prometheus_QuantumCore.mqh` | many duplicated lineages; canonical revision still unknown |
| Theodora | `Backend\app.py`, `Experts\TheodoraEA.mq5`, DeepSeek bridges | strongest local evidence of repeated order attempts, but logs show failures |

## Required reconstruction path

1. Preserve the original logs and source hashes.
2. Identify the exact producer of each `order_send` or `CTrade` attempt.
3. Separate signal count, intent count, request count, accepted order count, deal count and exit count.
4. Match any positive result to broker history, magic number, comment, symbol and time window.
5. Recreate the loop with a FakeExecutor before connecting any broker adapter.

No code from this lead is promoted yet. The original directories remain untouched.
