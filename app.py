
import streamlit as st
import pandas as pd

# Set default theme
st.set_page_config(page_title="BigBoy FX V2", layout="wide")

# Theme toggle
theme = st.sidebar.radio("🎨 Theme", ["🌙 Dark Mode", "☀️ Light Mode"])

if theme == "🌙 Dark Mode":
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0f0f0f;
            color: #e1e1e1;
        }
        .css-1d391kg {
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #ffffff;
            color: #111111;
        }
        </style>
    """, unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align:center;'>📊 BigBoy FX V2 – Live Dashboard</h1>", unsafe_allow_html=True)

# Live data section
sheet_id = "1abOo_P076bgURio56_5EEd3WCcwkoNuYk4bWwV69Azg"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=LIVE_FEED"

try:
    df = pd.read_csv(csv_url)

    # Watchlist Selector
    section = st.sidebar.selectbox("📌 Watchlist", ["All", "USD Majors", "JPY Pairs"])

    if section == "USD Majors":
        df = df[df["PAIR"].str.contains("USD")]
    elif section == "JPY Pairs":
        df = df[df["PAIR"].str.contains("JPY")]

    st.dataframe(df, use_container_width=True)

    st.markdown(f"<div style='text-align:right; font-size: 0.9em;'>⏱ Updated: {df['UPDATED_TIME'].max()}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error("❌ Failed to load data.")
    st.text(str(e))

# TradingView embed
st.markdown("---")
st.subheader("📈 TradingView Live Chart")

pair = st.selectbox("Select Pair", ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"])
tv_code = f'''
<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{pair}&symbol=FX:{pair}&interval=60&hidesidetoolbar=1&symboledit=1&saveimage=0&toolbarbg=f1f3f6&studies=[]&theme={'dark' if 'Dark' in theme else 'light'}&style=1&timezone=Etc/UTC&withdateranges=1&hideideas=1" 
width="100%" height="450" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen></iframe>
'''
st.components.v1.html(tv_code, height=450)
