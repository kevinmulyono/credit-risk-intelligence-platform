from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from sqlalchemy import text

from src.models.predict import predict_credit_risk
from src.database.load_data import engine

app = FastAPI(
    title="Credit Risk Intelligence Platform API",
    description="API untuk prediksi risiko kredit dan decision support system",
    version="1.0.0"
)

# ============================================================
# CORS — izinkan Next.js (localhost:3000) mengakses API
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Schema
# ============================================================
class CustomerInput(BaseModel):
    """
    Input schema untuk prediksi risiko kredit.
    Semua field opsional -> kalau tidak dikirim, akan diisi 0 secara otomatis
    (aman untuk kolom hasil one-hot encoding).
    """
    AMT_INCOME_TOTAL: Optional[float] = None
    AMT_CREDIT: Optional[float] = None
    AMT_ANNUITY: Optional[float] = None
    AMT_GOODS_PRICE: Optional[float] = None
    age_years: Optional[float] = None
    employment_years: Optional[float] = None
    CNT_CHILDREN: Optional[float] = None
    CNT_FAM_MEMBERS: Optional[float] = None
    EXT_SOURCE_1: Optional[float] = None
    EXT_SOURCE_2: Optional[float] = None
    EXT_SOURCE_3: Optional[float] = None
    CODE_GENDER: Optional[int] = None
    FLAG_OWN_CAR: Optional[int] = None
    FLAG_OWN_REALTY: Optional[int] = None

    class Config:
        extra = "allow"  # izinkan kirim kolom lain di luar yang didefinisikan di atas


class PredictionResponse(BaseModel):
    probability: float
    risk_category: str
    recommendation: str
    top_factors: list


# ============================================================
# Core Endpoints
# ============================================================
@app.get("/")
def root():
    return {
        "message": "Credit Risk Intelligence Platform API is running.",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerInput):
    try:
        input_dict = customer.dict(exclude_none=True)
        result = predict_credit_risk(input_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Analytics Endpoints (untuk Next.js Dashboard)
# ============================================================

def _query(sql: str) -> list:
    """Helper: jalankan SQL query dan kembalikan sebagai list of dict."""
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        cols = result.keys()
        return [dict(zip(cols, row)) for row in rows]


@app.get("/analytics/kpi")
def get_kpi():
    """KPI utama untuk Executive Dashboard."""
    try:
        data = _query("""
            SELECT
                COUNT(*)                                        AS total_customer,
                SUM("TARGET")                                   AS total_default,
                ROUND(AVG("TARGET")::NUMERIC * 100, 2)          AS default_rate_pct,
                ROUND(AVG("AMT_INCOME_TOTAL")::NUMERIC, 0)      AS avg_income,
                ROUND(AVG("AMT_CREDIT")::NUMERIC, 0)            AS avg_credit
            FROM vw_credit_risk
        """)
        return data[0] if data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/loan-distribution")
def get_loan_distribution():
    """Distribusi jumlah pinjaman per bucket."""
    try:
        return _query("""
            SELECT
                CASE
                    WHEN "AMT_CREDIT" < 300000 THEN '< 300K'
                    WHEN "AMT_CREDIT" < 600000 THEN '300K - 600K'
                    WHEN "AMT_CREDIT" < 900000 THEN '600K - 900K'
                    ELSE '> 900K'
                END AS credit_group,
                COUNT(*) AS total_customer
            FROM vw_credit_risk
            GROUP BY credit_group
            ORDER BY credit_group
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/risk-distribution")
def get_risk_distribution():
    """Distribusi kategori risiko berdasarkan EXT_SOURCE_3."""
    try:
        return _query("""
            SELECT
                CASE
                    WHEN "EXT_SOURCE_3" IS NULL THEN 'Unknown'
                    WHEN "EXT_SOURCE_3" >= 0.6 THEN 'Low Risk'
                    WHEN "EXT_SOURCE_3" >= 0.3 THEN 'Medium Risk'
                    ELSE 'High Risk'
                END AS risk_category,
                COUNT(*) AS total_customer
            FROM vw_credit_risk
            GROUP BY risk_category
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/default-by-education")
def get_default_by_education():
    """Default rate berdasarkan tingkat pendidikan."""
    try:
        return _query("""
            SELECT
                "NAME_EDUCATION_TYPE",
                COUNT(*)                                   AS total_customer,
                SUM("TARGET")                              AS total_default,
                ROUND(AVG("TARGET")::NUMERIC * 100, 2)     AS default_rate_pct
            FROM vw_credit_risk
            GROUP BY "NAME_EDUCATION_TYPE"
            ORDER BY default_rate_pct DESC
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/default-by-occupation")
def get_default_by_occupation():
    """Default rate berdasarkan jenis pekerjaan."""
    try:
        return _query("""
            SELECT
                "OCCUPATION_TYPE",
                COUNT(*)                                   AS total_customer,
                SUM("TARGET")                              AS total_default,
                ROUND(AVG("TARGET")::NUMERIC * 100, 2)     AS default_rate_pct
            FROM vw_credit_risk
            WHERE "OCCUPATION_TYPE" IS NOT NULL
            GROUP BY "OCCUPATION_TYPE"
            ORDER BY default_rate_pct DESC
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/default-by-income-group")
def get_default_by_income_group():
    """Default rate berdasarkan kelompok pendapatan."""
    try:
        return _query("""
            SELECT
                CASE
                    WHEN "AMT_INCOME_TOTAL" < 100000 THEN '1. < 100K'
                    WHEN "AMT_INCOME_TOTAL" < 200000 THEN '2. 100K-200K'
                    WHEN "AMT_INCOME_TOTAL" < 300000 THEN '3. 200K-300K'
                    WHEN "AMT_INCOME_TOTAL" < 500000 THEN '4. 300K-500K'
                    ELSE '5. > 500K'
                END AS income_group,
                COUNT(*) AS total_customer,
                ROUND(AVG("TARGET")::NUMERIC * 100, 2) AS default_rate_pct
            FROM vw_credit_risk
            GROUP BY income_group
            ORDER BY income_group
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/default-by-age-group")
def get_default_by_age_group():
    """Default rate berdasarkan kelompok usia."""
    try:
        return _query("""
            SELECT
                CASE
                    WHEN age_years < 25 THEN '< 25'
                    WHEN age_years < 35 THEN '25-34'
                    WHEN age_years < 45 THEN '35-44'
                    WHEN age_years < 55 THEN '45-54'
                    WHEN age_years < 65 THEN '55-64'
                    ELSE '65+'
                END AS age_group,
                COUNT(*) AS total_customer,
                ROUND(AVG("TARGET")::NUMERIC * 100, 2) AS default_rate_pct
            FROM vw_credit_risk
            GROUP BY age_group
            ORDER BY age_group
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/avg-loan-by-default")
def get_avg_loan_by_default():
    """Rata-rata pinjaman berdasarkan status default."""
    try:
        return _query("""
            SELECT
                "TARGET",
                COUNT(*) AS total_customer,
                ROUND(AVG("AMT_CREDIT")::NUMERIC, 0) AS avg_credit_amount,
                ROUND(AVG("AMT_INCOME_TOTAL")::NUMERIC, 0) AS avg_income,
                ROUND(AVG(credit_income_ratio)::NUMERIC, 2) AS avg_credit_income_ratio
            FROM vw_credit_risk
            GROUP BY "TARGET"
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/default-by-gender")
def get_default_by_gender():
    """Default rate berdasarkan gender dan kepemilikan aset."""
    try:
        return _query("""
            SELECT
                "CODE_GENDER",
                "FLAG_OWN_CAR",
                "FLAG_OWN_REALTY",
                COUNT(*) AS total_customer,
                ROUND(AVG("TARGET")::NUMERIC * 100, 2) AS default_rate_pct
            FROM vw_credit_risk
            GROUP BY "CODE_GENDER", "FLAG_OWN_CAR", "FLAG_OWN_REALTY"
            ORDER BY default_rate_pct DESC
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/feature-correlation")
def get_feature_correlation():
    """Korelasi fitur numerik terhadap TARGET."""
    try:
        return _query("""
            SELECT feature, correlation FROM (
                SELECT 'AMT_INCOME_TOTAL' AS feature, CORR("TARGET", "AMT_INCOME_TOTAL") AS correlation FROM vw_credit_risk
                UNION ALL SELECT 'AMT_CREDIT', CORR("TARGET", "AMT_CREDIT") FROM vw_credit_risk
                UNION ALL SELECT 'AMT_ANNUITY', CORR("TARGET", "AMT_ANNUITY") FROM vw_credit_risk
                UNION ALL SELECT 'credit_income_ratio', CORR("TARGET", credit_income_ratio) FROM vw_credit_risk
                UNION ALL SELECT 'age_years', CORR("TARGET", age_years) FROM vw_credit_risk
                UNION ALL SELECT 'employment_years', CORR("TARGET", employment_years) FROM vw_credit_risk
                UNION ALL SELECT 'EXT_SOURCE_1', CORR("TARGET", "EXT_SOURCE_1") FROM vw_credit_risk
                UNION ALL SELECT 'EXT_SOURCE_2', CORR("TARGET", "EXT_SOURCE_2") FROM vw_credit_risk
                UNION ALL SELECT 'EXT_SOURCE_3', CORR("TARGET", "EXT_SOURCE_3") FROM vw_credit_risk
            ) AS t
            ORDER BY ABS(correlation) DESC
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))