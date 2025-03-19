from motor import Motor

class Parkir:
    def __init__(self, kapasitas):
        self.kapasitas = kapasitas
        self.daftar_motor = []

    def parkir_motor(self, motor):
        if len(self.daftar_motor) < self.kapasitas:
            self.daftar_motor.append(motor)
            print(f"Motor dengan plat nomor {motor.plat_nomor} berhasil diparkir.")
        else:
            print("Parkir penuh, tidak bisa menambahkan motor lagi.")

    def keluarkan_motor(self, plat_nomor):
        for motor in self.daftar_motor:
            if motor.plat_nomor == plat_nomor:
                self.daftar_motor.remove(motor)
                print(f"Motor dengan {plat_nomor} berhasil dikeluarkan.")
                return
        print(f"Motor dengan plat nomor {plat_nomor} tidak ditemukan.")

    def tampilkan_daftar_motor(self):
        if not self.daftar_motor:
            print("Parkir kosong.")
        else:
            print("Daftar motor yang parkir:")
            for motor in self.daftar_motor:
                print(motor.info())