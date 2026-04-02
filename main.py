from fastapi import FastAPI
import pandas as pd
import joblib
import os
from sqlalchemy import create_engine

app = FastAPI()

# -----------------------------
# PATH FIX (IMPORTANT)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# LOAD MODEL
# -----------------------------
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
le = joblib.load(os.path.join(BASE_DIR, "label_encoder.pkl"))

print(" Model Loaded")

# -----------------------------
# DB CONNECTION
# -----------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:Kovilvenni@localhost:5432/banking_db"
)

print(" DB Connected")

# -----------------------------
# HOME API
# -----------------------------
@app.get("/")
def home():
    return {"message": "API Running Successfully"}


# -----------------------------
# CUSTOMER DATA API
# -----------------------------
@app.get("/customer/{customer_id}")
def get_customer(customer_id: str):

    try:
        df = pd.read_sql(
            f"SELECT * FROM features WHERE customer_id='{customer_id}'",
            engine
        )

        if df.empty:
            return {"error": "Customer not found"}

        row = df.iloc[0]

        # -----------------------------
        # CLEAN RESPONSE
        # -----------------------------
        response = {
            "customer_id": customer_id,

            "profile": {
                "avg_balance": round(row["avg_monthly_balance"], 2),
                "monthly_spend": round(row["monthly_spend"], 2),
                "risk_score": round(row["risk_score"], 2)
            },

            "behavior": {
                "debit_credit_ratio": round(row["debit_credit_ratio"], 2),
                "emi_ratio": round(row["emi_spend_ratio"], 2),
                "cash_ratio": round(row["cash_withdrawal_ratio"], 2)
            },

            "top_spending_categories": {
                "shopping": round(row["ONLINE_SHOPPING"], 2),
                "groceries": round(row["GROCERIES"], 2),
                "fuel": round(row["FUEL"], 2),
                "others": round(row["OTHER"], 2)
            },

            "model_info": {
                "predicted_product": row["product_label"],
                "confidence": round(row["recommendation_score"], 2),
                "reason": row["recommendation_reason"]
            }
        }

        return response

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/recommend/{customer_id}")
def recommend(customer_id: str):

    try:
        df = pd.read_sql(
            f"SELECT * FROM features WHERE customer_id='{customer_id}'",
            engine
        )

        if df.empty:
            return {"error": "Customer not found"}

        row = df.iloc[0]

        # -----------------------------
        # RESPONSE
        # -----------------------------
        return {
            "customer_id": customer_id,
            "recommendations": [
                {
                    "product": row["product_label"],
                    "score": round(row["recommendation_score"], 2),
                    "rank": 1,
                    "reason": row["recommendation_reason"]
                }
            ]
        }

    except Exception as e:
        return {"error": str(e)}    