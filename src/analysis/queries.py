import pandas as pd
from sqlalchemy import text

from src.database.load_data import engine


def get_default_rate_by_education():
    query = """
        SELECT
            "NAME_EDUCATION_TYPE",
            COUNT(*)                                   AS total_customer,
            SUM("TARGET")                               AS total_default,
            ROUND(AVG("TARGET")::NUMERIC * 100, 2)      AS default_rate_pct
        FROM vw_credit_risk
        GROUP BY "NAME_EDUCATION_TYPE"
        ORDER BY default_rate_pct DESC;
    """
    return pd.read_sql(text(query), engine)


def get_default_rate_by_occupation():
    query = """
        SELECT
            "OCCUPATION_TYPE",
            COUNT(*)                                   AS total_customer,
            SUM("TARGET")                               AS total_default,
            ROUND(AVG("TARGET")::NUMERIC * 100, 2)      AS default_rate_pct
        FROM vw_credit_risk
        WHERE "OCCUPATION_TYPE" IS NOT NULL
        GROUP BY "OCCUPATION_TYPE"
        ORDER BY default_rate_pct DESC;
    """
    return pd.read_sql(text(query), engine)


def get_default_rate_by_income_group():
    query = """
        SELECT
            CASE
                WHEN "AMT_INCOME_TOTAL" < 100000 THEN '1. < 100K'
                WHEN "AMT_INCOME_TOTAL" < 200000 THEN '2. 100K - 200K'
                WHEN "AMT_INCOME_TOTAL" < 300000 THEN '3. 200K - 300K'
                WHEN "AMT_INCOME_TOTAL" < 500000 THEN '4. 300K - 500K'
                ELSE '5. > 500K'
            END                                          AS income_group,
            COUNT(*)                                     AS total_customer,
            SUM("TARGET")                                AS total_default,
            ROUND(AVG("TARGET")::NUMERIC * 100, 2)       AS default_rate_pct
        FROM vw_credit_risk
        GROUP BY income_group
        ORDER BY income_group;
    """
    return pd.read_sql(text(query), engine)


def get_default_rate_by_age_group():
    query = """
        SELECT
            CASE
                WHEN age_years < 25 THEN '1. < 25'
                WHEN age_years < 35 THEN '2. 25 - 34'
                WHEN age_years < 45 THEN '3. 35 - 44'
                WHEN age_years < 55 THEN '4. 45 - 54'
                WHEN age_years < 65 THEN '5. 55 - 64'
                ELSE '6. 65+'
            END                                          AS age_group,
            COUNT(*)                                     AS total_customer,
            SUM("TARGET")                                AS total_default,
            ROUND(AVG("TARGET")::NUMERIC * 100, 2)       AS default_rate_pct
        FROM vw_credit_risk
        GROUP BY age_group
        ORDER BY age_group;
    """
    return pd.read_sql(text(query), engine)


def get_avg_loan_by_default_status():
    query = """
        SELECT
            "TARGET",
            COUNT(*)                                     AS total_customer,
            ROUND(AVG("AMT_CREDIT")::NUMERIC, 0)         AS avg_credit_amount,
            ROUND(AVG("AMT_INCOME_TOTAL")::NUMERIC, 0)   AS avg_income,
            ROUND(AVG(credit_income_ratio)::NUMERIC, 2)  AS avg_credit_income_ratio
        FROM vw_credit_risk
        GROUP BY "TARGET";
    """
    return pd.read_sql(text(query), engine)


def get_default_rate_by_gender_ownership():
    query = """
        SELECT
            "CODE_GENDER",
            "FLAG_OWN_CAR",
            "FLAG_OWN_REALTY",
            COUNT(*)                                     AS total_customer,
            ROUND(AVG("TARGET")::NUMERIC * 100, 2)       AS default_rate_pct
        FROM vw_credit_risk
        GROUP BY "CODE_GENDER", "FLAG_OWN_CAR", "FLAG_OWN_REALTY"
        ORDER BY default_rate_pct DESC;
    """
    return pd.read_sql(text(query), engine)


def get_feature_correlation():
    query = """
        SELECT feature, correlation
        FROM (
            SELECT 'AMT_INCOME_TOTAL' AS feature, CORR("TARGET", "AMT_INCOME_TOTAL") AS correlation FROM vw_credit_risk
            UNION ALL
            SELECT 'AMT_CREDIT', CORR("TARGET", "AMT_CREDIT") FROM vw_credit_risk
            UNION ALL
            SELECT 'AMT_ANNUITY', CORR("TARGET", "AMT_ANNUITY") FROM vw_credit_risk
            UNION ALL
            SELECT 'credit_income_ratio', CORR("TARGET", credit_income_ratio) FROM vw_credit_risk
            UNION ALL
            SELECT 'annuity_income_ratio', CORR("TARGET", annuity_income_ratio) FROM vw_credit_risk
            UNION ALL
            SELECT 'age_years', CORR("TARGET", age_years) FROM vw_credit_risk
            UNION ALL
            SELECT 'employment_years', CORR("TARGET", employment_years) FROM vw_credit_risk
            UNION ALL
            SELECT 'CNT_CHILDREN', CORR("TARGET", "CNT_CHILDREN") FROM vw_credit_risk
            UNION ALL
            SELECT 'CNT_FAM_MEMBERS', CORR("TARGET", "CNT_FAM_MEMBERS") FROM vw_credit_risk
            UNION ALL
            SELECT 'EXT_SOURCE_1', CORR("TARGET", "EXT_SOURCE_1") FROM vw_credit_risk
            UNION ALL
            SELECT 'EXT_SOURCE_2', CORR("TARGET", "EXT_SOURCE_2") FROM vw_credit_risk
            UNION ALL
            SELECT 'EXT_SOURCE_3', CORR("TARGET", "EXT_SOURCE_3") FROM vw_credit_risk
        ) AS correlation_table
        ORDER BY ABS(correlation) DESC;
    """
    return pd.read_sql(text(query), engine)