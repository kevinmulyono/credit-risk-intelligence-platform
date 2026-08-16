"""
Feature Labels Translation
Menerjemahkan nama fitur teknis dari model ML menjadi label yang user-friendly.
"""

FEATURE_TRANSLATIONS = {
    # Financial Features
    "AMT_INCOME_TOTAL": "Total Penghasilan",
    "AMT_CREDIT": "Jumlah Kredit",
    "AMT_ANNUITY": "Cicilan per Periode",
    "AMT_GOODS_PRICE": "Harga Barang",
    
    # Demographic Features
    "age_years": "Usia",
    "employment_years": "Lama Bekerja",
    "CNT_CHILDREN": "Jumlah Anak",
    "CNT_FAM_MEMBERS": "Jumlah Anggota Keluarga",
    
    # External Scores
    "EXT_SOURCE_1": "Skor Kredit Eksternal 1",
    "EXT_SOURCE_2": "Skor Kredit Eksternal 2",
    "EXT_SOURCE_3": "Skor Kredit Eksternal 3",
    
    # Binary Features
    "CODE_GENDER": "Jenis Kelamin",
    "FLAG_OWN_CAR": "Kepemilikan Mobil",
    "FLAG_OWN_REALTY": "Kepemilikan Rumah",
    
    # Additional Features (might be present in the model)
    "DAYS_BIRTH": "Usia (dalam hari)",
    "DAYS_EMPLOYED": "Lama Bekerja (dalam hari)",
    "DAYS_ID_PUBLISH": "Usia Dokumen Identitas",
    "DAYS_REGISTRATION": "Lama Registrasi",
    "REGION_RATING_CLIENT": "Rating Regional",
    "REGION_RATING_CLIENT_W_CITY": "Rating Regional dengan Kota",
    
    # Income Type
    "NAME_INCOME_TYPE_Working": "Tipe Penghasilan: Bekerja",
    "NAME_INCOME_TYPE_Commercial associate": "Tipe Penghasilan: Asosiasi Komersial",
    "NAME_INCOME_TYPE_Pensioner": "Tipe Penghasilan: Pensiunan",
    "NAME_INCOME_TYPE_State servant": "Tipe Penghasilan: Pegawai Negeri",
    
    # Education Type
    "NAME_EDUCATION_TYPE_Secondary / secondary special": "Pendidikan: SMA/Diploma",
    "NAME_EDUCATION_TYPE_Higher education": "Pendidikan: S1/S2",
    "NAME_EDUCATION_TYPE_Incomplete higher": "Pendidikan: Belum Selesai S1",
    "NAME_EDUCATION_TYPE_Lower secondary": "Pendidikan: SMP",
    
    # Family Status
    "NAME_FAMILY_STATUS_Married": "Status Keluarga: Menikah",
    "NAME_FAMILY_STATUS_Single / not married": "Status Keluarga: Lajang",
    "NAME_FAMILY_STATUS_Civil marriage": "Status Keluarga: Menikah Sipil",
    "NAME_FAMILY_STATUS_Separated": "Status Keluarga: Berpisah",
    "NAME_FAMILY_STATUS_Widow": "Status Keluarga: Janda/Duda",
    
    # Housing Type
    "NAME_HOUSING_TYPE_House / apartment": "Tipe Hunian: Rumah/Apartemen",
    "NAME_HOUSING_TYPE_With parents": "Tipe Hunian: Bersama Orang Tua",
    "NAME_HOUSING_TYPE_Municipal apartment": "Tipe Hunian: Apartemen Kota",
    "NAME_HOUSING_TYPE_Rented apartment": "Tipe Hunian: Sewa",
    
    # Contract Type
    "NAME_CONTRACT_TYPE_Cash loans": "Tipe Kontrak: Pinjaman Tunai",
    "NAME_CONTRACT_TYPE_Revolving loans": "Tipe Kontrak: Pinjaman Berputar",
    
    # Bureau Features (if present)
    "bureau_count": "Jumlah Kredit di Bank Lain",
    "bureau_active_count": "Jumlah Kredit Aktif di Bank Lain",
    "bureau_total_debt": "Total Hutang di Bank Lain",
    "bureau_avg_days_credit": "Rata-rata Umur Kredit di Bank Lain",
    
    # Previous Application Features
    "prev_app_count": "Jumlah Pengajuan Sebelumnya",
    "prev_app_approved_count": "Jumlah Pengajuan yang Disetujui",
    "prev_app_refused_count": "Jumlah Pengajuan yang Ditolak",
    
    # Credit Card Features
    "cc_balance_mean": "Rata-rata Saldo Kartu Kredit",
    "cc_limit_mean": "Rata-rata Limit Kartu Kredit",
    "cc_utilization_mean": "Rata-rata Utilisasi Kartu Kredit",
    
    # Payment Features
    "payment_rate": "Tingkat Pembayaran",
    "credit_to_income_ratio": "Rasio Kredit terhadap Penghasilan",
    "annuity_to_income_ratio": "Rasio Cicilan terhadap Penghasilan",
}


def translate_feature(feature_name: str) -> str:
    """
    Menerjemahkan nama fitur teknis menjadi label yang mudah dipahami.
    
    Parameters
    ----------
    feature_name : str
        Nama fitur teknis dari model
        
    Returns
    -------
    str
        Label yang user-friendly dalam Bahasa Indonesia
    """
    return FEATURE_TRANSLATIONS.get(feature_name, feature_name)