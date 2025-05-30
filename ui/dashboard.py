import streamlit as st

def render(df):
    st.markdown("### Dashboard")
    st.write("Overview of transaction data and fraud patterns")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Transactions", f"{len(df):,}")
    with col2:
        st.metric("Fraud Transactions", f"{df['is_fraud'].sum():,}")
    with col3:
        st.metric("Fraud Rate", f"{df['is_fraud'].mean() * 100:.2f}%")
    with col4:
        st.metric("Avg Transaction", f"${df['amount'].mean():.2f}")
    st.dataframe(df.sample(10), use_container_width=True)