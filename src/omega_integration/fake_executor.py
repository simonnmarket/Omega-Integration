from __future__ import annotations

from .contracts import FakeExecution, OrderIntent


class FakeExecutor:
    """Deterministic executor used before any broker adapter is enabled."""

    def __init__(self) -> None:
        self.executions: list[FakeExecution] = []
        self._seen: set[str] = set()

    def execute(self, intent: OrderIntent) -> FakeExecution:
        if intent.intent_id in self._seen:
            raise ValueError(f"duplicate intent: {intent.intent_id}")
        self._seen.add(intent.intent_id)
        result = FakeExecution(
            intent_id=intent.intent_id,
            order_id=f"FAKE-ORDER-{len(self.executions) + 1:04d}",
            deal_id=f"FAKE-DEAL-{len(self.executions) + 1:04d}",
            position_id=f"FAKE-POS-{len(self.executions) + 1:04d}",
            status="FILLED_FAKE",
        )
        self.executions.append(result)
        return result
