-- =====================================================================
-- CREDIT RISK INTELLIGENCE PLATFORM
-- Database Schema Documentation
-- =====================================================================
-- NOTE:
-- File ini adalah DOKUMENTASI, bukan script eksekusi.
-- Tabel-tabel raw dibuat secara otomatis oleh src/database/load_data.py
-- menggunakan pandas.DataFrame.to_sql().
--
-- Tujuan file ini: memberi gambaran cepat struktur & relasi database
-- tanpa perlu membuka DBeaver.
-- =====================================================================


-- =====================================================================
-- 1. application_train_raw / application_test_raw
-- =====================================================================
-- Grain      : 1 baris = 1 customer (aplikasi pinjaman saat ini)
-- Primary Key: SK_ID_CURR
-- Deskripsi  : Data utama customer saat mengajukan pinjaman.
--              application_train_raw punya kolom TARGET (0/1),
--              application_test_raw tidak punya TARGET (untuk prediksi).
-- Row count  : train = 307,511 | test = 48,744


-- =====================================================================
-- 2. bureau_raw
-- =====================================================================
-- Grain      : 1 baris = 1 kredit customer di bank/institusi LAIN
-- Primary Key: SK_ID_BUREAU
-- Foreign Key: SK_ID_CURR -> application_train_raw.SK_ID_CURR
-- Relasi     : 1 customer bisa punya banyak baris (one-to-many)
-- Row count  : 1,716,428


-- =====================================================================
-- 3. bureau_balance_raw
-- =====================================================================
-- Grain      : 1 baris = 1 bulan histori status kredit bureau
-- Foreign Key: SK_ID_BUREAU -> bureau_raw.SK_ID_BUREAU
-- Relasi     : 1 kredit bureau bisa punya banyak baris bulanan
-- Row count  : 27,299,925


-- =====================================================================
-- 4. previous_application_raw
-- =====================================================================
-- Grain      : 1 baris = 1 pengajuan pinjaman SEBELUMNYA di Home Credit
-- Primary Key: SK_ID_PREV
-- Foreign Key: SK_ID_CURR -> application_train_raw.SK_ID_CURR
-- Relasi     : 1 customer bisa punya banyak pengajuan sebelumnya
-- Row count  : 1,670,214


-- =====================================================================
-- 5. credit_card_balance_raw
-- =====================================================================
-- Grain      : 1 baris = 1 bulan histori saldo kartu kredit
-- Foreign Key: SK_ID_PREV -> previous_application_raw.SK_ID_PREV
--              SK_ID_CURR -> application_train_raw.SK_ID_CURR
-- Row count  : 3,840,312


-- =====================================================================
-- 6. installments_payments_raw
-- =====================================================================
-- Grain      : 1 baris = 1 cicilan (installment) yang dibayar/jatuh tempo
-- Foreign Key: SK_ID_PREV -> previous_application_raw.SK_ID_PREV
--              SK_ID_CURR -> application_train_raw.SK_ID_CURR
-- Row count  : 13,605,401


-- =====================================================================
-- 7. pos_cash_balance_raw
-- =====================================================================
-- Grain      : 1 baris = 1 bulan histori pinjaman POS/Cash
-- Foreign Key: SK_ID_PREV -> previous_application_raw.SK_ID_PREV
--              SK_ID_CURR -> application_train_raw.SK_ID_CURR
-- Row count  : 10,001,358


-- =====================================================================
-- RELATIONSHIP DIAGRAM (Text Version)
-- =====================================================================
--
-- application_train_raw / application_test_raw
--        |
--        | SK_ID_CURR
--        |
--        +----------------> bureau_raw
--        |                      |
--        |                      | SK_ID_BUREAU
--        |                      v
--        |                 bureau_balance_raw
--        |
--        +----------------> previous_application_raw
--                                |
--                                | SK_ID_PREV
--                                +----------> credit_card_balance_raw
--                                +----------> installments_payments_raw
--                                +----------> pos_cash_balance_raw
--
-- =====================================================================


-- =====================================================================
-- PLANNED VIEWS (Milestone 12-13)
-- =====================================================================
-- vw_customer_summary : agregasi bureau + previous_application per customer
-- vw_credit_risk      : subset fitur fokus risk-related untuk analysis
-- feature_table        : hasil akhir feature engineering untuk ML (Phase 5)
-- =====================================================================