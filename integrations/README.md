# Integration Registry

These folders are adapter boundaries, not copies of the old systems. No legacy project is the canonical engine by default.

| Source | Intended role | Initial status |
|---|---|---|
| Numeia 250625 | candidate signal/execution behavior with reported historical profit | source identified; adapter pending; profit attribution unverified |
| Artemis | strategy and research component candidate | source identified; adapter pending |
| Quantum | indicator/feature component candidate | source identified; adapter pending |
| Samsung Global Market | signal transport/execution pattern candidate | source identified; adapter pending |
| Aurora Trading System | repository and architecture candidate | Git repository identified; full audit pending |

Each adapter must record the original absolute path, source hash, revision date, contract mapping, asset coverage, observed result provenance and known limitations. An adapter must not expose a second broker-send path.

## Component selection rule

The system will not copy an entire project because one project produced a positive observation. It will evaluate components by function: data, features, signal, veto, risk, execution, reconciliation and metrics. A component can be selected independently, combined with other candidates, or rejected. The selection record must identify what was retained, what was discarded and why.
