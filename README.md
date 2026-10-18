# 🏦 AI-Powered Banking Product Recommendation System

An end-to-end machine learning system that reads customers' bank statements, builds a behavioural profile for each customer and recommends the **two best-fit banking products**, each with a confidence score and a plain-language reason.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![XGBoost](https://img.shields.io/badge/XGBoost-1A73E8) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)

🎥 **[Watch the demo video](Screen%20Recording%202026-04-12%20185503.mp4)**

## 📊 Results

| Metric | Value |
|---|---|
| Test accuracy | **90%** |
| Weighted F1-score (test) | **0.91** |
| Train accuracy | 94% |
| Transactions processed | 1M+ from 1,000 bank statement PDFs |
| Products predicted | 4 |

## 🧠 How it works

```
Bank statement PDFs ──► ETL (PyMuPDF + regex) ──► 1M+ transactions in 24 spending categories
        │
        ▼
Feature engineering (20+ features per customer: monthly spend, EMI ratio,
debit-credit ratio, cash withdrawal ratio, weighted risk score)
        │
        ▼
XGBoost classifier (class-balanced weights) ──► top-2 products + confidence + reason
        │
        ▼
FastAPI REST API  ◄──►  PostgreSQL (7 tables)  ◄──►  Streamlit dashboard
```

## 📁 Project structure

| File | Purpose |
|---|---|
| `axis_ml.ipynb` | PDF parsing, ETL, feature engineering, model training and evaluation |
| `sql.py` | Loads the processed CSVs into PostgreSQL |
| `main.py` | FastAPI backend (`/customer/{id}`, `/recommend/{id}`) |
| `streamlit_app.py` | Interactive dashboard |

## ⚙️ Run it locally

```bash
git clone https://github.com/Arunmozhi1997/banking-recommendation-system.git
cd banking-recommendation-system
pip install -r requirements.txt

# 1. Tell the app how to reach your PostgreSQL database (PowerShell example)
$env:DATABASE_URL="postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/banking_db"

# 2. Run axis_ml.ipynb to generate the CSVs (into data/) and model.pkl / label_encoder.pkl
# 3. Load the data into PostgreSQL
python sql.py

# 4. Start the API and the dashboard (two terminals)
uvicorn main:app --reload
streamlit run streamlit_app.py
```

> The raw bank statements, generated CSVs and trained model files are not committed to keep the repository small. Running the notebook recreates them.

## 👤 Author

**Arunmozhi M** · [Portfolio](https://arunmozhi1997.github.io) · [LinkedIn](https://linkedin.com/in/arunmozhi-m-65a29037b)
