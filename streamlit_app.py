import streamlit as st
import requests
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Axis Product Recommendation Dashboard",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (BANK UI)
# -----------------------------
st.markdown("""
<style>
.card {
    background-color: #1e2a3a;
    color: #f0f4f8;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #2e3f55;
    margin-bottom: 15px;
}
.card h3 {
    color: #63b3ed;
    margin-top: 0;
}
.card p {
    color: #e2e8f0;
    margin: 6px 0;
}
.title {
    font-size: 30px;
    font-weight: bold;
}
.sub {
    font-size: 16px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DB CONNECTION
# -----------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:Kovilvenni@localhost:5432/banking_db"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<p class="title"> Smart Banking Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub">AI-powered customer insights & recommendations</p>', unsafe_allow_html=True)

# -----------------------------
# INPUT
# -----------------------------
customer_id = st.text_input(" Enter Customer ID")


# -----------------------------
# MAIN ACTION
# -----------------------------
if st.button(" Analyze Customer"):

    # -----------------------------
    # CALL CUSTOMER API
    # -----------------------------
    customer_api = requests.get(
        f"http://127.0.0.1:8000/customer/{customer_id}"
    )

    data = customer_api.json()

    if "error" in data:
        st.error(data["error"])

    else:
        # -----------------------------
        # PROFILE SECTION
        # -----------------------------
        st.markdown("## 👤 Customer Profile")

        col1, col2, col3 = st.columns(3)

        col1.metric(" Avg Balance", f"₹ {data['profile']['avg_balance']:,}")
        col2.metric(" Monthly Spend", f"₹ {data['profile']['monthly_spend']:,}")
        col3.metric(" Risk Score", data['profile']['risk_score'])

        st.divider()

        # -----------------------------
        # BEHAVIOR SECTION
        # -----------------------------
        st.markdown("##  Behavior Insights")

        col4, col5, col6 = st.columns(3)

        col4.metric("Debit/Credit", data['behavior']['debit_credit_ratio'])
        col5.metric("EMI Ratio", data['behavior']['emi_ratio'])
        col6.metric("Cash Usage", data['behavior']['cash_ratio'])

        st.divider()

        # -----------------------------
        # SPENDING CHART
        # -----------------------------
        st.markdown("##  Spending Distribution")

        spend_dict = data["top_spending_categories"]

        spend_df = pd.DataFrame({
            "Category": list(spend_dict.keys()),
            "Value": list(spend_dict.values())
        })

        fig = px.pie(
            spend_df,
            names="Category",
            values="Value",
            title="Spending Breakdown"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # -----------------------------
        # RECOMMENDATION API
        # -----------------------------
        rec_api = requests.get(
            f"http://127.0.0.1:8000/recommend/{customer_id}"
        )

        rec_data = rec_api.json()

        # -----------------------------
        # RECOMMENDATION SECTION
        # -----------------------------
        st.markdown("##  Recommended Products")

        if "recommendations" in rec_data:

            for rec in rec_data["recommendations"]:

                st.markdown(f"""
                <div class="card">
                    <h3> {rec['product']}</h3>
                    <p><b> Score:</b> {rec['score']:.2f}</p>
                    <p><b> Rank:</b> {rec['rank']}</p>
                    <p><b> Reason:</b> {rec.get('reason','Behavior-based recommendation')}</p>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("No recommendations found")