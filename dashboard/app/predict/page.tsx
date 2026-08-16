"use client";

import { useState, FormEvent } from "react";

interface Factor {
  feature: string;
  direction: string;
  importance: number;
}

interface PredictionResult {
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

export default function MLPrediction() {
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
    CODE_GENDER: 1, // 1 = Laki-laki, 0 = Perempuan
    FLAG_OWN_CAR: 1, // 1 = Ya, 0 = Tidak
    FLAG_OWN_REALTY: 1, // 1 = Ya, 0 = Tidak
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
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
      setError(
        "Tidak dapat terhubung ke FastAPI server. Pastikan API berjalan di http://localhost:8000"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="page-title">Machine Learning Risk Prediction</div>
      <div className="page-subtitle">
        Isi formulir pengajuan kredit di bawah ini untuk menghitung kemungkinan gagal bayar customer menggunakan model LightGBM.
      </div>

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="card-title">1. Data Keuangan & Pinjaman</div>
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
              <label className="form-label">Jumlah Pinjaman / Credit (Rp)</label>
              <input
                type="number"
                className="form-input"
                value={formData.AMT_CREDIT}
                onChange={(e) => handleChange("AMT_CREDIT", Number(e.target.value))}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Cicilan per Bulan / Annuity (Rp)</label>
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
              <label className="form-label">Jumlah Anak</label>
              <input
                type="number"
                className="form-input"
                value={formData.CNT_CHILDREN}
                onChange={(e) => handleChange("CNT_CHILDREN", Number(e.target.value))}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Jumlah Anggota Keluarga</label>
              <input
                type="number"
                className="form-input"
                value={formData.CNT_FAM_MEMBERS}
                onChange={(e) => handleChange("CNT_FAM_MEMBERS", Number(e.target.value))}
                required
              />
            </div>
          </div>

          <hr className="divider" />

          <div className="card-title">2. Data Demografi & Aset</div>
          <div className="form-grid">
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
            <div className="form-group">
              <label className="form-label">Jenis Kelamin</label>
              <select
                className="form-select"
                value={formData.CODE_GENDER}
                onChange={(e) => handleChange("CODE_GENDER", Number(e.target.value))}
              >
                <option value={1}>Laki-laki</option>
                <option value={0}>Perempuan</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Memiliki Mobil?</label>
              <select
                className="form-select"
                value={formData.FLAG_OWN_CAR}
                onChange={(e) => handleChange("FLAG_OWN_CAR", Number(e.target.value))}
              >
                <option value={1}>Ya</option>
                <option value={0}>Tidak</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Memiliki Rumah/Properti?</label>
              <select
                className="form-select"
                value={formData.FLAG_OWN_REALTY}
                onChange={(e) => handleChange("FLAG_OWN_REALTY", Number(e.target.value))}
              >
                <option value={1}>Ya</option>
                <option value={0}>Tidak</option>
              </select>
            </div>
          </div>

          <hr className="divider" />

          <div className="card-title">3. Skor Kredit Eksternal (BI Checking / SLIK Score)</div>
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
            {loading ? "Memproses Prediksi ML..." : "🚀 Hitung Prediksi Risiko"}
          </button>
        </form>
      </div>

      {error && <div className="error-box">⚠️ {error}</div>}

      {result && (
        <div className="card">
          <div className="card-title">Hasil Prediksi Risiko Kredit</div>

          <div className="result-box">
            <div className="result-card">
              <div className="result-label">Probabilitas Default</div>
              <div className="result-value">{(result.probability * 100).toFixed(1)}%</div>
            </div>

            <div className="result-card">
              <div className="result-label">Kategori Risiko</div>
              <div className="result-value">
                <span
                  className={`badge ${
                    result.risk_category === "Low Risk"
                      ? "badge-low"
                      : result.risk_category === "Medium Risk"
                      ? "badge-medium"
                      : "badge-high"
                  }`}
                >
                  {result.risk_category === "Low Risk"
                    ? "🟢 Risiko Rendah"
                    : result.risk_category === "Medium Risk"
                    ? "🟡 Risiko Sedang"
                    : "🔴 Risiko Tinggi"}
                </span>
              </div>
            </div>

            <div className="result-card">
              <div className="result-label">Rekomendasi</div>
              <div className="result-value">
                <span
                  className={`badge ${
                    result.recommendation === "Approve"
                      ? "badge-low"
                      : result.recommendation === "Manual Review"
                      ? "badge-medium"
                      : "badge-high"
                  }`}
                >
                  {result.recommendation}
                </span>
              </div>
            </div>
          </div>

          <div className="card-title">Faktor-Faktor Penentu Utama</div>
          <div className="bar-list">
            {result.top_factors.map((f, i) => (
              <div key={i} className="bar-item">
                <div className="bar-label">{translateFeature(f.feature)}</div>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{
                      width: `${Math.min(100, Math.round(f.importance * 100))}%`,
                      background: f.direction === "Meningkatkan Risiko" ? "var(--danger)" : "var(--success)",
                    }}
                  />
                </div>
                <div className="bar-val">
                  {f.direction === "Meningkatkan Risiko" ? "🔺 Risiko ⬆" : "🔻 Risiko ⬇"}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
