class Motor:
    def __init__(self, plat_nomor, pemilik):
        self.plat_nomor = plat_nomor
        self.pemilik = pemilik

    def info(self):
        return f"Motor dengan plat nomor {self.plat_nomor} milik {self.pemilik}"