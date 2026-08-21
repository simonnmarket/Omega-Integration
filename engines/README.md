# Engines

This directory contains strategy and analysis engines after adapter review.

Rules:

- engines consume normalized market data and produce signals;
- engines never import MT5, CTrade, OrderSend or broker transports;
- every engine declares source provenance and contract version;
- legacy code remains in its original repository until the adapter is accepted;
- no engine is considered profitable because it generated signals or historical PnL.

Planned adapter boundaries: `numeia/`, `artemis/`, `quantum/`, `samsung/`, `aurora/`.
