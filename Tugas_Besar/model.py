from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Barang:
    """Kelas untuk merepresentasikan barang"""
    id: Optional[int] = None
    nama: str = ""
    kategori: str = ""
    satuan: str = ""
    harga_satuan: float = 0.0
    deskripsi: str = ""
    
    def __post_init__(self):
        if self.harga_satuan < 0:
            raise ValueError("Harga satuan tidak boleh negatif")

@dataclass
class Gudang:
    """Kelas untuk merepresentasikan gudang"""
    id: Optional[int] = None
    nama: str = ""
    lokasi: str = ""
    kapasitas_maksimum: int = 0
    kapasitas_terpakai: int = 0
    
    def __post_init__(self):
        if self.kapasitas_maksimum < 0:
            raise ValueError("Kapasitas maksimum tidak boleh negatif")
        if self.kapasitas_terpakai < 0:
            raise ValueError("Kapasitas terpakai tidak boleh negatif")
        if self.kapasitas_terpakai > self.kapasitas_maksimum:
            raise ValueError("Kapasitas terpakai tidak boleh melebihi kapasitas maksimum")
    
    def sisa_kapasitas(self) -> int:
        """Menghitung sisa kapasitas gudang"""
        return self.kapasitas_maksimum - self.kapasitas_terpakai
    
    def persentase_terpakai(self) -> float:
        """Menghitung persentase kapasitas yang terpakai"""
        if self.kapasitas_maksimum == 0:
            return 0.0
        return (self.kapasitas_terpakai / self.kapasitas_maksimum) * 100

@dataclass
class Transaksi:
    """Kelas untuk merepresentasikan transaksi barang"""
    id: Optional[int] = None
    barang_id: int = 0
    gudang_id: int = 0
    jenis: str = ""  # 'masuk' atau 'keluar'
    jumlah: int = 0
    tanggal: datetime = None
    keterangan: str = ""
    
    def __post_init__(self):
        if self.tanggal is None:
            self.tanggal = datetime.now()
        if self.jumlah <= 0:
            raise ValueError("Jumlah transaksi harus lebih dari 0")
        if self.jenis not in ['masuk', 'keluar']:
            raise ValueError("Jenis transaksi harus 'masuk' atau 'keluar'")

@dataclass
class StokBarang:
    """Kelas untuk merepresentasikan stok barang di gudang"""
    barang_id: int
    gudang_id: int
    jumlah: int = 0
    
    def __post_init__(self):
        if self.jumlah < 0:
            raise ValueError("Jumlah stok tidak boleh negatif")