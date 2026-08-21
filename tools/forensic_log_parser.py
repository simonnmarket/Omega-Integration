#!/usr/bin/env python3
"""Parse trading logs into auditable event counts without broker access."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

TIMESTAMP = re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})")
TRADES = re.compile(r"Trades:\s*(?P<count>\d+)", re.IGNORECASE)


def classify(message: str) -> str:
    lower = message.lower()
    if "scan completo" in lower:
        return "scan_cycle"
    if "order_send" in lower or "enviando ordem" in lower or "executando trade" in lower:
        if "retcode" in lower or "invalid stops" in lower or "erro" in lower:
            return "order_attempt_or_rejection"
        return "order_attempt"
    if "position_select" in lower or "nonetype" in lower or "exception" in lower:
        return "runtime_error"
    if "trades:" in lower:
        return "trade_count_report"
    if "profit" in lower or "lucro" in lower:
        return "profit_message"
    return "other"


def parse(path: Path) -> dict[str, object]:
    counts: Counter[str] = Counter()
    trade_reports: list[int] = []
    first: datetime | None = None
    last: datetime | None = None
    lines = 0
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        lines += 1
        match = TIMESTAMP.match(raw)
        if match:
            current = datetime.strptime(match.group("ts"), "%Y-%m-%d %H:%M:%S,%f")
            first = first or current
            last = current
        message = raw.split(" - ", 2)[-1] if " - " in raw else raw
        kind = classify(message)
        counts[kind] += 1
        trade_match = TRADES.search(message)
        if trade_match:
            trade_reports.append(int(trade_match.group("count")))
    elapsed = (last - first).total_seconds() if first and last else None
    return {
        "schema": "omega.forensic-log-summary.v1",
        "source": str(path),
        "lines": lines,
        "first_timestamp": first.isoformat(sep=" ") if first else None,
        "last_timestamp": last.isoformat(sep=" ") if last else None,
        "elapsed_seconds": elapsed,
        "events": dict(sorted(counts.items())),
        "trade_count_reports": len(trade_reports),
        "trade_count_max_reported": max(trade_reports) if trade_reports else None,
        "trade_count_sum_reported": sum(trade_reports) if trade_reports else 0,
        "broker_access": "NOT_PERFORMED_PARSER_ONLY",
        "economic_interpretation": "NOT_ESTABLISHED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.log.is_file():
        raise SystemExit(f"log does not exist: {args.log}")
    result = parse(args.log)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(result["events"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
