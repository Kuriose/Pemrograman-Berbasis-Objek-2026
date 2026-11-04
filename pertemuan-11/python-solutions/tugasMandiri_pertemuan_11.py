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

    def beli_produk(self, kode_produk: str, uang_masuk: int):
        # Cek apakah Kode Produk Valid
        if kode_produk not in self.inventaris:
            print(f"Kode {kode_produk} tidak terdaftar di dalam Mesin")
            return

        # Cek apakah Stok Barang Masih ada
        produk_terpilih = self.inventaris[kode_produk]

        if produk_terpilih.stok_produk <= 0: 
            print(f"{produk_terpilih.nama_produk} Habis!")
            return

        # Cek apakah Jumlah Uang Cukup
        if uang_masuk < produk_terpilih.harga_produk:
            print(f"Uang anda Kurang! Harga {produk_terpilih.nama_produk} sebesar Rp{produk_terpilih.harga_produk:,}")


if __name__ == "__main__": 
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
    mesin.beli_produk("M-00", 1000) # Berhasil
    print("\n")

    # Cek apakah Validasi Stok Barang Habis bisa Tertangkap
    mesin.beli_produk("M-04", 8000)
    print("\n")

    # Cek apakah Validasi Uang Tidak Cukup bisa Tertangkap
    mesin.beli_produk("M-02", 5000)
    print("\n")