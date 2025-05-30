import streamlit as st
from load_data import load_from_db
from feature_engineering import add_features
from ui.dashboard import render as render_dashboard
from ui.high_value import render as render_high_value
from ui.inactivity import render as render_inactivity
from ui.merchant_fraud import render as render_merchant_fraud
from ui.custom_query import render as render_custom_query

st.set_page_config(page_title="Credit Card Fraud AI Agent", page_icon="💳", layout="wide")
st.title("💳 Credit Card Fraud AI Agent")
st.write("This app demonstrates how an AI agent can analyze transaction data like a fraud analyst.")

@st.cache_resource
def initialize_data():
    df = load_from_db()
    if df.empty:
        st.error("Failed to load data from the database. Please check your DB connection and credentials.")
    else:
        df = add_features(df)
    return df

with st.spinner("Loading data..."):
    df = initialize_data()

if not df.empty:
    with st.expander("View Sample Data"):
        st.dataframe(df.head(10), use_container_width=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Dashboard",
        "High-Value Transactions",
        "Activity After Inactivity",
        "Merchant Fraud Rates",
        "Custom Query"
    ])

    with tab1:
        render_dashboard(df)
    with tab2:
        render_high_value(df)
    with tab3:
        render_inactivity(df)
    with tab4:
        render_merchant_fraud(df)
    with tab5:
        render_custom_query(df)

    st.markdown("---")
    st.markdown("💳 Credit Card Fraud AI Agent | Built with Streamlit, Pandas, and OpenAI")