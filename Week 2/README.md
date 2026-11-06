# Stock Portfolio Tracker

A simple yet functional investment portfolio tracking utility written in pure Python.

## Features

- Interactively enter stock ticker symbols, buy prices, and share quantities
- Live market price lookup via Yahoo Finance (`yfinance`)
- Optional validation against the S&P 500 constituents list
- Formatted console report showing:
  - Cost basis, current market value
  - Dollar and percentage gain/loss **per holding**
  - Aggregate portfolio totals
- Automatic export of the full summary to `portfolio_summary.csv`

## Requirements

- Python 3.8+
- `yfinance` (`pip install yfinance`)

## Quick Start

```bash
# Install dependency
pip install yfinance

# Interactive mode
python portfolio.py

# Demo mode (pre-populated sample portfolio)
python portfolio.py --demo
```

## Project Layout

```
.
├── portfolio.py            # Main application
├── constituents.csv        # S&P 500 ticker reference data
├── portfolio_summary.csv   # Generated output (created on first run)
└── README.md
```

## Sample Output (demo mode)

```
========================================================================
                        Stock Portfolio Tracker
========================================================================
...
  Total Invested Capital : $9,065.00
  Current Market Value   : $17,546.48
  Overall Gain / Loss    : $+8,481.48  (+93.56%)
...
✓ Portfolio summary written to: .../portfolio_summary.csv
```

## Notes

- Prices are fetched live; results will vary with market conditions.
- The script gracefully handles missing tickers or temporary API issues.
- `constituents.csv` is used only for optional ticker validation and is not required for price lookups.
