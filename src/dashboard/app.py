import streamlit as st

st.set_page_config(
    page_title="Credit Risk Intelligence Platform",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Credit Risk Intelligence Platform")
st.markdown("""
Aplikasi ini membantu menganalisis dan memprediksi **risiko gagal bayar (kredit macet)** 
dari calon peminjam bank, menggunakan data histori dan machine learning.
""")

st.divider()

st.subheader("Mulai dari sini")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Untuk melihat gambaran umum
    Buka halaman **Executive Dashboard** di sidebar kiri — berisi ringkasan angka 
    penting seperti total customer, tingkat gagal bayar, dan rata-rata pinjaman.

    Lalu lanjut ke **Business Analytics** untuk melihat pola-pola menarik, 
    misalnya kelompok customer mana yang paling berisiko.
    """)

with col2:
    st.markdown("""
    ### Untuk memprediksi risiko customer baru
    Buka halaman **ML Prediction** — isi data calon peminjam, sistem akan 
    menghitung kemungkinan gagal bayarnya secara otomatis.

    Untuk penjelasan lebih lengkap beserta rekomendasi keputusan (setujui/tolak), 
    buka halaman **Decision Support System**.
    """)

st.divider()

with st.expander("Istilah yang mungkin belum familiar"):
    st.markdown("""
    - **Gagal bayar (default)**: customer tidak mampu melunasi pinjamannya sesuai jadwal.
    - **Skor Kredit Eksternal**: semacam "skor kredit" dari lembaga informasi keuangan 
      di luar bank ini — mirip seperti skor BI Checking / SLIK, semakin tinggi semakin baik.
    - **Risk Score**: angka 0-100 yang menunjukkan seberapa besar kemungkinan customer 
      gagal bayar. Semakin tinggi, semakin berisiko.
    """)