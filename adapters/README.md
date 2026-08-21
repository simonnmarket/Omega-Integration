# Adapters

Adapters translate legacy systems into OMEGA contracts. They are the only permitted place for source-specific field mapping, symbol aliases and legacy behavior compatibility.

Every adapter must include:

- source path and revision;
- input/output contract;
- symbol and timeframe mapping;
- known stubs or unsupported behavior;
- deterministic fixture tests;
- broker-side-effect scan result.
