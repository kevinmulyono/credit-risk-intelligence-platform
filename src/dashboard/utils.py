"""
Dashboard Utility Functions
Fungsi-fungsi helper untuk aplikasi dashboard Streamlit.
"""

import pandas as pd
from typing import Dict, Any


def format_currency(amount: float, currency: str = "Rp") -> str:
    """
    Format angka menjadi format mata uang.
    
    Parameters
    ----------
    amount : float
        Jumlah uang
    currency : str
        Simbol mata uang (default: "Rp")
        
    Returns
    -------
    str
        String terformat (contoh: "Rp 1,000,000")
    """
    return f"{currency} {int(amount):,}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format angka menjadi persentase.
    
    Parameters
    ----------
    value : float
        Nilai (0-1 untuk persentase desimal, atau 0-100 untuk persentase biasa)
    decimals : int
        Jumlah digit desimal (default: 2)
        
    Returns
    -------
    str
        String terformat (contoh: "12.34%")
    """
    if value <= 1:
        value = value * 100
    return f"{value:.{decimals}f}%"


def calculate_credit_metrics(income: float, credit: float, annuity: float) -> Dict[str, float]:
    """
    Hitung metrik-metrik penting terkait kredit.
    
    Parameters
    ----------
    income : float
        Total penghasilan
    credit : float
        Jumlah kredit
    annuity : float
        Cicilan per periode
        
    Returns
    -------
    dict
        Dictionary berisi berbagai metrik
    """
    metrics = {}
    
    if income > 0:
        metrics["credit_to_income_ratio"] = credit / income
        metrics["annuity_to_income_ratio"] = annuity / income
    else:
        metrics["credit_to_income_ratio"] = 0
        metrics["annuity_to_income_ratio"] = 0
    
    if annuity > 0:
        metrics["loan_term_months"] = credit / annuity
    else:
        metrics["loan_term_months"] = 0
    
    return metrics


def get_risk_color(risk_category: str) -> str:
    """
    Dapatkan warna sesuai kategori risiko.
    
    Parameters
    ----------
    risk_category : str
        Kategori risiko ("Low Risk", "Medium Risk", "High Risk")
        
    Returns
    -------
    str
        Nama warna untuk Streamlit
    """
    color_map = {
        "Low Risk": "green",
        "Medium Risk": "orange",
        "High Risk": "red"
    }
    return color_map.get(risk_category, "gray")


def get_risk_icon(risk_category: str) -> str:
    """
    Dapatkan emoji icon sesuai kategori risiko.
    
    Parameters
    ----------
    risk_category : str
        Kategori risiko
        
    Returns
    -------
    str
        Emoji icon
    """
    icon_map = {
        "Low Risk": "🟢",
        "Medium Risk": "🟡",
        "High Risk": "🔴"
    }
    return icon_map.get(risk_category, "⚪")


def safe_division(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Pembagian yang aman (menghindari division by zero).
    
    Parameters
    ----------
    numerator : float
        Pembilang
    denominator : float
        Penyebut
    default : float
        Nilai default jika denominator = 0
        
    Returns
    -------
    float
        Hasil pembagian atau default value
    """
    if denominator == 0:
        return default
    return numerator / denominator