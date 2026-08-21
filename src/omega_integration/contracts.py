from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


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


@dataclass(frozen=True)
class Signal:
    signal_id: str
    event_id: str
    symbol: str
    strategy_id: str
    direction: str
    score: Decimal
    confidence: Decimal
    generated_at: datetime
    valid_until: datetime
    features_ref: str | None = None
