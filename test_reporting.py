import tempfile
import unittest
from datetime import date
from pathlib import Path
from reporting import Order, aggregate, sample_orders, write_outputs


class ReportingTests(unittest.TestCase):
    def test_repeatable_sample(self):
        self.assertEqual(sample_orders(), sample_orders())
        self.assertNotEqual(sample_orders(1), sample_orders(2))

    def test_week_and_channel_aggregation(self):
        rows = aggregate([Order(1, 1, date(2026, 1, 5), "organic", 1000),
                          Order(2, 2, date(2026, 1, 11), "organic", 2000)])
        self.assertEqual(rows, [{"week_start": "2026-01-05", "channel": "organic",
                                 "orders": 2, "revenue_cents": 3000}])

    def test_invalid_orders(self):
        order = Order(1, 1, date(2026, 1, 5), "organic", 1000)
        with self.assertRaises(ValueError):
            aggregate([order, order])
        with self.assertRaises(ValueError):
            aggregate([Order(2, 1, date(2026, 1, 5), "unknown", 1000)])
        with self.assertRaises(ValueError):
            aggregate([Order(3, 1, date(2026, 1, 5), "organic", -1)])

    def test_output(self):
        with tempfile.TemporaryDirectory() as temp:
            write_outputs(aggregate(sample_orders()), Path(temp))
            self.assertIn("Demo data only", (Path(temp) / "report.md").read_text())
            self.assertIn("week_start,channel,orders,revenue_cents", (Path(temp) / "weekly_channels.csv").read_text())


if __name__ == "__main__":
    unittest.main()
