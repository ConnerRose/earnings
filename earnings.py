#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

EARNINGS_PATH = (
    Path.home() / "earnings"  # replace with your path to this repository
)
CSV_PATH = EARNINGS_PATH / "earnings.csv"


def log_earnings():
    columns = ["date", "duration", "profit"]
    if not CSV_PATH.exists():
        df = pd.DataFrame(columns=columns)
        df.to_csv(CSV_PATH, index=False)
    else:
        df = pd.read_csv(CSV_PATH)

    try:
        duration = float(input("Enter session duration (in hours): "))
        profit = float(input("Enter profit (can be negative): "))
    except ValueError as err:
        print(f"Invalid input. Exiting.\n{err}")
        return

    new_row = pd.DataFrame(
        [
            {
                "date": datetime.now().strftime("%m-%d-%y"),
                "duration": duration,
                "profit": profit,
            }
        ],
        columns=columns,
    )

    df = new_row if df.empty else pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    print("Session logged.")


def show_earnings():
    if not CSV_PATH.exists():
        print("No earnings data found.")
        return

    df = pd.read_csv(CSV_PATH)
    if df.empty:
        print("No earnings data to show.")
        return

    summary = {
        "Total Sessions": len(df),
        "Total Hours": df["duration"].sum(),
        "Total Profit": df["profit"].sum(),
        "Average Hourly": df["profit"].sum() / df["duration"].sum(),
    }

    for k, v in summary.items():
        print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"log", "show"}:
        print("Usage: earnings.py [log|show]")
        sys.exit(1)

    if sys.argv[1] == "log":
        log_earnings()
    elif sys.argv[1] == "show":
        show_earnings()
