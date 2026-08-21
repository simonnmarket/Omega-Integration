# Numeia v5.1 Multi-Asset Portfolio EA - Technical Analysis

Status: `HIGH-VALUE CANDIDATE / NOT PROMOTED`

## Source identity

- Input: `C:\Users\Lenovo\.codex\attachments\f9384e0b-13e8-41b1-8b34-367b00c4ab0f\pasted-text.txt`
- Bytes: 17,878
- SHA256: `DF0CF5AE0713CABC1774E030FF30C57A10E41E8162563714EDB6541EE9B61131`
- Language: MQL5
- Declared version: `5.10`

## What the code actually does

This is a multi-asset portfolio allocator, not a directional signal engine.

1. It defines nine active symbols: US500, GER40, UK100, XAUUSD, XAGUSD, UKOIL+, EURUSD, GBPUSD and USDJPY.
2. It assigns target weights totalling 95% and keeps a nominal 5% cash reserve.
3. On first portfolio initialization it calculates target values and sends BUY orders for every asset.
4. It checks allocation drift only after 90 days and rebalances when the deviation threshold is exceeded.
5. It closes its own positions when the balance-based kill switch exceeds 30%.

There is no entry signal, prediction model, regime filter or market-direction decision in this file. Its economic behavior is closer to an automated diversified buy-and-hold portfolio with periodic rebalancing.

## Important code facts

| Area | Evidence | Assessment |
|---|---|---|
| Asset count | `NUM_ASSETS=9` at line 82 | Header says 10 assets, but the implementation uses 9 plus nominal cash |
| Initial execution | `InitializePortfolio()` and `BuyAsset()` | Sends multiple BUY orders immediately after initialization |
| Broker API | `CTrade` and `trade.Buy()` | Real execution path exists |
| Result confirmation | boolean result only | Does not prove retcode, deal or position reconciliation |
| Rebalance | `InpRebalanceDays=90` | Slow portfolio maintenance, not active trading |
| Risk stop | `ACCOUNT_BALANCE` at lines 205-210 | Ignores floating equity drawdown and starts from a single balance snapshot |
| Stops | Buy uses `sl=0`, `tp=0` | No protective SL/TP is sent |
| Partial initialization | `successCount >= NUM_ASSETS - 1` | Accepts 8/9 assets and can leave the portfolio incomplete |
| Position value | `GetPositionValue()` | Uses a generic contract-size formula that may be wrong across FX, CFDs and indices |
| Volume | `NormalizeVolume()` | Needs broker symbol contract, step, min/max and rounding tests |
| Timing | `Sleep(500)` inside loops | Can block the event handler during multi-order initialization/rebalance |

## Why the reported profit is plausible

The code buys several assets at startup. A profit observation above USD 2,000 is therefore plausible if the account had sufficient capital, the market period rose, the broker symbols mapped correctly and positions remained open or were later closed profitably.

However, the code alone cannot establish that the amount came from a predictive edge. To attribute the result, we need the MT5 history export containing period, symbol, magic `50010`, comments, deals, exits, commissions, swaps and balance/equity curve.

## Reusable components

- multi-asset target-weight registry;
- asset-class grouping;
- target-value allocation;
- portfolio drift and rebalance concept;
- magic-number isolation;
- candidate cash-reserve policy;
- portfolio-level exposure model.

## Must be replaced before integration

- direct `CTrade` calls;
- boolean-only execution confirmation;
- balance-only kill switch;
- no-SL/no-TP entry path;
- 8/9 partial-success rule;
- generic position-value formula;
- blocking `Sleep()` order loop;
- absence of idempotency and transaction reconciliation.

## OMEGA integration decision

`RETAIN_COMPONENTS`: portfolio allocation and rebalance concepts.

`ADAPT`: asset registry, target weights, exposure and cash policy.

`ISOLATE`: direct execution and broker-specific volume/value logic.

`PENDING_EVIDENCE`: the reported profit and its exact source.

`REJECT_AS_CANONICAL_SIGNAL`: this file does not contain a directional signal engine.

## Immediate next implementation

Convert the allocator into an OMEGA `PortfolioAllocation` module that emits `order_intent.schema.json` objects. The module must use FakeExecutor first, reconcile every intent/order/deal/position/exit, and compare the original portfolio behavior against the adapted behavior on the same historical inputs.
