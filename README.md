# Automated sales reporting, with synthetic data

A small, reproducible Python example of the reporting pipeline behind a weekly sales review. **This is a portfolio demonstration, not client code or a claim about a live deployment.** Every customer, transaction and result in this repository is synthetic.

## Business question

A team wants to know which acquisition channels bring revenue, how revenue compares across weeks, and where the weekly report changed. Manual spreadsheet work makes that answer slow and hard to reproduce.

## Approach

The script creates a deterministic sample of order records, validates them, aggregates revenue and order counts by week and channel, and writes a Markdown report and CSV summary. It flags week-over-week revenue changes. There are no dependencies, credentials, external calls or real customer records.

## Run

```bash
python3 reporting.py --output out
python3 -m unittest discover -s . -p "test_*.py" -v
```

Open `out/report.md` and `out/weekly_channels.csv`. Python 3.10+ is sufficient. Set `--seed` to another integer for a different, repeatable sample.

## Outcome and limits

The example replaces manual grouping with one repeatable command and adds input checks. Its output numbers are simulated, **not business results**. For a real deployment, I'd add a documented data contract, access controls, reconciliation against source systems, orchestration, observability, and agreed definitions for channel attribution and returns.
