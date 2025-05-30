import streamlit as st
from agent import analyze_as_fraud_analyst

def render(df):
    st.markdown("### Custom Query")
    st.write("Ask a specific question about the transaction data.")
    query = st.text_area(
        "Type your question (e.g., 'Show transactions over $1000 in the US with high risk scores')",
        height=100,
        key="cq_query"
    )
    if st.button("Run Custom Query", key="cq_button") and query.strip():
        filtered = df[
            (df['risk_score'] > 70) &
            (df['amount'] > 1000)
        ].sort_values('risk_score', ascending=False)
        st.success(f"Found {len(filtered)} transactions matching your query")
        st.dataframe(filtered.head(20), use_container_width=True)
        params = {'query': query}
        analysis = analyze_as_fraud_analyst("custom_query", params, filtered)
        st.info(analysis)