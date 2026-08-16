-- =====================================================================
-- VIEW: vw_pos_cash_agg
-- Sumber: pos_cash_balance_raw
-- Grain : 1 baris = 1 SK_ID_CURR
-- =====================================================================

DROP VIEW IF EXISTS vw_pos_cash_agg;

CREATE VIEW vw_pos_cash_agg AS
SELECT
    "SK_ID_CURR",
    COUNT(*)                                                          AS pos_record_count,
    ROUND(AVG("CNT_INSTALMENT")::NUMERIC, 2)                          AS pos_avg_installment_count,
    ROUND(AVG("SK_DPD")::NUMERIC, 2)                                  AS pos_avg_dpd,
    MAX("SK_DPD")                                                     AS pos_max_dpd,
    SUM(CASE WHEN "SK_DPD" > 0 THEN 1 ELSE 0 END)                     AS pos_dpd_count
FROM pos_cash_balance_raw
GROUP BY "SK_ID_CURR";


-- =====================================================================
-- VIEW: vw_installments_agg
-- Sumber: installments_payments_raw
-- Grain : 1 baris = 1 SK_ID_CURR
-- =====================================================================

DROP VIEW IF EXISTS vw_installments_agg;

CREATE VIEW vw_installments_agg AS
SELECT
    "SK_ID_CURR",
    COUNT(*)                                                          AS installment_count,
    ROUND(AVG("AMT_INSTALMENT" - "AMT_PAYMENT")::NUMERIC, 2)          AS avg_payment_diff,
    ROUND(AVG("DAYS_ENTRY_PAYMENT" - "DAYS_INSTALMENT")::NUMERIC, 2)  AS avg_days_late,
    SUM(CASE WHEN "DAYS_ENTRY_PAYMENT" > "DAYS_INSTALMENT" THEN 1 ELSE 0 END) AS late_payment_count
FROM installments_payments_raw
GROUP BY "SK_ID_CURR";


-- =====================================================================
-- VIEW: vw_credit_card_agg
-- Sumber: credit_card_balance_raw
-- Grain : 1 baris = 1 SK_ID_CURR
-- =====================================================================

DROP VIEW IF EXISTS vw_credit_card_agg;

CREATE VIEW vw_credit_card_agg AS
SELECT
    "SK_ID_CURR",
    COUNT(*)                                                          AS cc_record_count,
    ROUND(AVG("AMT_BALANCE")::NUMERIC, 2)                             AS cc_avg_balance,
    ROUND(AVG("AMT_CREDIT_LIMIT_ACTUAL")::NUMERIC, 2)                 AS cc_avg_credit_limit,
    ROUND(
        (AVG("AMT_BALANCE") / NULLIF(AVG("AMT_CREDIT_LIMIT_ACTUAL"), 0))::NUMERIC, 4
    )                                                                  AS cc_utilization_ratio,
    SUM(CASE WHEN "SK_DPD" > 0 THEN 1 ELSE 0 END)                     AS cc_dpd_count
FROM credit_card_balance_raw
GROUP BY "SK_ID_CURR";


-- =====================================================================
-- VIEW: vw_bureau_balance_agg
-- Sumber: bureau_balance_raw (join lewat bureau_raw untuk dapat SK_ID_CURR)
-- Grain : 1 baris = 1 SK_ID_CURR
-- =====================================================================

DROP VIEW IF EXISTS vw_bureau_balance_agg;

CREATE VIEW vw_bureau_balance_agg AS
SELECT
    b."SK_ID_CURR",
    COUNT(*)                                                          AS bureau_balance_record_count,
    SUM(CASE WHEN bb."STATUS" IN ('1','2','3','4','5') THEN 1 ELSE 0 END) AS bureau_balance_dpd_count,
    SUM(CASE WHEN bb."STATUS" = 'C' THEN 1 ELSE 0 END)                AS bureau_balance_closed_count
FROM bureau_balance_raw bb
INNER JOIN bureau_raw b ON bb."SK_ID_BUREAU" = b."SK_ID_BUREAU"
GROUP BY b."SK_ID_CURR";