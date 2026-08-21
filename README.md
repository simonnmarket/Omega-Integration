# OMEGA Canonical Architecture

Status: FOUNDATION ONLY - no trading execution is enabled by this repository.

This directory is the canonical integration foundation for the OMEGA ecosystem. It does not replace the original projects. It defines the contracts that allow the best parts of Numeia, Artemis, Quantum, Samsung Global Market and Aurora to be evaluated and integrated without creating parallel order paths.

## Operating objective

Recover the useful behavior already present in the working Numeia baseline, then add components only through explicit adapters and measurable contracts. Profit is a target to be investigated, not a property assumed from historical results.

## Canonical flow

`broker/data adapter -> normalized market event -> features -> strategy signal -> veto/consensus -> risk decision -> order intent -> one execution adapter -> broker transaction -> reconciliation -> metrics`

## Non-negotiable boundaries

- Strategy modules produce signals; they never send orders.
- Risk and veto modules may deny an intent; they may not silently rewrite it.
- Only the execution adapter may call an MT5 or broker API.
- Every intent, order, deal, position and exit must carry an idempotent identifier.
- A broker acknowledgement is not a fill. Retcode, deal and position state must be reconciled separately.
- Asset-specific behavior belongs in a configuration or adapter, never in the shared decision contract.
- Original source folders remain read-only references until a module is accepted.

## Current verified source baseline

The strongest source baseline identified so far is `E:\Arquivos Numeia\Numeia 250625`, especially `Expert\NumeiaEA.mq5` and the modular files under `Core\` and `Agents\`. It contains real `CTrade` paths, but also contains stubs and placeholders; it is therefore a source candidate, not a qualified production engine.

The GitHub repository confirmed reachable during discovery is `https://github.com/simonnmarket/AURORA-Trading-System`. Full repository-account inventory was not independently retrieved in this run and must not be treated as complete.

## First implementation order

1. Normalize the market-data, signal and order-intent contracts in `contracts/`.
2. Wrap Numeia behind `integrations/numeia/`; do not copy direct broker calls into strategy code.
3. Add fake execution and replay adapters before any broker adapter.
4. Reproduce the historical Numeia behavior with the same symbol, period, inputs and magic/comment data.
5. Only then compare modules from Artemis, Quantum, Samsung and Aurora by isolated adapter tests.

This foundation does not authorize live trading, DEMO trading or automatic order submission.
