"use client";

import { useEffect, useState } from "react";

interface EducationData {
  NAME_EDUCATION_TYPE: string;
  total_customer: number;
  total_default: number;
  default_rate_pct: number;
}

interface OccupationData {
  OCCUPATION_TYPE: string;
  total_customer: number;
  total_default: number;
  default_rate_pct: number;
}

interface IncomeData {
  income_group: string;
  total_customer: number;
  default_rate_pct: number;
}

interface AgeData {
  age_group: string;
  total_customer: number;
  default_rate_pct: number;
}

interface AvgLoanData {
  TARGET: number;
  total_customer: number;
  avg_credit_amount: number;
  avg_income: number;
  avg_credit_income_ratio: number;
}

interface GenderAssetData {
  CODE_GENDER: string;
  FLAG_OWN_CAR: string;
  FLAG_OWN_REALTY: string;
  total_customer: number;
  default_rate_pct: number;
}

interface CorrelationData {
  feature: string;
  correlation: number;
}

export default function BusinessAnalytics() {
  const [education, setEducation] = useState<EducationData[]>([]);
  const [occupation, setOccupation] = useState<OccupationData[]>([]);
  const [income, setIncome] = useState<IncomeData[]>([]);
  const [age, setAge] = useState<AgeData[]>([]);
  const [avgLoan, setAvgLoan] = useState<AvgLoanData[]>([]);
  const [genderAsset, setGenderAsset] = useState<GenderAssetData[]>([]);
  const [correlation, setCorrelation] = useState<CorrelationData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        setError(null);
        const [
          resEdu,
          resOcc,
          resInc,
          resAge,
          resLoan,
          resGen,
          resCorr,
        ] = await Promise.all([
          fetch("http://localhost:8000/analytics/default-by-education"),
          fetch("http://localhost:8000/analytics/default-by-occupation"),
          fetch("http://localhost:8000/analytics/default-by-income-group"),
          fetch("http://localhost:8000/analytics/default-by-age-group"),
          fetch("http://localhost:8000/analytics/avg-loan-by-default"),
          fetch("http://localhost:8000/analytics/default-by-gender"),
          fetch("http://localhost:8000/analytics/feature-correlation"),
        ]);

        if (
          !resEdu.ok ||
          !resOcc.ok ||
          !resInc.ok ||
          !resAge.ok ||
          !resLoan.ok ||
          !resGen.ok ||
          !resCorr.ok
        ) {
          throw new Error("Gagal mengambil data analitik dari FastAPI server.");
        }

        setEducation(await resEdu.json());
        setOccupation(await resOcc.json());
        setIncome(await resInc.json());
        setAge(await resAge.json());
        setAvgLoan(await resLoan.json());
        setGenderAsset(await resGen.json());
        setCorrelation(await resCorr.json());
      } catch (err: any) {
        setError(err.message || "Terjadi kesalahan saat memuat data.");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const maxEduRate = Math.max(...education.map((e) => e.default_rate_pct), 1);
  const maxOccRate = Math.max(...occupation.map((o) => o.default_rate_pct), 1);

  return (
    <>
      <div className="page-title">Business Analytics</div>
      <div className="page-subtitle">
        Analisis faktor demografi, ekonomi, dan aset terhadap tingkat risiko gagal bayar (default rate).
      </div>

      {loading && <div className="loading">Memuat data analisis bisnis...</div>}

      {error && (
        <div className="error-box">
          ⚠️ {error} Pastikan FastAPI backend berjalan di <code>http://localhost:8000</code>.
        </div>
      )}

      {!loading && !error && (
        <>
          {/* Section 1: Education */}
          <div className="card">
            <div className="card-title">Default Rate Berdasarkan Tingkat Pendidikan</div>
            <div className="two-col">
              <div className="bar-list">
                {education.map((item) => (
                  <div key={item.NAME_EDUCATION_TYPE} className="bar-item">
                    <div className="bar-label">{item.NAME_EDUCATION_TYPE}</div>
                    <div className="bar-track">
                      <div
                        className="bar-fill"
                        style={{ width: `${Math.round((item.default_rate_pct / maxEduRate) * 100)}%` }}
                      />
                    </div>
                    <div className="bar-val">{item.default_rate_pct}%</div>
                  </div>
                ))}
              </div>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Pendidikan</th>
                      <th>Total Customer</th>
                      <th>Total Default</th>
                      <th>Default Rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    {education.map((e) => (
                      <tr key={e.NAME_EDUCATION_TYPE}>
                        <td>{e.NAME_EDUCATION_TYPE}</td>
                        <td>{e.total_customer.toLocaleString("id-ID")}</td>
                        <td>{e.total_default.toLocaleString("id-ID")}</td>
                        <td><strong>{e.default_rate_pct}%</strong></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Section 2: Occupation */}
          <div className="card">
            <div className="card-title">Default Rate Berdasarkan Pekerjaan</div>
            <div className="two-col">
              <div className="bar-list">
                {occupation.slice(0, 10).map((item) => (
                  <div key={item.OCCUPATION_TYPE} className="bar-item">
                    <div className="bar-label">{item.OCCUPATION_TYPE}</div>
                    <div className="bar-track">
                      <div
                        className="bar-fill"
                        style={{ width: `${Math.round((item.default_rate_pct / maxOccRate) * 100)}%` }}
                      />
                    </div>
                    <div className="bar-val">{item.default_rate_pct}%</div>
                  </div>
                ))}
              </div>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Pekerjaan</th>
                      <th>Total Customer</th>
                      <th>Default Rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    {occupation.slice(0, 10).map((o) => (
                      <tr key={o.OCCUPATION_TYPE}>
                        <td>{o.OCCUPATION_TYPE}</td>
                        <td>{o.total_customer.toLocaleString("id-ID")}</td>
                        <td><strong>{o.default_rate_pct}%</strong></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Section 3: Income & Age */}
          <div className="two-col">
            <div className="card">
              <div className="card-title">Default Rate Berdasarkan Pendapatan</div>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Kelompok Income</th>
                      <th>Total Customer</th>
                      <th>Default Rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    {income.map((i) => (
                      <tr key={i.income_group}>
                        <td>{i.income_group}</td>
                        <td>{i.total_customer.toLocaleString("id-ID")}</td>
                        <td><strong>{i.default_rate_pct}%</strong></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="card">
              <div className="card-title">Default Rate Berdasarkan Kelompok Usia</div>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Kelompok Usia</th>
                      <th>Total Customer</th>
                      <th>Default Rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    {age.map((a) => (
                      <tr key={a.age_group}>
                        <td>{a.age_group}</td>
                        <td>{a.total_customer.toLocaleString("id-ID")}</td>
                        <td><strong>{a.default_rate_pct}%</strong></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Section 4: Average Loan & Gender/Asset */}
          <div className="card">
            <div className="card-title">Rata-rata Pinjaman Berdasarkan Status Default</div>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Status Customer</th>
                    <th>Total Customer</th>
                    <th>Rata-rata Pinjaman</th>
                    <th>Rata-rata Pendapatan</th>
                    <th>Credit / Income Ratio</th>
                  </tr>
                </thead>
                <tbody>
                  {avgLoan.map((l) => (
                    <tr key={l.TARGET}>
                      <td>
                        <strong>{l.TARGET === 1 ? "Gagal Bayar (Default)" : "Lancar (Non-Default)"}</strong>
                      </td>
                      <td>{l.total_customer.toLocaleString("id-ID")}</td>
                      <td>Rp {Math.round(l.avg_credit_amount).toLocaleString("id-ID")}</td>
                      <td>Rp {Math.round(l.avg_income).toLocaleString("id-ID")}</td>
                      <td>{l.avg_credit_income_ratio}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Section 5: Feature Correlation */}
          <div className="card">
            <div className="card-title">Korelasi Fitur Numerik terhadap Variabel TARGET (Gagal Bayar)</div>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Fitur Numerik</th>
                    <th>Koefisien Korelasi</th>
                    <th>Arah Pengaruh</th>
                  </tr>
                </thead>
                <tbody>
                  {correlation.map((c) => (
                    <tr key={c.feature}>
                      <td><code>{c.feature}</code></td>
                      <td><strong>{c.correlation?.toFixed(4)}</strong></td>
                      <td>
                        {c.correlation < 0 ? (
                          <span style={{ color: "var(--success)" }}>🔻 Menurunkan Risiko Gagal Bayar</span>
                        ) : (
                          <span style={{ color: "var(--danger)" }}>🔺 Meningkatkan Risiko Gagal Bayar</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </>
  );
}
