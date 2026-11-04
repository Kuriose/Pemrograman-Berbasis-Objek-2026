class Produk: 
    def __init__(self, kode_produk: str, nama_produk: str, harga_produk: int, stok_produk: int):
        self.kode_produk = kode_produk
        self.nama_produk = nama_produk
        self.harga_produk = harga_produk
        self.stok_produk = stok_produk

    def __str__(self):
        return f"[{self.kode_produk}] {self.nama_produk} - Rp{self.harga_produk:,} (stok: {self.stok_produk})"

class MesinMinuman: 
    def __init__(self):
        # Dibuat Dictionary untuk menyimpan Minuman-Minuman
        # Key: Kode Produk      |     Value: Objek Produk (Seluruh data Produk)
        self.inventaris = {}

    def tambah_produk(self, produk: Produk):
        # Setiap minuman memiliki kode unik-nya masing-masing. Bagian ini memeriksa duplikat dari kode unik-tersebut
        if produk.kode_produk in self.inventaris: 
            print(f"Produk dengan kode {produk.kode_produk} sudah ada di dalam mesin")

        # Menyimpan Informasi Minuman ke dalam Mesin
        self.inventaris[produk.kode_produk] = produk
        print(f"Berhasil menambahkan {produk.nama_produk} ke dalam Mesin!") 


    def lihat_produk(self):
        for minuman in self.inventaris.values():
            print(minuman)

    def beli_produk(self, kode_masuk: str, uang_masuk: int):
        # Cek apakah Kode Produk Valid
        if kode_masuk not in self.inventaris:
            # print(f"Kode {kode_produk} tidak terdaftar didalam Mesin")
            # return

            raise ProdukTidakAdaError(kode_masuk)

        # Cek apakah Stok Barang Masih ada
        produk_terpilih = self.inventaris[kode_masuk]

        if produk_terpilih.stok_produk <= 0: 
            # print(f"{produk_terpilih.nama_produk} Habis!")
            # return

            raise StokHabisError(produk_terpilih.nama_produk)

        # Cek apakah Jumlah Uang Cukup
        if uang_masuk < produk_terpilih.harga_produk:
            # print(f"Uang anda Kurang! Harga {produk_terpilih.nama_produk} sebesar Rp{produk_terpilih.harga_produk:,}")

            raise UangKurangError(produk_terpilih.harga_produk, uang_masuk)

        print("lewat")

# === ERROR HANDLING CLASSESS ===
class MesinError(Exception):
    """Induk Semua Error yang Berhubungan dengan Mesin"""

class ProdukTidakAdaError(MesinError):
    """Muncul Saat Kode Produk yang Dimasukkan dengan Kode Produk yang ada pada Mesin"""
    def __init__(self, kode_masuk: str):
        super().__init__(f"Kode {kode_masuk} Tidak ada terdaftar didalam Mesin! Silahkan Masukkan Kode yang benar.")

class StokHabisError(MesinError): 
    """Muncul Saat Stok Produk yang ada didalam Mesin berjumlah nol (Stok Habis)"""
    def __init__(self, nama_produk: str):
        super().__init__(f"{nama_produk} Kehabisan Stok! Silahkan pilih Minuman yang Lain.")

class UangKurangError(MesinError):
    """Muncul Saat Nominal Uang yang Dimasukkan Kurang dari Harga Produk yang ada"""
    def __init__(self, harga_produk: int, harga_masuk: int):
        super().__init__(f"Saldo tidak cukup: Saldo Rp{harga_masuk}, "
                         f"diminta Rp{harga_produk}")
        self.harga_produk = harga_produk
        self.harga_masuk = harga_masuk

    @property
    def kekurangan(self) -> int: 
        return self.harga_produk - self.harga_masuk

if __name__ == "__main__": 
    try: 
        # Inisiasi Produk Awal
        p1 = Produk("M-01", "Teh Botol", 5000, 10)
        p2 = Produk("M-02", "Kopi Susu", 8000, 5)
        p3 = Produk("M-03", "Air Mineral", 4000, 15)
        p4 = Produk("M-04", "Soda Jeruk", 7000, 0)

        # Inisiasi Mesin Minuman
        mesin = MesinMinuman()

        # Tambahkan Produk-Produk Minuman ke dalam Mesin
        mesin.tambah_produk(p1)
        mesin.tambah_produk(p2)
        mesin.tambah_produk(p3)
        mesin.tambah_produk(p4)
        print("\n")

        mesin.lihat_produk()
        print("\n")

        # Cek apakah Validasi Kode Produk Salah bisa Tertangkap
        # mesin.beli_produk("M-00", 1000) # Berhasil
        # print("\n")

        # Cek apakah Validasi Stok Barang Habis bisa Tertangkap
        # mesin.beli_produk("M-04", 8000)
        # print("\n")

        # Cek apakah Validasi Uang Tidak Cukup bisa Tertangkap
        mesin.beli_produk("M-02", 5000)
        print("\n")
    except MesinError as e: 
        print(e)