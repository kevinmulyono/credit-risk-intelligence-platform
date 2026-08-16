import os
import logging
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

# ==========================
# Logging Configuration
# ==========================
# Path absolut berdasarkan lokasi file ini, supaya tetap benar
# baik dijalankan langsung maupun di-import dari notebook
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "etl.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==========================
# PostgreSQL Configuration
# ==========================
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_DATABASE")

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# ==========================
# Data Folder
# ==========================
DATA_FOLDER = Path("data/raw")

csv_files = {
    "application_train.csv": "application_train_raw",
    "application_test.csv": "application_test_raw",
    "bureau.csv": "bureau_raw",
    "bureau_balance.csv": "bureau_balance_raw",
    "previous_application.csv": "previous_application_raw",
    "credit_card_balance.csv": "credit_card_balance_raw",
    "installments_payments.csv": "installments_payments_raw",
    "POS_CASH_balance.csv": "pos_cash_balance_raw",
}


def run_import():
    for filename, table_name in csv_files.items():
        path = DATA_FOLDER / filename

        print(f"\nLoading {filename}...")

        df = pd.read_csv(path)

        print(df.shape)

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False,
            chunksize=5000,
            method="multi"
        )

        print(f"{table_name} imported successfully!")

    print("\nAll datasets imported successfully!")


if __name__ == "__main__":
    run_import()