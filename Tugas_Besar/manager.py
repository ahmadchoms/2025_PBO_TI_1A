from typing import List, Dict, Tuple
from datetime import datetime
from model import Barang, Gudang, Transaksi
from database import DatabaseManager

class LogistikManager:
    """Kelas untuk mengelola logika bisnis aplikasi logistik"""
    
    def __init__(self, db_path: str = "logistik.db"):
        self.db = DatabaseManager(db_path)
    
    # Management Barang
    def tambah_barang(self, nama: str, kategori: str, satuan: str, 
                     harga_satuan: float, deskripsi: str = "") -> Dict[str, any]:
        """Menambah barang baru dengan validasi"""
        try:
            # Validasi input
            if not nama.strip():
                return {"success": False, "message": "Nama barang tidak boleh kosong"}
            if not kategori.strip():
                return {"success": False, "message": "Kategori tidak boleh kosong"}
            if not satuan.strip():
                return {"success": False, "message": "Satuan tidak boleh kosong"}
            if harga_satuan < 0:
                return {"success": False, "message": "Harga satuan tidak boleh negatif"}
            
            # Cek duplikasi nama barang
            barang_existing = self.db.get_semua_barang()
            if any(b.nama.lower() == nama.lower() for b in barang_existing):
                return {"success": False, "message": "Nama barang sudah ada"}
            
            barang = Barang(
                nama=nama.strip(),
                kategori=kategori.strip(),
                satuan=satuan.strip(),
                harga_satuan=harga_satuan,
                deskripsi=deskripsi.strip()
            )
            
            barang_id = self.db.tambah_barang(barang)
            return {"success": True, "message": "Barang berhasil ditambahkan", "id": barang_id}
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def get_semua_barang(self) -> List[Barang]:
        """Mengambil semua barang"""
        return self.db.get_semua_barang()
    
    # Management Gudang
    def tambah_gudang(self, nama: str, lokasi: str, kapasitas_maksimum: int) -> Dict[str, any]:
        """Menambah gudang baru dengan validasi"""
        try:
            # Validasi input
            if not nama.strip():
                return {"success": False, "message": "Nama gudang tidak boleh kosong"}
            if not lokasi.strip():
                return {"success": False, "message": "Lokasi tidak boleh kosong"}
            if kapasitas_maksimum <= 0:
                return {"success": False, "message": "Kapasitas maksimum harus lebih dari 0"}
            
            # Cek duplikasi nama gudang
            gudang_existing = self.db.get_semua_gudang()
            if any(g.nama.lower() == nama.lower() for g in gudang_existing):
                return {"success": False, "message": "Nama gudang sudah ada"}
            
            gudang = Gudang(
                nama=nama.strip(),
                lokasi=lokasi.strip(),
                kapasitas_maksimum=kapasitas_maksimum,
                kapasitas_terpakai=0
            )
            
            gudang_id = self.db.tambah_gudang(gudang)
            return {"success": True, "message": "Gudang berhasil ditambahkan", "id": gudang_id}
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def get_semua_gudang(self) -> List[Gudang]:
        """Mengambil semua gudang"""
        return self.db.get_semua_gudang()
    
    # Management Transaksi
    def proses_transaksi(self, barang_id: int, gudang_id: int, jenis: str, 
                        jumlah: int, keterangan: str = "") -> Dict[str, any]:
        """Memproses transaksi masuk atau keluar dengan validasi lengkap"""
        try:
            # Validasi input dasar
            if jumlah <= 0:
                return {"success": False, "message": "Jumlah harus lebih dari 0"}
            if jenis not in ['masuk', 'keluar']:
                return {"success": False, "message": "Jenis transaksi harus 'masuk' atau 'keluar'"}
            
            # Validasi keberadaan barang dan gudang
            barang = self.db.get_barang_by_id(barang_id)
            if not barang:
                return {"success": False, "message": "Barang tidak ditemukan"}
            
            gudang = self.db.get_gudang_by_id(gudang_id)
            if not gudang:
                return {"success": False, "message": "Gudang tidak ditemukan"}
            
            # Ambil stok saat ini
            stok_saat_ini = self.db.get_stok_barang(barang_id, gudang_id)
            
            # Validasi khusus berdasarkan jenis transaksi
            if jenis == 'keluar':
                if stok_saat_ini < jumlah:
                    return {"success": False, 
                           "message": f"Stok tidak mencukupi. Stok saat ini: {stok_saat_ini}"}
                stok_baru = stok_saat_ini - jumlah
                kapasitas_baru = gudang.kapasitas_terpakai - jumlah
            else:  # jenis == 'masuk'
                if gudang.kapasitas_terpakai + jumlah > gudang.kapasitas_maksimum:
                    sisa_kapasitas = gudang.sisa_kapasitas()
                    return {"success": False, 
                           "message": f"Kapasitas gudang tidak mencukupi. Sisa kapasitas: {sisa_kapasitas}"}
                stok_baru = stok_saat_ini + jumlah
                kapasitas_baru = gudang.kapasitas_terpakai + jumlah
            
            # Proses transaksi
            transaksi = Transaksi(
                barang_id=barang_id,
                gudang_id=gudang_id,
                jenis=jenis,
                jumlah=jumlah,
                tanggal=datetime.now(),
                keterangan=keterangan.strip()
            )
            
            # Simpan ke database
            transaksi_id = self.db.tambah_transaksi(transaksi)
            self.db.update_stok_barang(barang_id, gudang_id, stok_baru)
            self.db.update_kapasitas_gudang(gudang_id, kapasitas_baru)
            
            return {
                "success": True, 
                "message": f"Transaksi {jenis} berhasil diproses",
                "id": transaksi_id,
                "stok_baru": stok_baru
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def get_histori_transaksi(self, limit: int = 100) -> List[Tuple]:
        """Mengambil histori transaksi"""
        return self.db.get_semua_transaksi(limit)
    
    def get_transaksi_by_barang(self, barang_id: int) -> List[Tuple]:
        """Mengambil transaksi berdasarkan barang"""
        return self.db.get_transaksi_by_barang(barang_id)
    
    # Management Stok
    def get_semua_stok(self) -> List[Tuple]:
        """Mengambil semua stok barang"""
        return self.db.get_semua_stok()
    
    def get_stok_by_gudang(self, gudang_id: int) -> List[Tuple]:
        """Mengambil stok barang di gudang tertentu"""
        return self.db.get_stok_by_gudang(gudang_id)
    
    def get_ringkasan_stok(self) -> Dict[str, any]:
        """Mengambil ringkasan stok untuk dashboard"""
        try:
            semua_barang = self.db.get_semua_barang()
            semua_gudang = self.db.get_semua_gudang()
            semua_stok = self.db.get_semua_stok()
            
            # Hitung total nilai stok
            total_nilai_stok = 0
            total_item_stok = 0
            
            for stok in semua_stok:
                nama_barang = stok[0]  # nama_barang
                jumlah = stok[2]  # jumlah
                
                # Cari harga barang
                barang = next((b for b in semua_barang if b.nama == nama_barang), None)
                if barang:
                    total_nilai_stok += barang.harga_satuan * jumlah
                    total_item_stok += jumlah
            
            # Hitung statistik gudang
            total_kapasitas = sum(g.kapasitas_maksimum for g in semua_gudang)
            total_terpakai = sum(g.kapasitas_terpakai for g in semua_gudang)
            persentase_terpakai = (total_terpakai / total_kapasitas * 100) if total_kapasitas > 0 else 0
            
            return {
                "total_barang": len(semua_barang),
                "total_gudang": len(semua_gudang),
                "total_item_stok": total_item_stok,
                "total_nilai_stok": total_nilai_stok,
                "total_kapasitas": total_kapasitas,
                "total_terpakai": total_terpakai,
                "persentase_terpakai": persentase_terpakai,
                "sisa_kapasitas": total_kapasitas - total_terpakai
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_barang_stok_rendah(self, batas_minimum: int = 10) -> List[Dict]:
        """Mengambil barang dengan stok rendah"""
        try:
            semua_stok = self.db.get_semua_stok()
            stok_rendah = []
            
            # Kelompokkan stok per barang
            stok_per_barang = {}
            for stok in semua_stok:
                nama_barang = stok[0]
                jumlah = stok[2]
                
                if nama_barang in stok_per_barang:
                    stok_per_barang[nama_barang] += jumlah
                else:
                    stok_per_barang[nama_barang] = jumlah
            
            # Cari barang dengan stok rendah
            for nama_barang, total_stok in stok_per_barang.items():
                if total_stok <= batas_minimum:
                    stok_rendah.append({
                        "nama_barang": nama_barang,
                        "total_stok": total_stok
                    })
            
            return sorted(stok_rendah, key=lambda x: x['total_stok'])
            
        except Exception as e:
            return []
    
    def get_gudang_hampir_penuh(self, persentase_batas: float = 80.0) -> List[Dict]:
        """Mengambil gudang yang hampir penuh"""
        try:
            semua_gudang = self.db.get_semua_gudang()
            gudang_hampir_penuh = []
            
            for gudang in semua_gudang:
                persentase = gudang.persentase_terpakai()
                if persentase >= persentase_batas:
                    gudang_hampir_penuh.append({
                        "nama_gudang": gudang.nama,
                        "lokasi": gudang.lokasi,
                        "persentase_terpakai": persentase,
                        "sisa_kapasitas": gudang.sisa_kapasitas()
                    })
            
            return sorted(gudang_hampir_penuh, key=lambda x: x['persentase_terpakai'], reverse=True)
            
        except Exception as e:
            return []