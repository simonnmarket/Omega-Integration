# Evidence Rules

Every replay or test run must preserve:

- source and adapter hashes;
- configuration and asset universe;
- input fixture or market-data range;
- signals generated;
- vetoes and reasons;
- order intents;
- broker requests and retcodes;
- order, deal, position and exit identifiers;
- gross costs and net results;
- errors, rejects and shutdown state.

Never use order acceptance as a substitute for a deal, and never use a deal as proof of profitability without reconciled costs and exits.
