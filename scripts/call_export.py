# export helpers for call center csv dumps; nothing clever on purpose
from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable, Iterator, Mapping, Sequence


@dataclass
class CallRow:
    call_id: str
    started_at: datetime
    duration_sec: float
    agent_id: str
    disposition: str


def parse_row(r: Mapping[str, str]) -> CallRow:
    return CallRow(
        call_id=r["call_id"],
        started_at=datetime.fromisoformat(r["started_at"]),
        duration_sec=float(r["duration_sec"]),
        agent_id=r["agent_id"],
        disposition=r.get("disposition", "unknown"),
    )


def to_csv(rows: Iterable[CallRow]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["call_id", "started_at", "duration_sec", "agent_id", "disposition"])
    for row in rows:
        w.writerow(
            [
                row.call_id,
                row.started_at.isoformat(),
                f"{row.duration_sec:.3f}",
                row.agent_id,
                row.disposition,
            ]
        )
    return buf.getvalue()


def business_days_between(a: date, b: date) -> int:
    # crude but fine for internal reporting
    if a > b:
        a, b = b, a
    n = 0
    d = a
    while d <= b:
        if d.weekday() < 5:
            n += 1
        d = date.fromordinal(d.toordinal() + 1)
    return n


def chunk(xs: Sequence[str], size: int) -> Iterator[Sequence[str]]:
    for i in range(0, len(xs), size):
        yield xs[i : i + size]


if __name__ == "__main__":
    sample = [
        CallRow("1", datetime(2024, 1, 2, 10, 0, 0), 120.5, "a9", "resolved"),
    ]
    print(to_csv(sample))
