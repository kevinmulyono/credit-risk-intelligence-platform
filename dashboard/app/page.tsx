import Link from "next/link";

const features = [
  {
    href: "/executive",
    icon: "📊",
    title: "Executive Dashboard",
    desc: "KPI utama: total customer, default rate, rata-rata income & kredit.",
  },
  {
    href: "/analytics",
    icon: "📈",
    title: "Business Analytics",
    desc: "Default rate berdasarkan pendidikan, pekerjaan, usia, dan income group.",
  },
  {
    href: "/predict",
    icon: "🤖",
    title: "ML Prediction",
    desc: "Isi data calon peminjam → prediksi probabilitas gagal bayar secara instan.",
  },
  {
    href: "/decision",
    icon: "⚖️",
    title: "Decision Support",
    desc: "Risk gauge + faktor utama + rekomendasi Approve / Review / Reject.",
  },
];

export default function Home() {
  return (
    <>
      <div className="home-hero">
        <h1>Credit Risk Intelligence Platform</h1>
        <p>
          Platform end-to-end untuk menganalisis dan memprediksi risiko gagal
          bayar customer, berbasis PostgreSQL + Machine Learning (LightGBM) +
          FastAPI + Next.js.
        </p>
      </div>

      <div className="page-subtitle">Pilih halaman untuk mulai:</div>
      <div className="features-grid">
        {features.map((f) => (
          <Link key={f.href} href={f.href} className="feature-card">
            <div className="feature-icon">{f.icon}</div>
            <div className="feature-title">{f.title}</div>
            <div className="feature-desc">{f.desc}</div>
          </Link>
        ))}
      </div>

      <hr className="divider" />

      <div className="card">
        <div className="card-title">Arsitektur</div>
        <table>
          <thead>
            <tr>
              <th>Layer</th>
              <th>Teknologi</th>
              <th>Fungsi</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Data Storage</td><td>PostgreSQL</td><td>8 raw tables + 6 SQL views</td></tr>
            <tr><td>ETL</td><td>Python / Pandas</td><td>CSV → PostgreSQL</td></tr>
            <tr><td>Machine Learning</td><td>LightGBM + SHAP</td><td>Prediksi risiko kredit, AUC 0.7783</td></tr>
            <tr><td>API Backend</td><td>FastAPI</td><td>/predict + /analytics/*</td></tr>
            <tr><td>Frontend</td><td>Next.js</td><td>Dashboard interaktif</td></tr>
          </tbody>
        </table>
      </div>

      <div className="card">
        <div className="card-title">Hasil Model</div>
        <div className="kpi-grid">
          <div className="kpi-card">
            <div className="kpi-label">Model</div>
            <div className="kpi-value">LightGBM</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">AUC Score</div>
            <div className="kpi-value">0.7783</div>
            <div className="kpi-sub">vs Logistic Regression: 0.7628</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Training Data</div>
            <div className="kpi-value">307,511</div>
            <div className="kpi-sub">loan applications</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Features</div>
            <div className="kpi-value">98</div>
            <div className="kpi-sub">setelah encoding</div>
          </div>
        </div>
      </div>
    </>
  );
}
