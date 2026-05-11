import streamlit as st
import yfinance as yf
import pandas as pd
import os

DATA_FILE = "btc_hourly_data.csv"


@st.cache_data(ttl=3600)
def fetch_data():
    df = yf.download("BTC-USD", period="1mo", interval="1h", auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.index.name = "Datetime"
    df.to_csv(DATA_FILE)
    return df


def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, index_col="Datetime", parse_dates=True)
    else:
        df = fetch_data()
    return df


def fmt(val, prefix="$", decimals=2):
    try:
        return f"{prefix}{val:,.{decimals}f}"
    except Exception:
        return str(val)


def main():
    st.set_page_config(page_title="BTC Dashboard", layout="wide")

    st.title("Bitcoin (BTC-USD) Price Dashboard")
    st.caption("1 month of hourly OHLCV data via yfinance")

    if st.button("Refresh Data"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        fetch_data.clear()
        st.rerun()

    with st.spinner("Loading BTC data..."):
        df = load_data()

    if df.empty:
        st.error("No data available. Try refreshing.")
        return

    df["MA20"] = df["Close"].rolling(window=20).mean()

    latest = float(df["Close"].iloc[-1])
    open_price = float(df["Close"].iloc[0])
    change_pct = ((latest - open_price) / open_price) * 100

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Current Price", f"${latest:,.2f}", f"{change_pct:+.2f}%")
    m2.metric("1M High", f"${float(df['High'].max()):,.2f}")
    m3.metric("1M Low", f"${float(df['Low'].min()):,.2f}")
    m4.metric("Avg Volume", f"{float(df['Volume'].mean()):,.0f}")

    st.divider()

    st.subheader("Price Chart — Close & 20-Period Moving Average")
    chart_df = df[["Close", "MA20"]].rename(
        columns={"Close": "Close Price", "MA20": "MA (20)"}
    )
    st.line_chart(chart_df, height=400)

    st.divider()

    st.subheader("Raw Hourly Data (most recent 200 rows)")
    display_cols = ["Open", "High", "Low", "Close", "Volume", "MA20"]
    raw = df[display_cols].tail(200).sort_index(ascending=False).copy()

    formatted = pd.DataFrame(index=raw.index)
    formatted["Open"] = raw["Open"].apply(lambda x: fmt(x))
    formatted["High"] = raw["High"].apply(lambda x: fmt(x))
    formatted["Low"] = raw["Low"].apply(lambda x: fmt(x))
    formatted["Close"] = raw["Close"].apply(lambda x: fmt(x))
    formatted["Volume"] = raw["Volume"].apply(lambda x: fmt(x, prefix="", decimals=0))
    formatted["MA20"] = raw["MA20"].apply(lambda x: fmt(x) if pd.notna(x) else "-")

    st.dataframe(formatted, use_container_width=True, height=400)

    st.divider()

    st.subheader("Summary Statistics — Close Price")
    stats = df["Close"].describe()
    label_map = {
        "count": "Count", "mean": "Mean", "std": "Std Dev",
        "min": "Min", "25%": "25th Pct", "50%": "Median",
        "75%": "75th Pct", "max": "Max",
    }
    stats_df = pd.DataFrame({
        "Statistic": [label_map.get(k, k) for k in stats.index],
        "Value": [
            f"{v:,.0f}" if k == "count" else f"${v:,.2f}"
            for k, v in zip(stats.index, stats.values)
        ],
    })
    st.table(stats_df)

    st.caption(
        f"Data cached in `{DATA_FILE}` for 1 hour. "
        f"Click **Refresh Data** to re-fetch live prices."
    )


if __name__ == "__main__":
    main()
