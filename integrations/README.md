# Integration Registry

These folders are adapter boundaries, not copies of the old systems.

| Source | Intended role | Initial status |
|---|---|---|
| Numeia 250625 | baseline execution and modular decision candidate | source identified; adapter pending |
| Artemis | strategy and research component candidate | source identified; adapter pending |
| Quantum | indicator/feature component candidate | source identified; adapter pending |
| Samsung Global Market | external signal transport/execution pattern candidate | source identified; adapter pending |
| Aurora Trading System | repository and architecture reference | Git HEAD reachable; full audit pending |

Each adapter must record the original absolute path, source hash, revision date, contract mapping and known limitations. An adapter must not expose a second broker-send path.
