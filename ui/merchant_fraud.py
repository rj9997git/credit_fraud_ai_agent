import streamlit as st
from agent import analyze_as_fraud_analyst

def render(df):
    st.markdown("### Merchant Fraud Rates")
    st.write("Analyze which merchants have the highest fraud rates.")
    if st.button("Analyze Merchant Fraud Rates", key="mf_button"):
        summary = df.groupby('merchant').agg(
            total_txn=('transaction_id', 'count'),
            fraud_txn=('is_fraud', 'sum'),
            fraud_rate=('is_fraud', 'mean'),
            avg_amount=('amount', 'mean'),
            avg_risk_score=('risk_score', 'mean')
        ).sort_values('fraud_rate', ascending=False)
        summary['fraud_rate_pct'] = summary['fraud_rate'].map('{:.2%}'.format)
        st.dataframe(summary, use_container_width=True)
        analysis = analyze_as_fraud_analyst("merchant_fraud_rate", {}, summary)
        st.info(analysis)