# Test Contract

The test tree will contain four separate suites:

1. `contract`: schema and serialization checks;
2. `module`: deterministic tests for each adapter or strategy;
3. `integration`: full pipeline with fake broker and reconciliation;
4. `economic`: replay and holdout evaluation with costs, slippage and drawdown.

No module is promoted because another suite passed. The integrated suite must prove the complete path from data event to reconciled exit.
