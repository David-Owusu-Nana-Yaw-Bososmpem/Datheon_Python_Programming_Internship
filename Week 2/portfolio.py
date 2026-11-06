#!/usr/bin/env python3
"""
Stock Portfolio Tracker
=======================
Interactive utility to track investment positions.
Users enter ticker symbols, buy prices, and share quantities.
The script fetches live market prices (via yfinance), computes
portfolio value, per-holding gain/loss, and writes a summary
to portfolio_summary.csv.
"""

from __future__ import annotations

import csv
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance is required. Install with: pip install yfinance")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class Position:
    """Represents a single portfolio holding."""

    def __init__(self, ticker: str, buy_price: float, shares: float):
        self.ticker = ticker.upper().strip()
        self.buy_price = float(buy_price)
        self.shares = float(shares)
        self.current_price: Optional[float] = None
        self.name: str = ticker  # will be filled from yfinance if available

    @property
    def cost_basis(self) -> float:
        return self.buy_price * self.shares

    @property
    def market_value(self) -> float:
        if self.current_price is None:
            return 0.0
        return self.current_price * self.shares

    @property
    def gain_loss(self) -> float:
        return self.market_value - self.cost_basis

    @property
    def gain_loss_pct(self) -> float:
        if self.cost_basis == 0:
            return 0.0
        return (self.gain_loss / self.cost_basis) * 100.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_sp500_tickers(csv_path: str = "constituents.csv") -> set:
    """Load valid S&P 500 ticker symbols from the provided CSV (optional validation)."""
    tickers = set()
    if not os.path.isfile(csv_path):
        return tickers
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sym = row.get("Symbol", "").strip()
                if sym:
                    tickers.add(sym.upper())
    except Exception:
        pass
    return tickers


def fetch_price(ticker: str) -> Tuple[Optional[float], str]:
    """
    Fetch the latest closing / regular-market price for a ticker.
    Returns (price, company_name).
    """
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}
        # Prefer regularMarketPrice, fall back to previousClose / currentPrice
        price = (
            info.get("regularMarketPrice")
            or info.get("currentPrice")
            or info.get("previousClose")
        )
        name = info.get("shortName") or info.get("longName") or ticker
        if price is None:
            # last-ditch: download recent history
            hist = t.history(period="5d")
            if not hist.empty:
                price = float(hist["Close"].iloc[-1])
        return (float(price) if price is not None else None, str(name))
    except Exception as exc:
        print(f"  [warning] Could not fetch price for {ticker}: {exc}")
        return None, ticker


def print_header(title: str) -> None:
    width = 72
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_position_table(positions: List[Position]) -> None:
    """Pretty-print the holdings table to the console."""
    headers = [
        "Ticker",
        "Name",
        "Shares",
        "Buy $",
        "Curr $",
        "Cost Basis",
        "Mkt Value",
        "Gain/Loss $",
        "Gain/Loss %",
    ]
    # Column widths
    widths = [8, 22, 10, 10, 10, 12, 12, 12, 12]

    def fmt_row(vals: List[str]) -> str:
        return "  ".join(str(v).ljust(w) for v, w in zip(vals, widths))

    print(fmt_row(headers))
    print("-" * (sum(widths) + 2 * (len(widths) - 1)))

    for p in positions:
        name = (p.name[:20] + "…") if len(p.name) > 21 else p.name
        curr = f"{p.current_price:.2f}" if p.current_price is not None else "N/A"
        gl_str = f"{p.gain_loss:+.2f}" if p.current_price is not None else "N/A"
        glp_str = f"{p.gain_loss_pct:+.2f}%" if p.current_price is not None else "N/A"
        row = [
            p.ticker,
            name,
            f"{p.shares:.2f}",
            f"{p.buy_price:.2f}",
            curr,
            f"{p.cost_basis:.2f}",
            f"{p.market_value:.2f}" if p.current_price is not None else "N/A",
            gl_str,
            glp_str,
        ]
        print(fmt_row(row))


def write_summary_csv(positions: List[Position], path: str = "portfolio_summary.csv") -> None:
    """Write the portfolio summary to a CSV file."""
    fieldnames = [
        "Timestamp",
        "Ticker",
        "Security Name",
        "Shares",
        "Buy Price",
        "Current Price",
        "Cost Basis",
        "Market Value",
        "Gain/Loss ($)",
        "Gain/Loss (%)",
    ]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in positions:
            writer.writerow(
                {
                    "Timestamp": now,
                    "Ticker": p.ticker,
                    "Security Name": p.name,
                    "Shares": f"{p.shares:.4f}",
                    "Buy Price": f"{p.buy_price:.4f}",
                    "Current Price": f"{p.current_price:.4f}" if p.current_price is not None else "",
                    "Cost Basis": f"{p.cost_basis:.2f}",
                    "Market Value": f"{p.market_value:.2f}" if p.current_price is not None else "",
                    "Gain/Loss ($)": f"{p.gain_loss:.2f}" if p.current_price is not None else "",
                    "Gain/Loss (%)": f"{p.gain_loss_pct:.2f}" if p.current_price is not None else "",
                }
            )
    print(f"\n✓ Portfolio summary written to: {os.path.abspath(path)}")


# ---------------------------------------------------------------------------
# Interactive input
# ---------------------------------------------------------------------------

def prompt_positions(valid_tickers: Optional[set] = None) -> List[Position]:
    """Interactively collect portfolio positions from the user."""
    positions: List[Position] = []
    print_header("Add Portfolio Positions")
    print("Enter ticker, buy price, and number of shares.")
    print("Leave ticker blank (or type 'done') when finished.\n")

    while True:
        ticker = input("  Ticker symbol (or 'done'): ").strip()
        if not ticker or ticker.lower() in ("done", "quit", "q", "exit"):
            break

        ticker = ticker.upper()
        if valid_tickers and ticker not in valid_tickers:
            print(f"    Note: {ticker} is not in the local S&P 500 list – continuing anyway.")

        try:
            buy_str = input(f"  Buy price for {ticker}: ").strip().replace(",", "")
            buy_price = float(buy_str)
            if buy_price <= 0:
                raise ValueError("Buy price must be positive")
        except ValueError as e:
            print(f"    Invalid buy price ({e}). Skipping this ticker.")
            continue

        try:
            shares_str = input(f"  Number of shares for {ticker}: ").strip().replace(",", "")
            shares = float(shares_str)
            if shares <= 0:
                raise ValueError("Shares must be positive")
        except ValueError as e:
            print(f"    Invalid share quantity ({e}). Skipping this ticker.")
            continue

        positions.append(Position(ticker, buy_price, shares))
        print(f"    → Added {shares} shares of {ticker} @ ${buy_price:.2f}\n")

    return positions


def demo_positions() -> List[Position]:
    """Return a sample portfolio so the script can be run non-interactively."""
    return [
        Position("AAPL", 150.00, 10),
        Position("MSFT", 280.00, 5),
        Position("GOOGL", 120.00, 8),
        Position("NVDA", 400.00, 3),
        Position("AMZN", 140.00, 6),
        Position("JPM", 145.00, 12),
        Position("XOM", 95.00, 15),
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print_header("Stock Portfolio Tracker")
    print("Live prices powered by Yahoo Finance (yfinance)")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Optional S&P 500 validation set
    sp500 = load_sp500_tickers(
        os.path.join(os.path.dirname(__file__) or ".", "constituents.csv")
    )
    if sp500:
        print(f"Loaded {len(sp500)} S&P 500 tickers for optional validation.")

    # Decide interactive vs demo
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--demo", "-d", "demo"):
        print("\nRunning in DEMO mode with sample holdings…")
        positions = demo_positions()
    else:
        print("\nTip: pass --demo on the command line to use a pre-built sample portfolio.")
        positions = prompt_positions(sp500)

    if not positions:
        print("\nNo positions entered. Exiting.")
        return

    # Fetch live prices
    print_header("Fetching Live Market Prices")
    for p in positions:
        print(f"  Looking up {p.ticker} …", end=" ", flush=True)
        price, name = fetch_price(p.ticker)
        p.current_price = price
        p.name = name
        if price is not None:
            print(f"${price:.2f}  ({name})")
        else:
            print("FAILED")

    # Console report
    print_header("Portfolio Holdings")
    print_position_table(positions)

    # Aggregates
    total_cost = sum(p.cost_basis for p in positions)
    total_value = sum(p.market_value for p in positions if p.current_price is not None)
    total_gl = total_value - total_cost
    total_gl_pct = (total_gl / total_cost * 100.0) if total_cost else 0.0

    print("\n" + "-" * 72)
    print(f"  Total Invested Capital : ${total_cost:,.2f}")
    print(f"  Current Market Value   : ${total_value:,.2f}")
    print(f"  Overall Gain / Loss    : ${total_gl:+,.2f}  ({total_gl_pct:+.2f}%)")
    print("-" * 72)

    # Persist summary
    out_path = os.path.join(os.path.dirname(__file__) or ".", "portfolio_summary.csv")
    write_summary_csv(positions, out_path)

    print("\nDone.")


if __name__ == "__main__":
    main()
