# -*- coding: utf-8 -*-
"""Explore 日志回放指标统计（阶段B验收工具）。

用法:
    python3 backend/scripts/explore_replay_metrics.py --log backend/logs/app.log
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


SEARCH_DONE_RE = re.compile(
    r"done=search_analysis_fragments.*?hits=(?P<hits>\d+).*?keywords=(?P<keywords>[^ ]+).*?"
    r"total_hits=(?P<total_hits>\d+).*?has_more=(?P<has_more>True|False)"
)
PENDING_PAGE_RE = re.compile(r"search_analysis_fragments pending-page blocked")
LOOP_DONE_RE = re.compile(r"探索完成\(工具循环\): (?P<rounds>\d+)轮")


@dataclass
class SearchEvent:
    keywords: str
    hits: int
    total_hits: int
    has_more: bool


def _percentile(values: List[int], p: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return float(values[0])
    rank = max(0.0, min(1.0, p)) * (len(values) - 1)
    lower = int(math.floor(rank))
    upper = int(math.ceil(rank))
    if lower == upper:
        return float(values[lower])
    weight = rank - lower
    return float(values[lower]) * (1 - weight) + float(values[upper]) * weight


def parse_log(log_path: Path) -> Dict[str, float]:
    search_events: List[SearchEvent] = []
    pending_page_blocked = 0
    loop_rounds: List[int] = []

    with log_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = SEARCH_DONE_RE.search(line)
            if m:
                search_events.append(
                    SearchEvent(
                        keywords=str(m.group("keywords") or ""),
                        hits=int(m.group("hits") or 0),
                        total_hits=int(m.group("total_hits") or 0),
                        has_more=(m.group("has_more") == "True"),
                    )
                )
                continue

            if PENDING_PAGE_RE.search(line):
                pending_page_blocked += 1
                continue

            m_loop = LOOP_DONE_RE.search(line)
            if m_loop:
                loop_rounds.append(int(m_loop.group("rounds") or 0))

    total_search = len(search_events)
    zero_hits = sum(1 for ev in search_events if ev.hits <= 0)
    zero_hit_rate = (zero_hits / total_search) if total_search else 0.0

    repeated_zero = 0
    repeated_non_zero = 0
    prev: Optional[SearchEvent] = None
    for ev in search_events:
        if prev and ev.keywords == prev.keywords:
            if ev.hits <= 0 and prev.hits <= 0:
                repeated_zero += 1
            if ev.hits > 0 and prev.hits > 0:
                repeated_non_zero += 1
        prev = ev

    has_more_events = sum(1 for ev in search_events if ev.has_more)
    has_more_rate = (has_more_events / total_search) if total_search else 0.0

    loop_rounds_sorted = sorted(loop_rounds)
    return {
        "total_search_calls": float(total_search),
        "zero_hit_calls": float(zero_hits),
        "zero_hit_rate": round(zero_hit_rate, 4),
        "repeated_zero_pairs": float(repeated_zero),
        "repeated_non_zero_pairs": float(repeated_non_zero),
        "has_more_calls": float(has_more_events),
        "has_more_rate": round(has_more_rate, 4),
        "pending_page_blocked": float(pending_page_blocked),
        "loop_count": float(len(loop_rounds_sorted)),
        "loop_round_p50": round(_percentile(loop_rounds_sorted, 0.5), 2),
        "loop_round_p95": round(_percentile(loop_rounds_sorted, 0.95), 2),
        "loop_round_max": float(max(loop_rounds_sorted) if loop_rounds_sorted else 0),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Explore 日志回放指标统计")
    parser.add_argument("--log", default="backend/logs/app.log", help="日志文件路径")
    args = parser.parse_args()

    log_path = Path(args.log)
    if not log_path.exists():
        raise SystemExit(f"log file not found: {log_path}")

    metrics = parse_log(log_path)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
