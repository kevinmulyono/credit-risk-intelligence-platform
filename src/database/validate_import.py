import pandas as pd
from sqlalchemy import text

from src.database.load_data import engine, DATA_FOLDER, csv_files


def count_csv_rows(path):
    """
    Hitung jumlah baris CSV tanpa load semua kolom ke memori.
    Cukup baca 1 kolom saja -> jauh lebih ringan untuk file besar
    seperti bureau_balance.csv (27 juta baris).
    """
    df = pd.read_csv(path, usecols=[0])
    return len(df)


def count_db_rows(table_name):
    with engine.connect() as conn:
        result = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
        return result.scalar()


def run_validation():
    print(f"{'File':<35}{'CSV Rows':<15}{'DB Rows':<15}{'Match'}")
    print("-" * 75)

    all_match = True

    for filename, table_name in csv_files.items():
        path = DATA_FOLDER / filename

        csv_rows = count_csv_rows(path)
        db_rows = count_db_rows(table_name)

        match = "✅" if csv_rows == db_rows else "❌"
        if csv_rows != db_rows:
            all_match = False

        print(f"{filename:<35}{csv_rows:<15}{db_rows:<15}{match}")

    print("-" * 75)
    if all_match:
        print("\nSemua tabel MATCH. Import valid 100%.")
    else:
        print("\nADA MISMATCH! Cek tabel yang ❌ di atas — jangan lanjut ke milestone berikutnya dulu.")


if __name__ == "__main__":
    run_validation()