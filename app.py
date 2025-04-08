
import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="BigBoy FX Dashboard", layout="wide")

# Dark theme header
st.markdown("""
    <style>
    body, .stApp {
        background-color: #111111;
        color: #e1e1e1;
    }
    .css-1d391kg {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color:#00ffcc;'>📈 BigBoy Live Forex Dashboard</h1>", unsafe_allow_html=True)

# Auto-refresh interval (in seconds)
REFRESH_INTERVAL = 60
st.markdown(f"<div style='text-align:right; font-size: 0.9em;'>🔄 Auto-refresh every {REFRESH_INTERVAL} seconds</div>", unsafe_allow_html=True)

# Load from Google Sheet CSV export
sheet_id = "1abOo_P076bgURio56_5EEd3WCcwkoNuYk4bWwV69Azg"
sheet_name = "LIVE_FEED"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

try:
    df = pd.read_csv(csv_url)

    # Optional signal flag logic (demo)
    signal_flags = []
    for index, row in df.iterrows():
        price = float(row["PRICE"])
        if "JPY" in row["PAIR"] and price > 150:
            signal_flags.append("⚠️ High JPY Zone")
        elif "USD" in row["PAIR"] and price < 1:
            signal_flags.append("🔻 Below Parity")
        else:
            signal_flags.append("✅ Stable")

    df["SIGNAL"] = signal_flags

    # Format and display
    st.success("✅ Live data loaded successfully!")

    def color_signal(val):
        if "⚠️" in val:
            return "background-color: #331111; color: #ff4444"
        elif "🔻" in val:
            return "background-color: #333300; color: #ffff66"
        elif "✅" in val:
            return "background-color: #112211; color: #66ff66"
        return ""

    df_display = df.style.applymap(color_signal, subset=["SIGNAL"])

    st.dataframe(df_display, use_container_width=True)

    # Last updated info
    last_update = df["UPDATED_TIME"].max()
    st.markdown(f"<div style='text-align:right; font-size: 0.9em;'>⏱ Last Updated: {last_update}</div>", unsafe_allow_html=True)

    # Refresh delay
    time.sleep(REFRESH_INTERVAL)
    st.experimental_rerun()

except Exception as e:
    st.error("❌ Failed to load data.")
    st.text(str(e))
