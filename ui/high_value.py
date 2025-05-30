import streamlit as st
from agent import analyze_as_fraud_analyst

def render(df):
    st.markdown("### Find High-Value Transactions")
    st.write("Identify transactions above a certain amount in a specific country.")
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Country", sorted(df['location'].unique()), key="hv_country")
    with col2:
        amount = st.number_input("Minimum transaction amount ($)", 100, 10000, 1000, 100, key="hv_amount")
    if st.button("Analyze High-Value Transactions", key="hv_button"):
        filtered = df[(df['location'] == country) & (df['amount'] > amount)]
        if filtered.empty:
            st.warning(f"No transactions found over ${amount} in {country}")
        else:
            st.success(f"Found {len(filtered)} transactions over ${amount} in {country}")
            st.dataframe(filtered.sort_values('amount', ascending=False), use_container_width=True)
            params = {'country': country, 'amount': amount}
            analysis = analyze_as_fraud_analyst("high_value_transactions", params, filtered)
            st.info(analysis)