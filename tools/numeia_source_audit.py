#!/usr/bin/env python3
"""Build a deterministic, read-only audit of a Numeia source snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable


SOURCE_EXTENSIONS = {".mq5", ".mqh"}
BROKER_PATTERNS = {
    "ctrade": re.compile(r"\bCTrade\b"),
    "order_send": re.compile(r"\bOrderSend\s*\("),
    "buy": re.compile(r"\.Buy\s*\("),
    "sell": re.compile(r"\.Sell\s*\("),
    "position_close": re.compile(r"PositionClose(?:Partial)?\s*\("),
}
STUB_PATTERNS = {
    "placeholder": re.compile(r"placeholder", re.IGNORECASE),
    "todo": re.compile(r"\bTODO\b", re.IGNORECASE),
    "not_implemented": re.compile(r"not\s+implemented", re.IGNORECASE),
    "permissive_true": re.compile(r"return\s+true\s*;"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def matching_lines(text: str, patterns: dict[str, re.Pattern[str]]) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        names = [name for name, pattern in patterns.items() if pattern.search(line)]
        if names:
            matches.append({"line": number, "patterns": names, "text": line.strip()})
    return matches


def source_files(root: Path) -> Iterable[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file() and path.suffix in SOURCE_EXTENSIONS)


def audit(root: Path) -> dict[str, object]:
    files: list[dict[str, object]] = []
    broker_total = 0
    stub_total = 0
    for path in source_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        broker = matching_lines(text, BROKER_PATTERNS)
        stubs = matching_lines(text, STUB_PATTERNS)
        broker_total += len(broker)
        stub_total += len(stubs)
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "broker_matches": broker,
                "stub_matches": stubs,
                "classification": "execution_boundary_candidate" if broker else "analysis_or_support_candidate",
            }
        )
    return {
        "schema": "omega.numeia.source-audit.v1",
        "source_root": str(root),
        "source_root_exists": root.is_dir(),
        "read_only": True,
        "file_count": len(files),
        "broker_match_count": broker_total,
        "stub_match_count": stub_total,
        "files": files,
        "promotion_status": "PENDING_ADAPTER_AND_REPLAY",
        "broker_side_effect": "NONE_AUDIT_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    if not result["source_root_exists"]:
        raise SystemExit(f"source root does not exist: {args.source}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("file_count", "broker_match_count", "stub_match_count", "promotion_status")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
