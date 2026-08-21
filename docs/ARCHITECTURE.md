# OMEGA Modular Architecture

## Layers

| Layer | Responsibility | May depend on | Must not do |
|---|---|---|---|
| Data | Convert broker or file data to normalized events | adapters, contracts | create signals or orders |
| Features | Calculate indicators and market descriptors | data contracts | call broker APIs |
| Strategies | Produce directional or neutral signals | features, contracts | size positions or send orders |
| Decision | Combine signals and apply vetoes | strategies, risk inputs | bypass risk |
| Risk | Validate exposure, loss, cost and limits | decision, portfolio state | send orders |
| Execution | Translate one approved intent to one broker request | broker adapter, contracts | invent signals |
| Reconciliation | Link request, acknowledgement, deal, position and exit | broker events, ledgers | infer fills from a boolean |
| Metrics | Calculate gross/net results and diagnostics | reconciled events | change trading state |

## Dependency rule

Dependencies point inward toward contracts. A module can be replaced without changing the contracts above it. No strategy, feature or integration may import `MetaTrader5`, `CTrade`, `OrderSend` or an equivalent broker function directly. Static checks will reject those imports outside the execution adapter.

## Asset expansion

The shared contracts are asset-agnostic. Symbol rules, tick size, point value, trading sessions, minimum volume, spread limits and cost models belong to the asset profile. XAUUSD, XAGUSD, FX, indices, energy and crypto can therefore use the same pipeline without contaminating one another.

## Acceptance of an old component

An old component is accepted only when its adapter demonstrates:

- declared inputs and outputs;
- deterministic behavior on a fixed fixture;
- no hidden broker side effects;
- traceable provenance to the original file and revision;
- correct behavior for at least one normal case, one rejection case and one malformed-input case;
- no direct execution path outside `execution/`.

## Evidence required for an economic comparison

The comparison must keep separate: generated signals, approved intents, broker requests, accepted orders, deals, open positions, exits, gross PnL, costs and net PnL. A strategy cannot be promoted from signal count or order acceptance alone.
