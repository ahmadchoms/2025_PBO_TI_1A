import sqlite3
import os
from konfigurasi import DB_PATH

def setup_database():
    print(f"Memeriksa / membuat database di: {DB_PATH}")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deskripsi TEXT NOT NULL,
                jumlah REAL NOT NULL CHECK (jumlah > 0),
                kategori TEXT,
                tanggal DATE NOT NULL
            ); """
        print("Membuat tabel 'transaksi' (jika belum ada)...")
        cursor.execute(sql_create_table)
        conn.commit()
        print("Tabel 'transaksi' siap.")
        return True
    except sqlite3.Error as e:
        print(f"Error SQLite saat setup: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print("Koneksi DB setup ditutup.")

if __name__ == "__main__":
    print("Memulai Setup Database Pengeluaran...")
    if setup_database():
        print(f"\nSetup Database {os.path.basename(DB_PATH)} selesai. Database tersedia di {DB_PATH}.")
    else:
        print(f"\nSetup Database {os.path.basename(DB_PATH)} gagal.")
    print("Setup Database Selesai.")