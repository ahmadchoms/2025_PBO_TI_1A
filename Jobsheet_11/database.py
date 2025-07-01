import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_db_connection() -> sqlite3.Connection | None:
    """
    Membuka koneksi baru ke database SQLite.

    Returns :
        sqlite3.Connection: Objek koneksi database jika berhasil, None jika gagal.
    """
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error [database.py] Gagal membuka koneksi DB: {e}")
        return None

def execute_query(query: str, params: tuple = None) -> int | None:
    """
    Menjalankan query non-SELECT (INSERT, UPDATE, DELETE).

    Args:
        query (str): Query SQL yang akan dijalankan.
        params (tuple, optional): Parameter untuk query. Default adalah None.

    Returns:
        int: ID baris terakhir yang dimauskan (untuk INSERT),
        None jika gagal.
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error [database.py] Gagal menjalankan query: {e} | Quert: {query[:60]}")
        conn.rollback()
        return None
    finally:
        conn.close()

def fetch_query(query: str, params: tuple = None, fetch_all: bool = True) -> list | dict | None:
    """
    Menjalankan query SELECT dan mengembalikan hasilnya.

    Args:
        query (str): Query SQL yang akan dijalankan.
        params (tuple, optional): Parameter untuk query. Default adalah None.
        fetch_all (bool, optional): Mengembalikan semua hasil (True) atau satu baris (False). Default adalah True.

    Returns:
        list: Daftar hasil query jika fetch_all=True, dict jika fetch_all=False.
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            return cursor.fetchall() if fetch_all else cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error [database.py] Gagal menjalankan query: {e} | Quert: {query[:60]}")
        return None
    finally:
        conn.close()

def get_dataframe(query: str, params: tuple = None) -> pd.DataFrame:
    """
    Menjalankan query SELECT dan mengembalikan hasilnya dalam bentuk DataFrame.

    Args:
        query (str): Query SQL yang akan dijalankan.
        params (tuple, optional): Parameter untuk query. Default adalah None.

    Returns:
        pd.DataFrame: DataFrame yang berisi hasil query.
    """
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        return pd.read_sql_query(query, conn, params=params)
    except sqlite3.Error as e:
        print(f"Error [database.py] Gagal menjalankan query: {e} | Quert: {query[:60]}")
        return pd.DataFrame()
    finally:
        conn.close()

def setup_database_initial() -> bool:
    """
    Memastikan tabel transaksi ada di database.

    Returns: 
        bool: True jika tabel berhasil dibuat atau sudah ada, False jika gagal.
    """
    print(f"Memeriksa / membuat tabel di database: {DB_PATH}")
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deskripsi TEXT NOT NULL,
            jumlah REAL NOT NULL CHECK (jumlah > 0),
            kategori TEXT,
            tanggal DATE NOT NULL
        ); """
        cursor.execute(sql_create_table)
        conn.commit()
        print(" -> Tabel transaksi siap.")
        return True
    except sqlite3.Error as e:
        print(f"Error [database.py] Gagal setup  tabel: {e}")
        return False
    finally:
        conn.close()