import joblib
import pandas as pd
import numpy as np
from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "models"

_model = joblib.load(MODEL_DIR / "credit_risk_model.pkl")
_feature_columns = joblib.load(MODEL_DIR / "feature_columns.pkl")


def classify_risk(probability: float) -> str:
    """
    Klasifikasi probability default menjadi kategori risiko bisnis.
    """
    if probability < 0.10:
        return "Low Risk"
    elif probability < 0.30:
        return "Medium Risk"
    else:
        return "High Risk"


def get_recommendation(risk_category: str) -> str:
    """
    Rekomendasi keputusan bisnis berdasarkan kategori risiko.
    """
    mapping = {
        "Low Risk": "Approve",
        "Medium Risk": "Manual Review",
        "High Risk": "Reject"
    }
    return mapping[risk_category]


def get_top_contributing_factors(shap_row: np.ndarray, feature_names: list, top_n: int = 5) -> pd.DataFrame:
    """
    Mengembalikan top N fitur paling berkontribusi terhadap prediksi,
    beserta arah kontribusinya.
    """
    contributions = pd.DataFrame({
        "feature": feature_names,
        "shap_value": shap_row
    })
    contributions["abs_value"] = contributions["shap_value"].abs()
    contributions = contributions.sort_values("abs_value", ascending=False).head(top_n)
    contributions["direction"] = contributions["shap_value"].apply(
        lambda x: "Meningkatkan Risiko" if x > 0 else "Menurunkan Risiko"
    )
    return contributions[["feature", "shap_value", "direction"]]


def compute_derived_features(input_dict: dict) -> dict:
    """
    Menghitung ulang fitur turunan (rasio) dari input mentah,
    supaya konsisten dengan cara feature_table_final dibangun di Milestone 19.

    Tanpa langkah ini, fitur seperti goods_price_credit_ratio akan selalu
    bernilai 0 meski AMT_INCOME_TOTAL / AMT_CREDIT diubah oleh user,
    karena fitur tersebut tidak dikirim langsung lewat form.
    """
    data = dict(input_dict)  # copy, supaya tidak mengubah input asli

    income = data.get("AMT_INCOME_TOTAL")
    credit = data.get("AMT_CREDIT")
    annuity = data.get("AMT_ANNUITY")
    goods_price = data.get("AMT_GOODS_PRICE")
    fam_members = data.get("CNT_FAM_MEMBERS")

    if credit and income:
        data["credit_income_ratio"] = round(credit / income, 4)

    if annuity and income:
        data["annuity_income_ratio"] = round(annuity / income, 6)

    if goods_price and credit:
        data["goods_price_credit_ratio"] = round(goods_price / credit, 4)

    if income and fam_members:
        data["income_per_family_member"] = round(income / fam_members, 2)

    return data


def predict_credit_risk(input_dict: dict) -> dict:
    """
    Fungsi utama scoring end-to-end.

    Parameters
    ----------
    input_dict : dict
        Dictionary berisi nilai fitur customer.
        Key harus sesuai dengan kolom di feature_columns.pkl.
        Fitur yang tidak dikirim akan diisi 0 (default aman untuk kolom hasil one-hot encoding
        dan kolom histori yang memang berarti "tidak ada riwayat").

    Returns
    -------
    dict berisi: probability, risk_category, recommendation, top_factors
    """
    # Hitung fitur turunan dari input mentah sebelum membentuk baris fitur
    enriched_input = compute_derived_features(input_dict)

    # Susun input jadi 1 baris DataFrame sesuai urutan kolom training
    row = {col: enriched_input.get(col, 0) for col in _feature_columns}
    X_input = pd.DataFrame([row], columns=_feature_columns)

    # Prediksi probability
    probability = float(_model.predict_proba(X_input)[0, 1])

    # Kategori risiko & rekomendasi
    risk_category = classify_risk(probability)
    recommendation = get_recommendation(risk_category)

    # SHAP contribution (native LightGBM, tanpa library shap)
    shap_contrib = _model.booster_.predict(X_input, pred_contrib=True)
    shap_values_row = shap_contrib[0, :-1]

    top_factors = get_top_contributing_factors(shap_values_row, _feature_columns, top_n=5)

    return {
        "probability": round(probability, 4),
        "risk_category": risk_category,
        "recommendation": recommendation,
        "top_factors": top_factors.to_dict(orient="records")
    }