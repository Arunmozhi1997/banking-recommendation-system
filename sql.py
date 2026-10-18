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
engine = create_engine(os.getenv("DATABASE_URL"))

# -----------------------------
# LOAD CSV (FULL PATH)
# -----------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

customers_df = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
accounts_df = pd.read_csv(os.path.join(DATA_DIR, "accounts.csv"))
transactions_df = pd.read_csv(os.path.join(DATA_DIR, "transactions.csv"))
features_df = pd.read_csv(os.path.join(DATA_DIR, "features.csv"))
product_catalog = pd.read_csv(os.path.join(DATA_DIR, "product_catalog.csv"))
recommendations_df = pd.read_csv(os.path.join(DATA_DIR, "recommendations.csv"))
model_metadata_df = pd.read_csv(os.path.join(DATA_DIR, "model_metadata.csv"))

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
