# Repository Layout

| Path | Purpose | Status |
|---|---|---|
| `contracts/` | stable data and intent contracts | active |
| `engines/` | signal and analysis engines | empty until adapters accepted |
| `adapters/` | legacy-to-contract translation | pending |
| `execution/` | one broker execution boundary | disabled foundation |
| `research/` | replay, datasets and holdouts | pending |
| `reports/` | generated technical and economic reports | pending |
| `evidence/` | immutable run evidence | active rules only |
| `config/` | asset and runtime configuration | active |
| `tracking/` | command, commit and provenance records | active |

The first engine to be adapted is Numeia 250625. It must remain traceable to its original source and must not bypass this layout.
