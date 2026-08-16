-- =====================================================================
-- VIEW: vw_customer_summary
-- Tujuan: Agregasi histori bureau & previous_application per customer
-- Grain : 1 baris = 1 SK_ID_CURR
-- =====================================================================

DROP VIEW IF EXISTS vw_customer_summary;

CREATE VIEW vw_customer_summary AS

WITH bureau_agg AS (
    SELECT
        "SK_ID_CURR",
        COUNT(*)                                   AS bureau_credit_count,
        SUM(CASE WHEN "CREDIT_ACTIVE" = 'Active' THEN 1 ELSE 0 END) AS bureau_active_credit_count,
        AVG("DAYS_CREDIT")                          AS bureau_avg_days_credit,
        AVG("AMT_CREDIT_SUM")                       AS bureau_avg_credit_sum,
        AVG("AMT_CREDIT_SUM_DEBT")                  AS bureau_avg_credit_debt,
        SUM(CASE WHEN "CREDIT_DAY_OVERDUE" > 0 THEN 1 ELSE 0 END)   AS bureau_overdue_count
    FROM bureau_raw
    GROUP BY "SK_ID_CURR"
),

previous_app_agg AS (
    SELECT
        "SK_ID_CURR",
        COUNT(*)                                                    AS prev_application_count,
        SUM(CASE WHEN "NAME_CONTRACT_STATUS" = 'Approved' THEN 1 ELSE 0 END) AS prev_approved_count,
        SUM(CASE WHEN "NAME_CONTRACT_STATUS" = 'Refused' THEN 1 ELSE 0 END)  AS prev_refused_count,
        AVG("AMT_APPLICATION")                                      AS prev_avg_amt_application,
        AVG("AMT_CREDIT")                                           AS prev_avg_amt_credit,
        AVG("CNT_PAYMENT")                                          AS prev_avg_cnt_payment
    FROM previous_application_raw
    GROUP BY "SK_ID_CURR"
)

SELECT
    a."SK_ID_CURR",

    COALESCE(b.bureau_credit_count, 0)          AS bureau_credit_count,
    COALESCE(b.bureau_active_credit_count, 0)   AS bureau_active_credit_count,
    b.bureau_avg_days_credit,
    b.bureau_avg_credit_sum,
    b.bureau_avg_credit_debt,
    COALESCE(b.bureau_overdue_count, 0)         AS bureau_overdue_count,

    COALESCE(p.prev_application_count, 0)       AS prev_application_count,
    COALESCE(p.prev_approved_count, 0)          AS prev_approved_count,
    COALESCE(p.prev_refused_count, 0)           AS prev_refused_count,
    p.prev_avg_amt_application,
    p.prev_avg_amt_credit,
    p.prev_avg_cnt_payment,

    CASE
        WHEN COALESCE(p.prev_application_count, 0) = 0 THEN NULL
        ELSE ROUND(
            COALESCE(p.prev_approved_count, 0)::NUMERIC
            / p.prev_application_count, 4
        )
    END AS prev_approval_rate

FROM application_train_raw a
LEFT JOIN bureau_agg b        ON a."SK_ID_CURR" = b."SK_ID_CURR"
LEFT JOIN previous_app_agg p  ON a."SK_ID_CURR" = p."SK_ID_CURR";