"use client";

import { useEffect, useState } from "react";

interface KPI {
  total_customer?: number;
  total_default?: number;
  default_rate_pct?: number;
  avg_income?: number;
  avg_credit?: number;
}

interface LoanDist {
  credit_group: string;
  total_customer: number;
}

interface RiskDist {
  risk_category: string;
  total_customer: number;
}

export default function ExecutiveDashboard() {
  const [kpi, setKpi] = useState<KPI | null>(null);
  const [loanDist, setLoanDist] = useState<LoanDist[]>([]);
  const [riskDist, setRiskDist] = useState<RiskDist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        setError(null);
        const [resKpi, resLoan, resRisk] = await Promise.all([
          fetch("http://localhost:8000/analytics/kpi"),
          fetch("http://localhost:8000/analytics/loan-distribution"),
          fetch("http://localhost:8000/analytics/risk-distribution"),
        ]);

        if (!resKpi.ok || !resLoan.ok || !resRisk.ok) {
          throw new Error("Gagal mengunduh data dari API FastAPI.");
        }

        const dataKpi = await resKpi.json();
        const dataLoan = await resLoan.json();
        const dataRisk = await resRisk.json();

        setKpi(dataKpi);
        setLoanDist(dataLoan);
        setRiskDist(dataRisk);
      } catch (err: any) {
        setError(err.message || "Terjadi kesalahan saat memuat data.");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const maxLoanCount = Math.max(...loanDist.map((d) => d.total_customer), 1);
  const maxRiskCount = Math.max(...riskDist.map((d) => d.total_customer), 1);

  return (
    <>
      <div className="page-title">Executive Dashboard</div>
      <div className="page-subtitle">
        Ringkasan KPI utama dan gambaran umum seluruh portofolio kredit customer.
      </div>

      {loading && <div className="loading">Memuat data KPI & distribusi portofolio...</div>}

      {error && (
        <div className="error-box">
          ⚠️ {error} Pastikan FastAPI backend berjalan di <code>http://localhost:8000</code>.
        </div>
      )}

      {!loading && !error && kpi && (
        <>
          <div className="kpi-grid">
            <div className="kpi-card">
              <div className="kpi-label">Total Customer</div>
              <div className="kpi-value">{kpi.total_customer?.toLocaleString("id-ID") ?? 0}</div>
              <div className="kpi-sub">Total pengajuan diproses</div>
            </div>

            <div className="kpi-card">
              <div className="kpi-label">Default Rate</div>
              <div className="kpi-value">{kpi.default_rate_pct ?? 0}%</div>
              <div className="kpi-sub">{kpi.total_default?.toLocaleString("id-ID")} total gagal bayar</div>
            </div>

            <div className="kpi-card">
              <div className="kpi-label">Rata-rata Income</div>
              <div className="kpi-value">
                Rp {Math.round(kpi.avg_income ?? 0).toLocaleString("id-ID")}
              </div>
              <div className="kpi-sub">Pendapatan tahunan</div>
            </div>

            <div className="kpi-card">
              <div className="kpi-label">Rata-rata Kredit</div>
              <div className="kpi-value">
                Rp {Math.round(kpi.avg_credit ?? 0).toLocaleString("id-ID")}
              </div>
              <div className="kpi-sub">Nilai pinjaman disetujui</div>
            </div>
          </div>

          <hr className="divider" />

          <div className="two-col">
            <div className="card">
              <div className="card-title">Distribusi Jumlah Pinjaman</div>
              <div className="bar-list">
                {loanDist.map((item) => {
                  const pct = Math.round((item.total_customer / maxLoanCount) * 100);
                  return (
                    <div key={item.credit_group} className="bar-item">
                      <div className="bar-label">{item.credit_group}</div>
                      <div className="bar-track">
                        <div className="bar-fill" style={{ width: `${pct}%` }} />
                      </div>
                      <div className="bar-val">{item.total_customer.toLocaleString("id-ID")}</div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="card">
              <div className="card-title">Distribusi Kategori Risiko (EXT_SOURCE_3)</div>
              <div className="bar-list">
                {riskDist.map((item) => {
                  const pct = Math.round((item.total_customer / maxRiskCount) * 100);
                  return (
                    <div key={item.risk_category} className="bar-item">
                      <div className="bar-label">{item.risk_category}</div>
                      <div className="bar-track">
                        <div className="bar-fill" style={{ width: `${pct}%` }} />
                      </div>
                      <div className="bar-val">{item.total_customer.toLocaleString("id-ID")}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
}
