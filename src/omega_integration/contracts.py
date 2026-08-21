from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class SymbolSpec:
    symbol: str
    price: Decimal
    contract_size: Decimal
    min_volume: Decimal
    volume_step: Decimal
    max_volume: Decimal


@dataclass(frozen=True)
class OrderIntent:
    intent_id: str
    symbol: str
    side: str
    volume: Decimal
    target_value: Decimal
    source: str
    reason: str


@dataclass(frozen=True)
class FakeExecution:
    intent_id: str
    order_id: str
    deal_id: str
    position_id: str
    status: str

