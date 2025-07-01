import datetime
import locale

class Transaksi:
    def __init__(self, deskripsi: str, jumlah: float, kategori: str, tanggal: datetime.date | str, id_transaksi: int | None = None):
        self.id = id_transaksi
        self.deskripsi = str(deskripsi) if deskripsi else "Tanpa Deskripsi"

        try:
            jumlah_float = float(jumlah)
            self.jumlah = jumlah_float if jumlah_float > 0 else 0.0
            if jumlah_float <= 0:
                print(f"Peringatan Jumlah {jumlah} harus positif.")
        except ValueError:
            self.jumlah = 0.0
            print(f"Peringan Jumlah {jumlah} tidak valid.")

        self.kategori = str(kategori) if kategori else "Lainnya"
        if isinstance(tanggal, datetime.date):
            self.tanggal = tanggal
        elif isinstance(tanggal, str):
            try:
                self.tanggal = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
            except ValueError:
                self.tanggal = datetime.datetime.now().date()
                print(f"Peringatan Tanggal {tanggal} tidak valid. Menggunakan tanggal saat ini.")
        else:
            self.tanggal = datetime.date.today()
            print(f"Peringatan Tipe tanggal {type(tanggal)} tidak valid. Menggunakan tanggal saat ini.")
    
    def __repr__(self) -> str:
        """
        Mengembalikan representasi string dari objek Transaksi.

        Returns:
            str: String yang menggambarkan detail transaksi dengan format mata uang lokal.
        """
        try:
            locale.setlocale(locale.LC_ALL, "id_ID.UTF-8")
            jumlah_str = locale.format_string("%.0f", self.jumlah, grouping=True)
        except locale.Error:
            jumlah_str = f"{self.jumlah:.0f}"

        return f"Transaksi ID: {self.id}, Tanggal: {self.tanggal.strftime('%Y-%m-%d')}, Deskripsi: {self.deskripsi}, Jumlah: {jumlah_str}, Kategori: {self.kategori}"
    
    def to_dict(self) -> dict:
        """
        Mengembalikan representasi transaksi sebagai dictionary.

        Returns:
            dict: Dictionary berisi atribut transaksi.
        """
        return {
            "id": self.id,
            "deskripsi": self.deskripsi,
            "jumlah": self.jumlah,
            "kategori": self.kategori,
            "tanggal": self.tanggal.strftime("%Y-%m-%d")
        }