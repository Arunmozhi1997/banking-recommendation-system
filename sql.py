import pandas as pd
import os
from sqlalchemy import create_engine

# -----------------------------
# CHECK PATH
# -----------------------------
print("Current Path:", os.getcwd())

# -----------------------------
# DB CONNECTION
# -----------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:Kovilvenni@localhost:5432/banking_db"
)

# -----------------------------
# LOAD CSV (FULL PATH)
# -----------------------------
customers_df = pd.read_csv(r"C:\Users\HP\axis_ml\venv\Scripts\customers.csv")
accounts_df = pd.read_csv(r"C:\Users\HP\axis_ml\venv\Scripts\accounts.csv")
transactions_df = pd.read_csv(r"C:\Users\HP\axis_ml\venv\Scripts\transactions.csv")
features_df = pd.read_csv(r"C:\Users\HP\axis_ml\venv\Scripts\features.csv")
product_catalog = pd.read_csv(r"C:\Users\HP\axis_ml\venv\Scripts\product_catalog.csv")
recommendations_df = pd.read_csv(r"C:\Users\HP\axis_ml\venv\Scripts\recommendations.csv")
model_metadata_df = pd.read_csv(r"C:\Users\HP\axis_ml\venv\Scripts\model_metadata.csv")

print("✅ All CSV loaded successfully")

# -----------------------------
# UPLOAD
# -----------------------------
customers_df.to_sql("customers", engine, if_exists="append", index=False)
accounts_df.to_sql("accounts", engine, if_exists="append", index=False)
transactions_df.to_sql("transactions", engine, if_exists="append", index=False)
features_df.to_sql("features", engine, if_exists="append", index=False)
product_catalog.to_sql("product_catalog", engine, if_exists="append", index=False)
recommendations_df.to_sql("recommendations", engine, if_exists="append", index=False)
model_metadata_df.to_sql("model_metadata", engine, if_exists="append", index=False)

print("🎉 ALL TABLES LOADED")