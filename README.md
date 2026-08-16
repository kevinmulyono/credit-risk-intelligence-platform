# Credit Risk Intelligence Platform

Aplikasi end-to-end untuk menganalisis dan memprediksi risiko kredit customer, dibangun dengan pendekatan production-grade data pipeline — bukan sekadar notebook machine learning.

## Business Problem

Sebuah bank menerima ribuan pengajuan pinjaman setiap hari. Platform ini membantu menjawab:

- Seberapa besar risiko seorang customer akan gagal bayar (default)?
- Faktor apa yang paling mempengaruhi risiko tersebut?
- Segmen customer mana yang punya default rate tertinggi?
- Apa rekomendasi keputusan bisnis (approve / manual review / reject) untuk sebuah pengajuan?

## Dataset

[Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk) (Kaggle) — 8 file CSV relasional, terdiri dari data aplikasi pinjaman, histori kredit di bank lain (bureau), dan histori pinjaman sebelumnya di Home Credit (kartu kredit, cicilan, POS/cash loan).

## Arsitektur

```
CSV (8 files)
    ↓  Python (Pandas + SQLAlchemy)
PostgreSQL — Raw Tables (8 tabel)
    ↓  SQL Views (agregasi & join)
SQL Views (6 views: vw_credit_risk, vw_customer_summary,
           vw_pos_cash_agg, vw_installments_agg,
           vw_credit_card_agg, vw_bureau_balance_agg)
    ↓
feature_table (PostgreSQL, gabungan semua view + fitur turunan)
    ↓  Python (missing value handling + encoding)
feature_table_final (CSV + PostgreSQL, 307,507 baris × 100 kolom)
    ↓
Machine Learning (Logistic Regression → LightGBM)
    ↓  SHAP (native LightGBM TreeSHAP)
Model Interpretability
    ↓
FastAPI (/predict endpoint)
    ↓
Streamlit Dashboard (4 halaman)
```

## Tech Stack

| Kategori | Tools |
|---|---|
| Bahasa | Python |
| Database | PostgreSQL |
| Data Access | SQL, SQLAlchemy, psycopg2 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, LightGBM |
| Model Interpretability | Native LightGBM TreeSHAP |
| API | FastAPI |
| Dashboard | Streamlit |
| Tools | Git, GitHub, VS Code, DBeaver |

## Struktur Project

```
credit-risk-intelligence-platform/
│
├── data/
│   ├── raw/                    # CSV asli dari Kaggle
│   ├── processed/               # feature_table_final.csv, data_profile.csv
│   └── models/                  # model .pkl hasil training
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda_from_database.ipynb
│   ├── 03_missing_value_encoding.ipynb
│   └── 04_baseline_model.ipynb
│
├── sql/
│   ├── schema.sql                # dokumentasi struktur database
│   ├── vw_credit_risk.sql
│   ├── vw_customer_summary.sql
│   ├── vw_behavior_agg.sql
│   └── business_analysis.sql     # query analisis bisnis
│
├── src/
│   ├── database/
│   │   ├── load_data.py          # ETL: CSV -> PostgreSQL raw tables
│   │   └── validate_import.py    # validasi row count CSV vs DB
│   ├── etl/
│   │   └── build_feature_table.py # build feature_table dari SQL views
│   ├── analysis/
│   │   └── queries.py             # reusable business analysis queries
│   ├── models/
│   │   └── predict.py             # scoring function (model + SHAP)
│   ├── api/
│   │   └── main.py                # FastAPI app (/predict endpoint)
│   └── dashboard/
│       ├── app.py                 # halaman utama Streamlit
│       └── pages/
│           ├── 1_Executive_Dashboard.py
│           ├── 2_Business_Analytics.py
│           ├── 3_ML_Prediction.py
│           └── 4_Decision_Support_System.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Hasil Utama

- **Model**: LightGBM, AUC Score **0.7783** (baseline Logistic Regression: 0.7628)
- **Fitur paling berpengaruh**: `EXT_SOURCE_3`, `age_years`, `EXT_SOURCE_2`, `EXT_SOURCE_1` — konsisten antara korelasi SQL, feature importance model, dan SHAP values
- **Insight bisnis**: kepemilikan aset (rumah/mobil) berkorelasi dengan default rate yang lebih rendah; pendidikan dan kelompok usia menunjukkan pola risiko yang jelas

## Cara Menjalankan Project

### 1. Clone repository

```bash
git clone <repo-url>
cd credit-risk-intelligence-platform
```

### 2. Setup virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### 3. Setup PostgreSQL

- Buat database baru bernama `credit_risk_db`
- Copy `.env.example` menjadi `.env`, isi dengan kredensial PostgreSQL kamu

```bash
cp .env.example .env
```

### 4. Download dataset

Download dataset [Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk) dari Kaggle, letakkan seluruh file CSV di folder `data/raw/`.

### 5. Jalankan ETL — Import CSV ke PostgreSQL

```bash
python src/database/load_data.py
python -m src.database.validate_import
```

### 6. Buat SQL Views

Jalankan file-file berikut secara berurutan di PostgreSQL (via DBeaver atau `psql`):

```
sql/vw_credit_risk.sql
sql/vw_customer_summary.sql
sql/vw_behavior_agg.sql
```

### 7. Build feature table

```bash
python -m src.etl.build_feature_table
```

### 8. Jalankan notebook missing value handling & encoding

Buka dan jalankan `notebooks/03_missing_value_encoding.ipynb` secara berurutan. Notebook ini akan menghasilkan `data/processed/feature_table_final.csv` dan tabel `feature_table_final` di PostgreSQL.

### 9. Training model

Buka dan jalankan `notebooks/04_baseline_model.ipynb` secara berurutan. Notebook ini akan menyimpan model final ke `data/models/credit_risk_model.pkl`.

### 10. Jalankan FastAPI

```bash
uvicorn src.api.main:app --reload
```

API akan berjalan di `http://127.0.0.1:8000`. Dokumentasi interaktif tersedia di `http://127.0.0.1:8000/docs`.

### 11. Jalankan Streamlit Dashboard

Buka terminal baru (biarkan FastAPI tetap berjalan di terminal sebelumnya):

```bash
streamlit run src/dashboard/app.py
```

Dashboard akan berjalan di `http://localhost:8501`.

## Halaman Dashboard

| Halaman | Deskripsi |
|---|---|
| **Executive Dashboard** | KPI utama: total customer, default rate, rata-rata income & kredit, distribusi pinjaman |
| **Business Analytics** | Analisis default rate berdasarkan pendidikan, pekerjaan, income group, usia, dan korelasi fitur |
| **ML Prediction** | Form input customer baru, menghasilkan prediksi probabilitas default via FastAPI |
| **Decision Support System** | Penjelasan naratif hasil prediksi (risk score, faktor kontribusi, rekomendasi approve/review/reject) |

## Catatan

- Model dilatih dengan `class_weight`/`scale_pos_weight` untuk menangani ketidakseimbangan kelas (TARGET: 282,686 non-default vs 24,825 default)
- Prediksi untuk customer tanpa histori kredit (bureau, kartu kredit, cicilan sebelumnya) akan memperlakukan fitur histori tersebut sebagai 0, yang dapat mempengaruhi akurasi untuk customer benar-benar baru
- File model (`.pkl`) tidak disertakan di repository — jalankan notebook training untuk menghasilkannya secara lokal