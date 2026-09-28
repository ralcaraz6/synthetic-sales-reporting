"""Synthetic weekly sales reporting demo. No external data or dependencies."""
from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

CHANNELS = ("organic", "paid_search", "referral")


@dataclass(frozen=True)
class Order:
    order_id: int
    customer_id: int
    order_date: date
    channel: str
    amount_cents: int


def sample_orders(seed: int = 42, n: int = 240) -> list[Order]:
    """Generate repeatable fake transactions across eight calendar weeks."""
    rng = random.Random(seed)
    start = date(2026, 1, 5)  # Monday
    return [Order(i + 1, rng.randint(1, 70), start + timedelta(days=rng.randrange(56)),
                  rng.choice(CHANNELS), rng.randint(1800, 42000)) for i in range(n)]


def aggregate(orders: list[Order]) -> list[dict[str, int | str]]:
    seen: set[int] = set()
    totals: dict[tuple[date, str], list[int]] = defaultdict(lambda: [0, 0])
    for order in orders:
        if order.order_id in seen:
            raise ValueError(f"Duplicate order ID: {order.order_id}")
        seen.add(order.order_id)
        if order.channel not in CHANNELS or order.amount_cents < 0:
            raise ValueError(f"Invalid order: {order.order_id}")
        week = order.order_date - timedelta(days=order.order_date.weekday())
        totals[(week, order.channel)][0] += 1
        totals[(week, order.channel)][1] += order.amount_cents
    return [{"week_start": week.isoformat(), "channel": channel,
             "orders": values[0], "revenue_cents": values[1]}
            for (week, channel), values in sorted(totals.items())]


def write_outputs(rows: list[dict[str, int | str]], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    with (output / "weekly_channels.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["week_start", "channel", "orders", "revenue_cents"])
        writer.writeheader()
        writer.writerows(rows)
    weeks: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for row in rows:
        week = weeks[str(row["week_start"])]
        week[0] += int(row["orders"])
        week[1] += int(row["revenue_cents"])
    lines = ["# Synthetic weekly sales report", "", "Demo data only. All revenue is simulated.", "",
             "| Week starting | Orders | Revenue (EUR) | WoW revenue |",
             "|---|---:|---:|---:|"]
    previous = None
    for week, (count, cents) in sorted(weeks.items()):
        change = "n/a" if previous is None or previous == 0 else f"{(cents / previous - 1) * 100:+.1f}%"
        lines.append(f"| {week} | {count} | {cents / 100:,.2f} | {change} |")
        previous = cents
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("out"))
    args = parser.parse_args()
    write_outputs(aggregate(sample_orders(args.seed)), args.output)
    print(f"Wrote {args.output / 'report.md'} and {args.output / 'weekly_channels.csv'}")


if __name__ == "__main__":
    main()
