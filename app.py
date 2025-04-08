
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BigBoy FX Dashboard", layout="wide")
st.title("📈 BigBoy Live Forex Dashboard")

sheet_id = "1pZ10U5hvZRFXLLfhKxo6V8SsuajH6Yygi47NJsrI9HU"
sheet_name = "LIVE_FEED"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

try:
    df = pd.read_csv(csv_url)
    st.success("Live data loaded successfully!")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error("Failed to load data. Make sure your sheet is published or shared correctly.")
    st.text(str(e))
