import logging
from sqlalchemy import text

from src.database.load_data import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


BUILD_FEATURE_TABLE_QUERY = """
DROP TABLE IF EXISTS feature_table;

CREATE TABLE feature_table AS
SELECT
    cr.*,

    cs.bureau_credit_count,
    cs.bureau_active_credit_count,
    cs.bureau_avg_days_credit,
    cs.bureau_avg_credit_sum,
    cs.bureau_avg_credit_debt,
    cs.bureau_overdue_count,
    cs.prev_application_count,
    cs.prev_approved_count,
    cs.prev_refused_count,
    cs.prev_avg_amt_application,
    cs.prev_avg_amt_credit,
    cs.prev_avg_cnt_payment,
    cs.prev_approval_rate,

    pc.pos_record_count,
    pc.pos_avg_installment_count,
    pc.pos_avg_dpd,
    pc.pos_max_dpd,
    pc.pos_dpd_count,

    ip.installment_count,
    ip.avg_payment_diff,
    ip.avg_days_late,
    ip.late_payment_count,

    cc.cc_record_count,
    cc.cc_avg_balance,
    cc.cc_avg_credit_limit,
    cc.cc_utilization_ratio,
    cc.cc_dpd_count,

    bb.bureau_balance_record_count,
    bb.bureau_balance_dpd_count,
    bb.bureau_balance_closed_count,

    -- ============================================
    -- Derived Features (Milestone 19)
    -- ============================================

    ROUND(
        (cr."AMT_GOODS_PRICE" / NULLIF(cr."AMT_CREDIT", 0))::NUMERIC, 4
    )                                                              AS goods_price_credit_ratio,

    ROUND(
        (cr."AMT_INCOME_TOTAL" / NULLIF(cr."CNT_FAM_MEMBERS", 0))::NUMERIC, 2
    )                                                              AS income_per_family_member,

    CASE WHEN COALESCE(cs.bureau_overdue_count, 0) > 0 THEN 1 ELSE 0 END AS has_bureau_overdue_flag,
    CASE WHEN COALESCE(pc.pos_dpd_count, 0) > 0 THEN 1 ELSE 0 END        AS has_pos_dpd_flag,
    CASE WHEN COALESCE(cc.cc_dpd_count, 0) > 0 THEN 1 ELSE 0 END         AS has_cc_dpd_flag,

    (
        CASE WHEN COALESCE(cs.bureau_overdue_count, 0) > 0 THEN 1 ELSE 0 END +
        CASE WHEN COALESCE(pc.pos_dpd_count, 0) > 0 THEN 1 ELSE 0 END +
        CASE WHEN COALESCE(cc.cc_dpd_count, 0) > 0 THEN 1 ELSE 0 END
    )                                                              AS total_dpd_count,

    CASE WHEN COALESCE(cc.cc_utilization_ratio, 0) > 0.8 THEN 1 ELSE 0 END AS is_high_utilization,

    CASE
        WHEN COALESCE(ip.installment_count, 0) = 0 THEN NULL
        ELSE ROUND(
            (ip.late_payment_count::NUMERIC / ip.installment_count), 4
        )
    END                                                            AS late_payment_rate

FROM vw_credit_risk cr
LEFT JOIN vw_customer_summary   cs ON cr."SK_ID_CURR" = cs."SK_ID_CURR"
LEFT JOIN vw_pos_cash_agg       pc ON cr."SK_ID_CURR" = pc."SK_ID_CURR"
LEFT JOIN vw_installments_agg   ip ON cr."SK_ID_CURR" = ip."SK_ID_CURR"
LEFT JOIN vw_credit_card_agg    cc ON cr."SK_ID_CURR" = cc."SK_ID_CURR"
LEFT JOIN vw_bureau_balance_agg bb ON cr."SK_ID_CURR" = bb."SK_ID_CURR";
"""


def build_feature_table():
    logger.info("Building feature_table from all views...")

    with engine.begin() as conn:
        conn.execute(text(BUILD_FEATURE_TABLE_QUERY))

    logger.info("feature_table created successfully.")

    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM feature_table'))
        row_count = result.scalar()

    logger.info(f"feature_table row count: {row_count}")

    return row_count


if __name__ == "__main__":
    build_feature_table()