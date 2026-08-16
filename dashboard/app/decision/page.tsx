"use client";

import { useState, FormEvent } from "react";

interface Factor {
  feature: string;
  direction: string;
  importance: number;
}

interface DecisionResult {
  probability: number;
  risk_category: string;
  recommendation: string;
  top_factors: Factor[];
}

const FEATURE_LABELS: Record<string, string> = {
  EXT_SOURCE_3: "Skor Eksternal 3 (Kredit Rating)",
  EXT_SOURCE_2: "Skor Eksternal 2 (Kredit Rating)",
  EXT_SOURCE_1: "Skor Eksternal 1 (Kredit Rating)",
  age_years: "Usia Customer",
  employment_years: "Lama Bekerja",
  AMT_CREDIT: "Jumlah Pinjaman",
  AMT_GOODS_PRICE: "Harga Barang/Objek Dibiayai",
  AMT_ANNUITY: "Cicilan per Bulan",
  AMT_INCOME_TOTAL: "Total Pendapatan",
  FLAG_OWN_CAR: "Kepemilikan Mobil",
  FLAG_OWN_REALTY: "Kepemilikan Rumah/Properti",
  CODE_GENDER: "Jenis Kelamin",
};

function translateFeature(feature: string): string {
  return FEATURE_LABELS[feature] || feature;
}

export default function DecisionSupport() {
  const [formData, setFormData] = useState({
    AMT_INCOME_TOTAL: 180000000,
    AMT_CREDIT: 450000000,
    AMT_ANNUITY: 2500000,
    AMT_GOODS_PRICE: 400000000,
    age_years: 35,
    employment_years: 5,
    CNT_CHILDREN: 0,
    CNT_FAM_MEMBERS: 2,
    EXT_SOURCE_1: 0.5,
    EXT_SOURCE_2: 0.5,
    EXT_SOURCE_3: 0.5,
    CODE_GENDER: 1,
    FLAG_OWN_CAR: 1,
    FLAG_OWN_REALTY: 1,
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DecisionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: string, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        throw new Error(`API Error status ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError("Tidak dapat terhubung ke API. Pastikan FastAPI server berjalan di http://localhost:8000");
    } finally {
      setLoading(false);
    }
  };

  const posFactors = result?.top_factors.filter((f) => f.direction === "Menurunkan Risiko") || [];
  const negFactors = result?.top_factors.filter((f) => f.direction === "Meningkatkan Risiko") || [];
  const riskScore = result ? Math.round(result.probability * 100) : 0;

  return (
    <>
      <div className="page-title">Decision Support System</div>
      <div className="page-subtitle">
        Sistem analisis pendukung keputusan persetujuan kredit berbasis Explainable AI (SHAP).
      </div>

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="card-title">Input Profile Customer</div>
          <div className="form-grid">
            <div className="form-group">
              <label className="form-label">Total Income / Tahun (Rp)</label>
              <input
                type="number"
                className="form-input"
                value={formData.AMT_INCOME_TOTAL}
                onChange={(e) => handleChange("AMT_INCOME_TOTAL", Number(e.target.value))}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Jumlah Pinjaman (Rp)</label>
              <input
                type="number"
                className="form-input"
                value={formData.AMT_CREDIT}
                onChange={(e) => handleChange("AMT_CREDIT", Number(e.target.value))}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Annuity / Cicilan per Bulan (Rp)</label>
              <input
                type="number"
                className="form-input"
                value={formData.AMT_ANNUITY}
                onChange={(e) => handleChange("AMT_ANNUITY", Number(e.target.value))}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Harga Barang (Rp)</label>
              <input
                type="number"
                className="form-input"
                value={formData.AMT_GOODS_PRICE}
                onChange={(e) => handleChange("AMT_GOODS_PRICE", Number(e.target.value))}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Usia (Tahun)</label>
              <input
                type="number"
                className="form-input"
                value={formData.age_years}
                onChange={(e) => handleChange("age_years", Number(e.target.value))}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Lama Bekerja (Tahun)</label>
              <input
                type="number"
                step="0.5"
                className="form-input"
                value={formData.employment_years}
                onChange={(e) => handleChange("employment_years", Number(e.target.value))}
                required
              />
            </div>
          </div>

          <hr className="divider" />

          <div className="slider-row" style={{ marginBottom: "20px" }}>
            <div className="slider-group">
              <label className="form-label">External Score 1</label>
              <span className="slider-value">{formData.EXT_SOURCE_1.toFixed(2)}</span>
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={formData.EXT_SOURCE_1}
                onChange={(e) => handleChange("EXT_SOURCE_1", parseFloat(e.target.value))}
              />
            </div>
            <div className="slider-group">
              <label className="form-label">External Score 2</label>
              <span className="slider-value">{formData.EXT_SOURCE_2.toFixed(2)}</span>
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={formData.EXT_SOURCE_2}
                onChange={(e) => handleChange("EXT_SOURCE_2", parseFloat(e.target.value))}
              />
            </div>
            <div className="slider-group">
              <label className="form-label">External Score 3</label>
              <span className="slider-value">{formData.EXT_SOURCE_3.toFixed(2)}</span>
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={formData.EXT_SOURCE_3}
                onChange={(e) => handleChange("EXT_SOURCE_3", parseFloat(e.target.value))}
              />
            </div>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Menganalisis..." : "⚖️ Analisis Keputusan Kredit"}
          </button>
        </form>
      </div>

      {error && <div className="error-box">⚠️ {error}</div>}

      {result && (
        <>
          <div className="card">
            <div className="card-title">Risk Score Gauge</div>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
              <span>Skor Gagal Bayar: <strong>{riskScore} / 100</strong></span>
              <span><strong>{result.risk_category}</strong></span>
            </div>
            <div className="progress-track">
              <div
                className={`progress-fill ${
                  result.risk_category === "Low Risk"
                    ? "progress-low"
                    : result.risk_category === "Medium Risk"
                    ? "progress-medium"
                    : "progress-high"
                }`}
                style={{ width: `${riskScore}%` }}
              />
            </div>
          </div>

          <div className="card">
            <div className="card-title">Analisis Faktor Positif & Negatif</div>
            <div className="factors-grid">
              <div>
                <div style={{ fontWeight: 600, color: "var(--success)", marginBottom: "8px" }}>
                  ✔ Faktor Positif (Menurunkan Risiko)
                </div>
                {posFactors.length > 0 ? (
                  <ul className="factor-list">
                    {posFactors.map((f, i) => (
                      <li key={i} className="factor-item">
                        🟢 <strong>{translateFeature(f.feature)}</strong>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="form-hint">Tidak ada faktor positif signifikan.</div>
                )}
              </div>

              <div>
                <div style={{ fontWeight: 600, color: "var(--danger)", marginBottom: "8px" }}>
                  ✘ Faktor Negatif (Meningkatkan Risiko)
                </div>
                {negFactors.length > 0 ? (
                  <ul className="factor-list">
                    {negFactors.map((f, i) => (
                      <li key={i} className="factor-item">
                        🔴 <strong>{translateFeature(f.feature)}</strong>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="form-hint">Tidak ada faktor negatif signifikan.</div>
                )}
              </div>
            </div>

            <hr className="divider" />

            <div className="card-title">Rekomendasi Keputusan Akhir</div>
            {result.recommendation === "Approve" && (
              <div className="rec-box rec-approve">
                ✅ <strong>APPROVE</strong> — Customer memiliki profil risiko rendah dan direkomendasikan untuk disetujui.
              </div>
            )}
            {result.recommendation === "Manual Review" && (
              <div className="rec-box rec-review">
                ⚠️ <strong>MANUAL REVIEW</strong> — Customer memiliki profil risiko sedang. Perlu peninjauan manual oleh tim Credit Risk Analyst.
              </div>
            )}
            {result.recommendation === "Reject" && (
              <div className="rec-box rec-reject">
                ❌ <strong>REJECT</strong> — Customer memiliki profil risiko tinggi dan tidak direkomendasikan untuk disetujui tanpa jaminan/mitigasi tambahan.
              </div>
            )}
          </div>
        </>
      )}
    </>
  );
}
