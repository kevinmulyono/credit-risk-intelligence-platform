import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import streamlit as st
import pandas as pd
from sqlalchemy import text

from src.database.load_data import engine

st.set_page_config(page_title="Executive Dashboard", layout="wide")

st.title("Executive Dashboard")
st.markdown("Ringkasan KPI utama dari seluruh portofolio kredit.")


@st.cache_data(ttl=3600)
def load_kpi_data():
    query = """
        SELECT
            COUNT(*)                                        AS total_customer,
            SUM("TARGET")                                   AS total_default,
            ROUND(AVG("TARGET")::NUMERIC * 100, 2)          AS default_rate_pct,
            ROUND(AVG("AMT_INCOME_TOTAL")::NUMERIC, 0)      AS avg_income,
            ROUND(AVG("AMT_CREDIT")::NUMERIC, 0)            AS avg_credit
        FROM vw_credit_risk;
    """
    return pd.read_sql(text(query), engine).iloc[0]


@st.cache_data(ttl=3600)
def load_loan_distribution():
    query = """
        SELECT
            CASE
                WHEN "AMT_CREDIT" < 300000 THEN '1. < 300K'
                WHEN "AMT_CREDIT" < 600000 THEN '2. 300K - 600K'
                WHEN "AMT_CREDIT" < 900000 THEN '3. 600K - 900K'
                ELSE '4. > 900K'
            END AS credit_group,
            COUNT(*) AS total_customer
        FROM vw_credit_risk
        GROUP BY credit_group
        ORDER BY credit_group;
    """
    return pd.read_sql(text(query), engine)


@st.cache_data(ttl=3600)
def load_risk_category_distribution():
    query = """
        SELECT
            CASE
                WHEN "EXT_SOURCE_3" IS NULL THEN 'Unknown'
                WHEN "EXT_SOURCE_3" >= 0.6 THEN 'Low Risk'
                WHEN "EXT_SOURCE_3" >= 0.3 THEN 'Medium Risk'
                ELSE 'High Risk'
            END AS risk_category,
            COUNT(*) AS total_customer
        FROM vw_credit_risk
        GROUP BY risk_category;
    """
    return pd.read_sql(text(query), engine)


# ============================================================
# KPI Cards
# ============================================================
kpi = load_kpi_data()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customer", f"{int(kpi['total_customer']):,}")

with col2:
    st.metric("Default Rate", f"{kpi['default_rate_pct']}%")

with col3:
    st.metric("Rata-rata Income", f"Rp {int(kpi['avg_income']):,}")

with col4:
    st.metric("Rata-rata Kredit", f"Rp {int(kpi['avg_credit']):,}")

st.divider()

# ============================================================
# Charts
# ============================================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Distribusi Jumlah Pinjaman")
    df_loan = load_loan_distribution()
    st.bar_chart(df_loan.set_index("credit_group"))

with col_right:
    st.subheader("Distribusi Kategori Risiko (berdasarkan EXT_SOURCE_3)")
    df_risk = load_risk_category_distribution()
    st.bar_chart(df_risk.set_index("risk_category"))

st.divider()
st.caption("Data bersumber dari vw_credit_risk (PostgreSQL) — total 307,511 customer.")