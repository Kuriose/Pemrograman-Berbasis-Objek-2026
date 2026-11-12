import os

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
        self.riwayat_penjualan = {}
        self.total_pendapatan = 0


    def tambah_produk(self, produk: Produk):
        # Setiap minuman memiliki kode unik-nya masing-masing. Bagian ini memeriksa duplikat dari kode unik-tersebut
        if produk.kode_produk in self.inventaris: 
            print(f"Produk dengan kode {produk.kode_produk} sudah ada di dalam mesin")

        # Menyimpan Informasi Minuman ke dalam Mesin
        self.inventaris[produk.kode_produk] = produk
        print(f"Berhasil menambahkan {produk.nama_produk} ke dalam Mesin!") 

    def cetak_struk(self):
        print("\n" + "-" * 60)
        print("==> Struk / Laporan Penjualan")
        print("-" * 60)

        if not self.riwayat_penjualan:
            print("Belum ada transaksi yang tercatat.")
        else:
            total_item_terjual = 0
            for nama_produk, jumlah in self.riwayat_penjualan.items():
                print(f" - {nama_produk} x {jumlah}")
                total_item_terjual += jumlah
            print("-" * 60)
            print(f"Total Keseluruhan Item Terjual: {total_item_terjual}")
        print("-" * 60)
        print(f"Total Pendapatan: Rp{self.total_pendapatan:,}")
        
        print("-" * 60)
        print("Sisa Stok Produk di Mesin")        
        if not self.inventaris:
            print("Mesin Kosong.")
        else:
            for produk in self.inventaris.values():
                status_stok = f"{produk.stok_produk} pcs" if produk.stok_produk > 0 else "HABIS (0 pcs)"
                print(f"-> [{produk.kode_produk}] {produk.nama_produk:<12} : {status_stok}")
        print("-" * 60)


    def lihat_produk(self):
        for minuman in self.inventaris.values():
            print(minuman)

    def beli_produk(self, kode_masuk: str, uang_masuk: int):
        # Cek apakah Kode Produk Valid
        if kode_masuk not in self.inventaris:
            raise ProdukTidakAdaError(kode_masuk)

        # Cek apakah Stok Barang Masih ada
        produk_terpilih = self.inventaris[kode_masuk]

        if produk_terpilih.stok_produk <= 0: 
            raise StokHabisError(produk_terpilih.nama_produk)

        # Cek apakah Jumlah Uang Cukup
        if uang_masuk < produk_terpilih.harga_produk:
            raise UangKurangError(produk_terpilih.harga_produk, uang_masuk)

        print(f"Berhasil Membeli {produk_terpilih.nama_produk}")
        produk_terpilih.stok_produk -= 1
        sisa_uang = uang_masuk - produk_terpilih.harga_produk
        # struk.append(produk_terpilih)

        if produk_terpilih.nama_produk in self.riwayat_penjualan:
            self.riwayat_penjualan[produk_terpilih.nama_produk] += 1
        else:
            self.riwayat_penjualan[produk_terpilih.nama_produk] = 1

        self.total_pendapatan += produk_terpilih.harga_produk

        if sisa_uang == 0:
            print("Uang anda Pas")
            return
        print(f"Sisa Kembalian Anda: Rp{sisa_uang:,}")

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
        self.harga_produk = harga_produk
        self.harga_masuk = harga_masuk
        
        super().__init__(f"Saldo Anda Tidak Cukup! Saldo yang dimasukkan sebesar Rp{harga_masuk:,} \n"
                         f"Harga Minuman sebesar Rp{harga_produk:,}, jadi Saldo anda kurang Rp{harga_masuk:,}")

    @property
    def kekurangan(self) -> int: 
        return self.harga_produk - self.harga_masuk

if __name__ == "__main__": 
    # Inisiasi Produk Awal
    p1 = Produk("M-01", "Teh Botol", 5000, 10)
    p2 = Produk("M-02", "Kopi Susu", 8000, 5)
    p3 = Produk("M-03", "Air Mineral", 4000, 15)
    p4 = Produk("M-04", "Soda Jeruk", 7000, 0)
    p5 = Produk("M-05", "Energy Drink", 6500, 4)

    # Inisiasi struk belanja
    struk = []

    # Inisiasi Mesin Minuman
    mesin = MesinMinuman()

    # Tambahkan Produk-Produk Minuman ke dalam Mesin
    mesin.tambah_produk(p1)
    mesin.tambah_produk(p2)
    mesin.tambah_produk(p3)
    mesin.tambah_produk(p4)
    mesin.tambah_produk(p5)
    print("\n")

    mesin.lihat_produk()
    print("\n")

    # Jumlah Pengujian: Minimal enam Pengujian, bebas mau situasi berhasil atau tidak 
    daftar_pengujian = [
        {
            "kode": "M-01", # Pengujian Berhasil 
            "uang": 5000, 
        }, 
        {
            "kode": "M-100", # Pengujian Gagal
            "uang": 5000
        }, 
        {
            "kode": "M-02", # Pengujian Berhasil
            "uang": 10000
        }, 
        {
            "kode": "M-04", # Pengujian Gagal 
            "uang": 7000
        }, 
        {
            "kode": "M-03", # Pengujian Gagal 
            "uang": 3000
        }, 
        {
            "kode": "M-05", # Pengujian Berhasil
            "uang": 7000
        }
    ]

    for i, test in enumerate(daftar_pengujian, start=1):
        print("\n=== MELAKUKAN TRANSAKSI =======================")
        try:
            mesin.beli_produk(test["kode"], test["uang"])
        except ProdukTidakAdaError as e: 
            print(e)
        except StokHabisError as e: 
            print(e)
        except UangKurangError as e: 
            print(e)
        except MesinError as e: 
            print(e)
        finally: 
            print("Mesin siap melayani pembeli berikutnya!")
            os.system("pause")

    # print(struk)
    # for i in struk:
    #     print(i)
    mesin.cetak_struk()