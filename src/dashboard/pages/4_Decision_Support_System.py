import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import streamlit as st
import requests

from src.dashboard.feature_labels import translate_feature

st.set_page_config(page_title="Decision Support System", layout="wide")

st.title("Decision Support System")
st.markdown("""
Sistem ini tidak hanya memprediksi risiko, tapi juga **menjelaskan** dan 
**merekomendasikan keputusan** berdasarkan hasil analisis model.
""")

API_URL = "http://127.0.0.1:8000/predict"

st.divider()

with st.form("dss_form"):
    st.subheader("Input Data Customer")

    col1, col2, col3 = st.columns(3)

    with col1:
        income = st.number_input("Total Income (Rp)", min_value=0, value=180000000, step=1000000, key="dss_income")
        credit = st.number_input("Jumlah Kredit (Rp)", min_value=0, value=450000000, step=1000000, key="dss_credit")
        annuity = st.number_input("Annuity (Rp)", min_value=0, value=2500000, step=100000, key="dss_annuity")
        goods_price = st.number_input("Harga Barang (Rp)", min_value=0, value=400000000, step=1000000, key="dss_goods")

    with col2:
        age = st.number_input("Usia (tahun)", min_value=18, max_value=100, value=35, key="dss_age")
        employment_years = st.number_input("Lama Bekerja (tahun)", min_value=0.0, max_value=50.0, value=5.0, key="dss_emp")
        children = st.number_input("Jumlah Anak", min_value=0, max_value=20, value=0, key="dss_children")
        family_members = st.number_input("Jumlah Anggota Keluarga", min_value=1, max_value=20, value=2, key="dss_family")

    with col3:
        ext_source_1 = st.slider("External Score 1", 0.0, 1.0, 0.5, key="dss_ext1")
        ext_source_2 = st.slider("External Score 2", 0.0, 1.0, 0.5, key="dss_ext2")
        ext_source_3 = st.slider("External Score 3", 0.0, 1.0, 0.5, key="dss_ext3")

    col4, col5, col6 = st.columns(3)
    with col4:
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"], key="dss_gender")
    with col5:
        own_car = st.selectbox("Punya Mobil?", ["Ya", "Tidak"], key="dss_car")
    with col6:
        own_realty = st.selectbox("Punya Rumah?", ["Ya", "Tidak"], key="dss_realty")

    submitted = st.form_submit_button("Analisis Keputusan", use_container_width=True)


if submitted:
    payload = {
        "AMT_INCOME_TOTAL": income,
        "AMT_CREDIT": credit,
        "AMT_ANNUITY": annuity,
        "AMT_GOODS_PRICE": goods_price,
        "age_years": age,
        "employment_years": employment_years,
        "CNT_CHILDREN": children,
        "CNT_FAM_MEMBERS": family_members,
        "EXT_SOURCE_1": ext_source_1,
        "EXT_SOURCE_2": ext_source_2,
        "EXT_SOURCE_3": ext_source_3,
        "CODE_GENDER": 1 if gender == "Laki-laki" else 0,
        "FLAG_OWN_CAR": 1 if own_car == "Ya" else 0,
        "FLAG_OWN_REALTY": 1 if own_realty == "Ya" else 0,
    }

    try:
        with st.spinner("Menganalisis..."):
            response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code != 200:
            st.error(f"API error: {response.status_code}")
            st.json(response.json())
        else:
            result = response.json()
            probability = result["probability"]
            risk_category = result["risk_category"]
            recommendation = result["recommendation"]
            top_factors = result["top_factors"]

            st.divider()

            # ============================================================
            # Risk Score Gauge (visual sederhana pakai progress bar)
            # ============================================================
            st.subheader("Risk Score")

            risk_score = int(probability * 100)
            st.progress(probability, text=f"{risk_score}/100")

            color_map = {"Low Risk": "green", "Medium Risk": "orange", "High Risk": "red"}
            st.markdown(f"### Kategori Risiko: :{color_map[risk_category]}[{risk_category}]")

            st.divider()

            # ============================================================
            # Top Contributing Factors (naratif)
            # ============================================================
            st.subheader("Faktor Utama yang Mempengaruhi")

            positive_factors = [f for f in top_factors if f["direction"] == "Menurunkan Risiko"]
            negative_factors = [f for f in top_factors if f["direction"] == "Meningkatkan Risiko"]

            col_pos, col_neg = st.columns(2)

            with col_pos:
                st.markdown("**✔ Faktor Positif**")
                if positive_factors:
                    for f in positive_factors:
                        label = translate_feature(f["feature"])
                        st.write(f"- **{label}**")
                else:
                    st.write("Tidak ada faktor positif signifikan.")

            with col_neg:
                st.markdown("**✘ Faktor Negatif**")
                if negative_factors:
                    for f in negative_factors:
                        label = translate_feature(f["feature"])
                        st.write(f"- **{label}**")
                else:
                    st.write("Tidak ada faktor negatif signifikan.")

            st.divider()

            # ============================================================
            # Recommendation
            # ============================================================
            st.subheader("Rekomendasi Keputusan")

            if recommendation == "Approve":
                st.success(f"✔ **APPROVE** — Customer ini menunjukkan profil risiko rendah dan direkomendasikan untuk disetujui.")
            elif recommendation == "Manual Review":
                st.warning(f"⚠ **MANUAL REVIEW** — Customer ini memiliki profil risiko menengah. Disarankan untuk ditinjau lebih lanjut oleh tim credit analyst sebelum keputusan final.")
            else:
                st.error(f"✘ **REJECT** — Customer ini menunjukkan profil risiko tinggi dan tidak direkomendasikan untuk disetujui tanpa mitigasi tambahan.")

            st.caption("""
            Catatan: Prediksi ini didasarkan pada data yang diinput. Fitur histori kredit 
            (bureau, kartu kredit, cicilan sebelumnya) yang tidak tersedia akan dianggap 
            sebagai 0/tidak ada oleh model, yang dapat mempengaruhi hasil untuk customer baru.
            """)

    except requests.exceptions.ConnectionError:
        st.error("Tidak bisa terhubung ke API. Pastikan FastAPI server sedang berjalan di http://127.0.0.1:8000")
    except requests.exceptions.Timeout:
        st.error("Request timeout. API terlalu lama merespons.")