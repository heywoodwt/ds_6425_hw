#!/usr/bin/env python3
import sys
import traceback

try:
    # IMPORTANT: Import matplotlib and set backend BEFORE importing polars/pyarrow
    print("Step 1: Importing matplotlib...")
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for file output
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    print("✓ Matplotlib imported")

    print("\nStep 2: Importing polars...")
    import polars as pl
    print("✓ Polars imported")

    print("\nStep 3: Reading CSV...")
    csv_trades = pl.read_csv("trades_100k.csv")
    print(f"✓ Loaded {len(csv_trades)} rows")
    print(f"  Columns: {csv_trades.columns}")

    print("\nStep 4: Converting datetime...")
    csv_trades = csv_trades.with_columns(
        pl.col("created_time").str.to_datetime()
    ).sort(["ticker", "created_time"])
    print("✓ Datetime converted and sorted")

    print("\nStep 5: Creating ticker summary...")
    ticker_summary = csv_trades.group_by("ticker").agg([
        pl.len().alias("trade_count"),
    ]).sort("trade_count", descending=True)
    print(f"✓ Found {ticker_summary.height} unique tickers")

    print("\nStep 6: Getting top ticker...")
    top_ticker = ticker_summary[0, "ticker"]
    print(f"✓ Top ticker: {top_ticker}")

    print("\nStep 7: Filtering for top ticker...")
    ticker_trades = csv_trades.filter(pl.col("ticker") == top_ticker)
    print(f"✓ Filtered {len(ticker_trades)} trades")

    print("\nStep 8: Converting to pandas...")
    df = ticker_trades.select([
        "created_time",
        (pl.col("yes_price") / 100).alias("yes_price_dollars"),
        "count"
    ]).to_pandas()
    print(f"✓ Converted to pandas: {df.shape}")
    print(f"  Columns: {df.columns.tolist()}")
    print(f"  First row: {df.iloc[0].to_dict()}")

    print("\nStep 9: Creating plot...")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["created_time"], df["yes_price_dollars"], marker='o', linestyle='-', markersize=3, alpha=0.7)
    ax.set_title(f"{top_ticker}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Yes Price (USD)")
    ax.grid(True, alpha=0.3)
    print("✓ Plot created")

    print("\nStep 10: Saving plot...")
    plt.savefig("test_output.png", dpi=100, bbox_inches='tight')
    print("✓ Plot saved to test_output.png")

    print("\n" + "="*50)
    print("SUCCESS! No errors found.")
    print("="*50)

except Exception as e:
    print("\n" + "="*50)
    print("ERROR OCCURRED:")
    print("="*50)
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)