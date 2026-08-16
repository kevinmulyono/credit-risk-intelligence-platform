import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import streamlit as st

from src.analysis.queries import (
    get_default_rate_by_education,
    get_default_rate_by_occupation,
    get_default_rate_by_income_group,
    get_default_rate_by_age_group,
    get_avg_loan_by_default_status,
    get_default_rate_by_gender_ownership,
    get_feature_correlation,
)

st.set_page_config(page_title="Business Analytics", layout="wide")

st.title("Business Analytics Dashboard")
st.markdown("Analisis mendalam faktor-faktor yang mempengaruhi risiko default berdasarkan segmen customer.")

st.divider()

# ============================================================
# Default Rate by Education
# ============================================================
st.subheader("Default Rate by Education")
df_education = get_default_rate_by_education()

col1, col2 = st.columns([2, 1])
with col1:
    st.bar_chart(df_education.set_index("NAME_EDUCATION_TYPE")["default_rate_pct"])
with col2:
    st.dataframe(df_education, use_container_width=True, hide_index=True)

st.divider()

# ============================================================
# Default Rate by Occupation
# ============================================================
st.subheader("Default Rate by Occupation")
df_occupation = get_default_rate_by_occupation()

col1, col2 = st.columns([2, 1])
with col1:
    st.bar_chart(df_occupation.set_index("OCCUPATION_TYPE")["default_rate_pct"])
with col2:
    st.dataframe(df_occupation, use_container_width=True, hide_index=True)

st.divider()

# ============================================================
# Default Rate by Income Group & Age Group
# ============================================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Default Rate by Income Group")
    df_income = get_default_rate_by_income_group()
    st.bar_chart(df_income.set_index("income_group")["default_rate_pct"])
    st.dataframe(df_income, use_container_width=True, hide_index=True)

with col_right:
    st.subheader("Default Rate by Age Group")
    df_age = get_default_rate_by_age_group()
    st.bar_chart(df_age.set_index("age_group")["default_rate_pct"])
    st.dataframe(df_age, use_container_width=True, hide_index=True)

st.divider()

# ============================================================
# Average Loan by Default Status
# ============================================================
st.subheader("Average Loan Amount by Default Status")
df_loan_status = get_avg_loan_by_default_status()
st.dataframe(df_loan_status, use_container_width=True, hide_index=True)

st.divider()

# ============================================================
# Default Rate by Gender & Asset Ownership
# ============================================================
st.subheader("Default Rate by Gender & Asset Ownership")
df_gender = get_default_rate_by_gender_ownership()
st.dataframe(df_gender, use_container_width=True, hide_index=True)

st.divider()

# ============================================================
# Feature Correlation
# ============================================================
st.subheader("Korelasi Fitur Numerik terhadap TARGET")
df_corr = get_feature_correlation()

col1, col2 = st.columns([2, 1])
with col1:
    st.bar_chart(df_corr.set_index("feature")["correlation"])
with col2:
    st.dataframe(df_corr, use_container_width=True, hide_index=True)

st.caption("Data bersumber dari vw_credit_risk (PostgreSQL) via src/analysis/queries.py")