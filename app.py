import streamlit as st
import pandas as pd
from src.config import PROCESSED_DIR

st.set_page_config(page_title="Smart E-Commerce AI", page_icon="🛍️", layout="wide")
st.title("Smart E-Commerce AI")
st.caption("Historical analysis of the English-language DataCo Smart Supply Chain dataset")
st.info("Run data preparation and training using the commands in README.md. The dashboard reads only locally generated data and model artifacts.")
st.warning("DataCo records cover 2015–2018; results describe observed historical data and do not forecast current market conditions.")
orders_path=PROCESSED_DIR/"orders_one_row.parquet"
if orders_path.exists():
    orders=pd.read_parquet(orders_path); items=pd.read_parquet(PROCESSED_DIR/"order_items_enriched.parquet")
    c1,c2,c3=st.columns(3); c1.metric("Orders",f"{orders.order_id.nunique():,}"); c2.metric("Order items",f"{len(items):,}"); c3.metric("Booked item value",f"{items.price.sum():,.2f} (dataset units)")
    dates=pd.to_datetime(orders.order_purchase_timestamp,errors="coerce"); st.caption(f"Observed purchase period: {dates.min():%Y-%m-%d} to {dates.max():%Y-%m-%d}. Value is the DataCo Order Item Total; no currency is assumed.")
    st.subheader("Weekly item value"); weekly=pd.read_parquet(PROCESSED_DIR/"weekly_revenue.parquet").set_index("week_start"); target="revenue_value" if "revenue_value" in weekly else "revenue_brl"; st.line_chart(weekly[[target]])
else:
    st.error("Real DataCo data is not prepared yet. The dataset was not replaced with synthetic examples.")
    st.code("Copy DataCoSupplyChainDataset.csv to data/raw/\npython scripts/validate_data.py\npython scripts/prepare_data.py\npython scripts/train_all.py --mode full")
