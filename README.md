# Bitcoin BTC-USD Streamlit Dashboard

An interactive data dashboard built with Streamlit that displays 1 month of hourly Bitcoin (BTC-USD) price data with a 20-period Moving Average indicator.

## Features

- Fetches 1 month of hourly BTC-USD OHLCV data via **yfinance**
- Caches data to a local **CSV file** (`btc_hourly_data.csv`) to avoid redundant API calls
- Displays **key metrics**: current price, 1-month high/low, average volume
- **Line chart** showing Close price alongside the 20-period Moving Average (MA20)
- **Raw data table** (most recent 200 rows, formatted)
- **Summary statistics** for the Close price
- One-click **Refresh** button to re-fetch live data

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run dashboard.py --server.port 5000
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Files

| File | Description |
|------|-------------|
| `dashboard.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |
| `btc_hourly_data.csv` | Auto-generated CSV cache of fetched data |

## Technical Indicator

The **20-Period Moving Average (MA20)** is computed as a rolling mean of the Close price over 20 hourly candles (~20 hours). It smooths short-term noise and helps identify the prevailing trend direction.
