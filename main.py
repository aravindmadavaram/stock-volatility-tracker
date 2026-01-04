import sys
import os
import time
from datetime import datetime

# Warn on older Python (3.9) but attempt to import compatible yfinance
if sys.version_info < (3, 10):
    print(f"Warning: running on Python {sys.version.split()[0]} — some yfinance releases require Python 3.10+.")
    print("If you see typing syntax errors when importing yfinance, install a compatible release:")
    print("  python -m pip install 'yfinance<0.2.0'")

try:
    import yfinance as yf
except Exception as e:
    print("Failed to import yfinance:", e)
    print("Try installing a yfinance version compatible with your Python or upgrade Python.")
    sys.exit(1)

import pandas as pd

# List of Tech Stocks to Track
tickers = ['AAPL', 'AMZN', 'GOOGL', 'TSLA', 'MSFT', 'NVDA']

def fetch_stock_data():
    print(f"--- Fetching Data at {datetime.now()} ---")
    stock_data = []
    
    for ticker in tickers:
        try:
            # Try download first (sometimes more reliable) with retries
            hist = None
            attempts = 3
            for attempt in range(1, attempts + 1):
                try:
                    hist = yf.download(ticker, period="30d", progress=False)
                    if hist is not None and not hist.empty:
                        break
                except Exception as exc:
                    print(f"Attempt {attempt} download error for {ticker}: {exc}")
                time.sleep(1 * attempt)

            # Fallback to Ticker.history if download returned nothing
            if hist is None or hist.empty:
                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period="30d")
                except Exception as exc:
                    print(f"Fallback history failed for {ticker}: {exc}")

            # If still empty, try yahooquery as a last resort
            if (hist is None or hist.empty):
                try:
                    from yahooquery import Ticker as YQTicker
                    yq = YQTicker(ticker)
                    yq_hist = yq.history(period='30d')
                    # yahooquery returns a MultiIndex when multiple symbols; handle single symbol
                    if isinstance(yq_hist, dict):
                        yq_hist = pd.DataFrame()
                    if not yq_hist.empty:
                        # Normalize column names (yahooquery returns lowercase names)
                        try:
                            yq_hist.columns = [str(c).capitalize() for c in yq_hist.columns]
                        except Exception:
                            pass
                        hist = yq_hist
                        print(f"{ticker}: fetched data via yahooquery fallback")
                except Exception as exc:
                    print(f"yahooquery fallback failed for {ticker}: {exc}")

            # If no history was returned, skip this ticker
            if hist is None or hist.empty:
                print(f"- {ticker}: No data found for this date range or data unavailable")
                continue

            # Use last available row for volatility calculation
            current_price = hist['Close'].iloc[-1]
            high = hist['High'].iloc[-1]
            low = hist['Low'].iloc[-1]
            volatility = ((high - low) / current_price) * 100
            
            # Flag if volatility is greater than 2%
            status = "High Volatility" if volatility > 2.0 else "Stable"
            
            stock_data.append({
                "Ticker": ticker,
                "Price": round(current_price, 2),
                "Volatility %": round(volatility, 2),
                "Status": status
            })
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    # Create DataFrame
    df = pd.DataFrame(stock_data)
    print(df)

    # Skip saving if there's no data
    if df.empty:
        print("No data fetched; skipping CSV save.\n")
        return

    # Save to CSV (Simulating a Database Load)
    csv_path = 'market_data_log.csv'
    write_header = not os.path.exists(csv_path)
    df.to_csv(csv_path, mode='a', header=write_header, index=False)
    print("Data saved to CSV.\n")

if __name__ == "__main__":
    # Run loop to simulate real-time tracking
    fetch_stock_data()