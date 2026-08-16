-- =====================================================================
-- VIEW: vw_credit_risk
-- Tujuan: Subset fitur risk-related dari application_train_raw
--         untuk kebutuhan analisis bisnis (Phase 4)
-- Grain : 1 baris = 1 SK_ID_CURR
-- =====================================================================

DROP VIEW IF EXISTS vw_credit_risk;

CREATE VIEW vw_credit_risk AS

SELECT
    "SK_ID_CURR",
    "TARGET",

    -- Demografi
    "CODE_GENDER",
    "DAYS_BIRTH",
    ROUND((ABS("DAYS_BIRTH") / 365.0)::NUMERIC, 1)   AS age_years,
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "CNT_CHILDREN",
    "CNT_FAM_MEMBERS",

    -- Pekerjaan & Income
    "NAME_INCOME_TYPE",
    "OCCUPATION_TYPE",
    "AMT_INCOME_TOTAL",
    "DAYS_EMPLOYED",
    CASE
        WHEN "DAYS_EMPLOYED" > 0 THEN NULL  -- anomaly value (365243) -> jadi NULL
        ELSE ROUND((ABS("DAYS_EMPLOYED") / 365.0)::NUMERIC, 1)
    END                                       AS employment_years,

    -- Kredit
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    ROUND(("AMT_CREDIT" / NULLIF("AMT_INCOME_TOTAL", 0))::NUMERIC, 2)  AS credit_income_ratio,
    ROUND(("AMT_ANNUITY" / NULLIF("AMT_INCOME_TOTAL", 0))::NUMERIC, 4) AS annuity_income_ratio,

    -- Kepemilikan Aset
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY",

    -- External Score (fitur paling prediktif di dataset ini)
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3"

FROM application_train_raw;