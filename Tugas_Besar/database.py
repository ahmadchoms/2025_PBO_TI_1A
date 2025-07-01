import sqlite3
from typing import List, Optional, Tuple
from model import Barang, Gudang, Transaksi

class DatabaseManager:
    """Kelas untuk mengelola koneksi dan operasi database SQLite"""
    
    def __init__(self, db_path: str = "logistik.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Membuat koneksi ke database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Inisialisasi tabel-tabel database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabel barang
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS barang (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    kategori TEXT NOT NULL,
                    satuan TEXT NOT NULL,
                    harga_satuan REAL NOT NULL,
                    deskripsi TEXT
                )
            ''')
            
            # Tabel gudang
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gudang (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    lokasi TEXT NOT NULL,
                    kapasitas_maksimum INTEGER NOT NULL,
                    kapasitas_terpakai INTEGER DEFAULT 0
                )
            ''')
            
            # Tabel transaksi
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transaksi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barang_id INTEGER NOT NULL,
                    gudang_id INTEGER NOT NULL,
                    jenis TEXT NOT NULL CHECK (jenis IN ('masuk', 'keluar')),
                    jumlah INTEGER NOT NULL,
                    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    keterangan TEXT,
                    FOREIGN KEY (barang_id) REFERENCES barang (id),
                    FOREIGN KEY (gudang_id) REFERENCES gudang (id)
                )
            ''')
            
            # Tabel stok barang per gudang
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stok_barang (
                    barang_id INTEGER NOT NULL,
                    gudang_id INTEGER NOT NULL,
                    jumlah INTEGER DEFAULT 0,
                    PRIMARY KEY (barang_id, gudang_id),
                    FOREIGN KEY (barang_id) REFERENCES barang (id),
                    FOREIGN KEY (gudang_id) REFERENCES gudang (id)
                )
            ''')
            
            conn.commit()
    
    # CRUD Operations untuk Barang
    def tambah_barang(self, barang: Barang) -> int:
        """Menambah barang baru ke database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO barang (nama, kategori, satuan, harga_satuan, deskripsi)
                VALUES (?, ?, ?, ?, ?)
            ''', (barang.nama, barang.kategori, barang.satuan, 
                  barang.harga_satuan, barang.deskripsi))
            return cursor.lastrowid
    
    def get_semua_barang(self) -> List[Barang]:
        """Mengambil semua barang dari database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM barang ORDER BY nama')
            rows = cursor.fetchall()
            return [Barang(id=row['id'], nama=row['nama'], kategori=row['kategori'],
                          satuan=row['satuan'], harga_satuan=row['harga_satuan'],
                          deskripsi=row['deskripsi']) for row in rows]
    
    def get_barang_by_id(self, barang_id: int) -> Optional[Barang]:
        """Mengambil barang berdasarkan ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM barang WHERE id = ?', (barang_id,))
            row = cursor.fetchone()
            if row:
                return Barang(id=row['id'], nama=row['nama'], kategori=row['kategori'],
                             satuan=row['satuan'], harga_satuan=row['harga_satuan'],
                             deskripsi=row['deskripsi'])
            return None
    
    # CRUD Operations untuk Gudang
    def tambah_gudang(self, gudang: Gudang) -> int:
        """Menambah gudang baru ke database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO gudang (nama, lokasi, kapasitas_maksimum, kapasitas_terpakai)
                VALUES (?, ?, ?, ?)
            ''', (gudang.nama, gudang.lokasi, gudang.kapasitas_maksimum, gudang.kapasitas_terpakai))
            return cursor.lastrowid
    
    def get_semua_gudang(self) -> List[Gudang]:
        """Mengambil semua gudang dari database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM gudang ORDER BY nama')
            rows = cursor.fetchall()
            return [Gudang(id=row['id'], nama=row['nama'], lokasi=row['lokasi'],
                          kapasitas_maksimum=row['kapasitas_maksimum'],
                          kapasitas_terpakai=row['kapasitas_terpakai']) for row in rows]
    
    def get_gudang_by_id(self, gudang_id: int) -> Optional[Gudang]:
        """Mengambil gudang berdasarkan ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM gudang WHERE id = ?', (gudang_id,))
            row = cursor.fetchone()
            if row:
                return Gudang(id=row['id'], nama=row['nama'], lokasi=row['lokasi'],
                             kapasitas_maksimum=row['kapasitas_maksimum'],
                             kapasitas_terpakai=row['kapasitas_terpakai'])
            return None
    
    def update_kapasitas_gudang(self, gudang_id: int, kapasitas_terpakai: int):
        """Update kapasitas terpakai gudang"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE gudang SET kapasitas_terpakai = ? WHERE id = ?
            ''', (kapasitas_terpakai, gudang_id))
    
    # CRUD Operations untuk Transaksi
    def tambah_transaksi(self, transaksi: Transaksi) -> int:
        """Menambah transaksi baru ke database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transaksi (barang_id, gudang_id, jenis, jumlah, tanggal, keterangan)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (transaksi.barang_id, transaksi.gudang_id, transaksi.jenis,
                  transaksi.jumlah, transaksi.tanggal, transaksi.keterangan))
            return cursor.lastrowid
    
    def get_semua_transaksi(self, limit: int = 100) -> List[Tuple]:
        """Mengambil semua transaksi dengan detail barang dan gudang"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.id, b.nama as nama_barang, g.nama as nama_gudang,
                       t.jenis, t.jumlah, t.tanggal, t.keterangan
                FROM transaksi t
                JOIN barang b ON t.barang_id = b.id
                JOIN gudang g ON t.gudang_id = g.id
                ORDER BY t.tanggal DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
    
    def get_transaksi_by_barang(self, barang_id: int) -> List[Tuple]:
        """Mengambil transaksi berdasarkan barang"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.id, b.nama as nama_barang, g.nama as nama_gudang,
                       t.jenis, t.jumlah, t.tanggal, t.keterangan
                FROM transaksi t
                JOIN barang b ON t.barang_id = b.id
                JOIN gudang g ON t.gudang_id = g.id
                WHERE t.barang_id = ?
                ORDER BY t.tanggal DESC
            ''', (barang_id,))
            return cursor.fetchall()
    
    # Operations untuk Stok Barang
    def update_stok_barang(self, barang_id: int, gudang_id: int, jumlah: int):
        """Update atau insert stok barang di gudang"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO stok_barang (barang_id, gudang_id, jumlah)
                VALUES (?, ?, ?)
            ''', (barang_id, gudang_id, jumlah))
    
    def get_stok_barang(self, barang_id: int, gudang_id: int) -> int:
        """Mengambil stok barang di gudang tertentu"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT jumlah FROM stok_barang 
                WHERE barang_id = ? AND gudang_id = ?
            ''', (barang_id, gudang_id))
            row = cursor.fetchone()
            return row['jumlah'] if row else 0
    
    def get_semua_stok(self) -> List[Tuple]:
        """Mengambil semua stok barang dengan detail"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT b.nama as nama_barang, g.nama as nama_gudang,
                       s.jumlah, b.satuan
                FROM stok_barang s
                JOIN barang b ON s.barang_id = b.id
                JOIN gudang g ON s.gudang_id = g.id
                WHERE s.jumlah > 0
                ORDER BY b.nama, g.nama
            ''')
            return cursor.fetchall()
    
    def get_stok_by_gudang(self, gudang_id: int) -> List[Tuple]:
        """Mengambil stok barang di gudang tertentu"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT b.nama as nama_barang, s.jumlah, b.satuan, b.kategori
                FROM stok_barang s
                JOIN barang b ON s.barang_id = b.id
                WHERE s.gudang_id = ? AND s.jumlah > 0
                ORDER BY b.nama
            ''', (gudang_id,))
            return cursor.fetchall()