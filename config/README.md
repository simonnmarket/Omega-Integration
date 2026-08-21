# Configuration

Configuration is versioned and separated by concern:

- asset universe and broker symbol mappings;
- risk and cost policy;
- engine selection;
- execution mode;
- report and evidence locations.

Secrets and account credentials are never committed. Runtime credentials must come from the host environment or a protected secret store.
