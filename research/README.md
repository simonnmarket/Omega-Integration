# Research

Research artifacts are offline-only until explicitly promoted through the execution boundary.

Required separation:

- `datasets/`: immutable input references;
- `replays/`: reproducible runs;
- `holdout/`: untouched evaluation data;
- `comparisons/`: baseline versus candidate results;
- `models/`: research artifacts with provenance.

No research file may silently alter runtime configuration.
