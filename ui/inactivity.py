import streamlit as st
from agent import analyze_as_fraud_analyst

def render(df):
    st.markdown("### Find Activity After Inactivity")
    st.write("Identify transactions that occur after a period of inactivity.")
    col1, col2 = st.columns(2)
    with col1:
        inactivity_hours = st.slider("Minimum hours of inactivity", 1, 240, 48, 1, key="ia_hours")
    with col2:
        multiplier = st.slider("Amount increase multiplier", 1.5, 10.0, 3.0, 0.5, key="ia_multiplier")
    if st.button("Analyze Activity After Inactivity", key="ia_button"):
        suspicious = df[
            (df['time_since_last'] > inactivity_hours) &
            (df['amount'] > multiplier * df['rolling_avg_amount'])
        ]
        if suspicious.empty:
            st.warning(f"No suspicious activity found with these parameters")
        else:
            st.success(f"Found {len(suspicious)} suspicious transactions")
            st.dataframe(suspicious.sort_values('time_since_last', ascending=False), use_container_width=True)
            params = {'hours': inactivity_hours, 'multiplier': multiplier}
            analysis = analyze_as_fraud_analyst("activity_after_inactivity", params, suspicious)
            st.info(analysis)