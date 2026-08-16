import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import streamlit as st
import requests

from src.dashboard.feature_labels import translate_feature

st.set_page_config(page_title="ML Prediction", layout="wide")

st.title("Prediksi Risiko Kredit")
st.markdown("""
Isi data calon peminjam di bawah ini, sistem akan menghitung kemungkinan 
customer tersebut **gagal bayar (default)** beserta faktor-faktor penyebabnya.
""")

API_URL = "http://127.0.0.1:8000/predict"

st.divider()

with st.form("prediction_form"):
    st.subheader("Data Keuangan")

    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input(
            "Total Penghasilan per Tahun (Rp)",
            min_value=0, value=180000000, step=1000000,
            help="Total pendapatan customer dalam setahun."
        )
        credit = st.number_input(
            "Jumlah Pinjaman yang Diajukan (Rp)",
            min_value=0, value=450000000, step=1000000,
            help="Total nilai pinjaman yang diajukan customer."
        )
        annuity = st.number_input(
            "Cicilan per Bulan (Rp)",
            min_value=0, value=2500000, step=100000,
            help="Jumlah yang harus dibayar customer setiap periode cicilan."
        )

    with col2:
        goods_price = st.number_input(
            "Harga Barang/Objek yang Dibiayai (Rp)",
            min_value=0, value=400000000, step=1000000,
            help="Contoh: harga rumah atau kendaraan yang dibeli dengan pinjaman ini."
        )
        children = st.number_input("Jumlah Anak", min_value=0, max_value=20, value=0)
        family_members = st.number_input("Jumlah Anggota Keluarga", min_value=1, max_value=20, value=2)

    st.divider()
    st.subheader("Data Pribadi")

    col3, col4 = st.columns(2)

    with col3:
        age = st.number_input("Usia (tahun)", min_value=18, max_value=100, value=35)
        employment_years = st.number_input("Lama Bekerja (tahun)", min_value=0.0, max_value=50.0, value=5.0)

    with col4:
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        own_car = st.selectbox("Punya Mobil?", ["Ya", "Tidak"])
        own_realty = st.selectbox("Punya Rumah?", ["Ya", "Tidak"])

    st.divider()
    st.subheader("Skor Kredit Eksternal")
    st.caption(
        "Skor ini mirip seperti riwayat BI Checking / SLIK — dihitung oleh lembaga "
        "informasi keuangan di luar bank. Semakin tinggi (mendekati 1.0), "
        "semakin baik rekam jejak keuangan customer. Kosongkan di angka default (0.5) "
        "jika tidak tahu."
    )

    col5, col6, col7 = st.columns(3)
    with col5:
        ext_source_1 = st.slider("Skor Eksternal 1", 0.0, 1.0, 0.5)
    with col6:
        ext_source_2 = st.slider("Skor Eksternal 2", 0.0, 1.0, 0.5)
    with col7:
        ext_source_3 = st.slider("Skor Eksternal 3", 0.0, 1.0, 0.5)

    submitted = st.form_submit_button("Hitung Risiko", use_container_width=True, type="primary")


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
        with st.spinner("Menghitung prediksi..."):
            response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()

            st.divider()
            st.subheader("Hasil Prediksi")

            risk_category = result["risk_category"]
            risk_text_id = {
                "Low Risk": "Risiko Rendah",
                "Medium Risk": "Risiko Sedang",
                "High Risk": "Risiko Tinggi",
            }
            recommendation_text_id = {
                "Approve": "Disetujui",
                "Manual Review": "Perlu Ditinjau Manual",
                "Reject": "Ditolak",
            }

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Kemungkinan Gagal Bayar", f"{result['probability'] * 100:.1f}%")

            with col2:
                risk_color = {"Low Risk": "🟢", "Medium Risk": "🟡", "High Risk": "🔴"}
                icon = risk_color.get(risk_category, "")
                st.metric("Tingkat Risiko", f"{icon} {risk_text_id.get(risk_category, risk_category)}")

            with col3:
                st.metric("Rekomendasi", recommendation_text_id.get(result["recommendation"], result["recommendation"]))

            st.divider()
            st.subheader("Apa yang Mempengaruhi Hasil Ini?")
            st.caption("Berikut faktor-faktor yang paling menentukan hasil prediksi di atas, diurutkan dari yang paling berpengaruh.")

            for factor in result["top_factors"]:
                label = translate_feature(factor["feature"])
                if factor["direction"] == "Meningkatkan Risiko":
                    st.write(f"🔺 **{label}** — membuat risiko lebih tinggi")
                else:
                    st.write(f"🔻 **{label}** — membuat risiko lebih rendah")

        else:
            st.error("Terjadi kesalahan saat memproses data. Silakan coba lagi.")

    except requests.exceptions.ConnectionError:
        st.error(
            "Sistem prediksi sedang tidak aktif. Pastikan server API sudah dijalankan "
            "(uvicorn src.api.main:app --reload)."
        )
    except requests.exceptions.Timeout:
        st.error("Proses memakan waktu terlalu lama. Silakan coba lagi.")