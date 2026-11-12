import os

# === WARNA TERMINAL (ANSI escape code) ===
class Warna:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    HIJAU   = "\033[92m"
    MERAH   = "\033[91m"
    KUNING  = "\033[93m"
    BIRU    = "\033[94m"
    CYAN    = "\033[96m"
    ABU     = "\033[90m"

LEBAR = 84

# Mencetak Garis
def garis(karakter="─", lebar=LEBAR):
    print(karakter * lebar)

# Mencetak header teks tertentu
def judul(teks: str, lebar=LEBAR):
    print("┌" + "─" * (lebar - 2) + "┐")
    print("│" + teks.center(lebar - 2) + "│")
    print("└" + "─" * (lebar - 2) + "┘")

# Memberikan input agar pembaca dapat membaca output di terminal dengan mudah
def jeda():
    """Pengganti os.system('pause') agar bisa berjalan di semua OS (Windows/Linux/Mac)."""
    input(f"{Warna.ABU}Tekan ENTER untuk melanjutkan...{Warna.RESET}")


class Produk:
    def __init__(self, kode_produk: str, nama_produk: str, harga_produk: int, stok_produk: int):
        self.kode_produk = kode_produk
        self.nama_produk = nama_produk
        self.harga_produk = harga_produk
        self.stok_produk = stok_produk

    # Magic method, digunakan pada saat nanti ingin mencetak produk yang ada di dalam mesin minuman
    def __str__(self):
        status = f"{self.stok_produk} pcs" if self.stok_produk > 0 else "HABIS"
        warna_stok = Warna.HIJAU if self.stok_produk > 0 else Warna.MERAH
        return (
            f" {Warna.CYAN}[{self.kode_produk}]{Warna.RESET} "
            f"{self.nama_produk:<25} "
            f"Rp{self.harga_produk:>7,}   "
            f"{warna_stok}{status:>8}{Warna.RESET}"
        )


class MesinMinuman:
    def __init__(self):
        # Dibuat Dictionary untuk menyimpan Minuman-Minuman
        # Key: Kode Produk      |     Value: Objek Produk (Seluruh data Produk)
        self.inventaris = {}
        self.riwayat_penjualan = {}
        self.total_pendapatan = 0

    # Method awal untuk menambahkan minuman ke dalam mesin
    def tambah_produk(self, produk: Produk):
        # Setiap minuman memiliki kode unik-nya masing-masing. Bagian ini memeriksa duplikat dari kode unik-tersebut
        if produk.kode_produk in self.inventaris:
            print(f"{Warna.KUNING}[!] Produk dengan kode {produk.kode_produk} sudah ada di dalam mesin{Warna.RESET}")

        # Menyimpan Informasi Minuman ke dalam Mesin
        self.inventaris[produk.kode_produk] = produk
        print(f"{Warna.HIJAU}[V] Berhasil menambahkan {produk.nama_produk} ke dalam Mesin!{Warna.RESET}")

    # Method yang digunakan untuk mencetak struk setelah proses transaksi
    def cetak_struk(self):
        print()
        judul("STRUK / LAPORAN PENJUALAN")

        if not self.riwayat_penjualan:
            print(" Belum ada transaksi yang tercatat.")
        else:
            total_item_terjual = 0
            print(f" {'Nama Produk':<20}{'Jumlah':>10}")
            garis("·")
            for nama_produk, jumlah in self.riwayat_penjualan.items():
                print(f" {nama_produk:<20}{jumlah:>7} pcs")
                total_item_terjual += jumlah
            garis()
            print(f" {'Total Item Terjual':<20}{total_item_terjual:>7} pcs")

        garis()
        print(f" {Warna.BOLD}Total Pendapatan: Rp{self.total_pendapatan:,}{Warna.RESET}")
        garis()

        print(" Sisa Stok Produk di Mesin")
        garis("·")
        if not self.inventaris:
            print(" Mesin Kosong.")
        else:
            for produk in self.inventaris.values():
                warna_stok = Warna.HIJAU if produk.stok_produk > 0 else Warna.MERAH
                status_stok = f"{produk.stok_produk} pcs" if produk.stok_produk > 0 else "HABIS (0 pcs)"
                print(f" [{produk.kode_produk}] {produk.nama_produk:<25}: {warna_stok}{status_stok}{Warna.RESET}")
        garis()
        print(f"{Warna.CYAN}Terima kasih telah menggunakan Mesin Minuman Otomatis!{Warna.RESET}\n")

    # Method yang menampilkan daftar produk yang disimpan didalam mesin minuman
    def lihat_produk(self): 
        judul("DAFTAR PRODUK TERSEDIA")
        print(f" {'Kode':<6}{'Nama Produk':<25}{'Harga':>10}   {'Stok':>8}")
        garis("·")
        for minuman in self.inventaris.values():
            print(minuman)
        garis()

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

        # Memproses transaksi minuman yang sudah dipilih
        print(f"{Warna.HIJAU}[V] Berhasil Membeli {produk_terpilih.nama_produk}{Warna.RESET}")
        produk_terpilih.stok_produk -= 1
        sisa_uang = uang_masuk - produk_terpilih.harga_produk

        # Bagian yang mencatat produk yang dibeli beserta jumlahnya
        if produk_terpilih.nama_produk in self.riwayat_penjualan:
            self.riwayat_penjualan[produk_terpilih.nama_produk] += 1
        else:
            self.riwayat_penjualan[produk_terpilih.nama_produk] = 1
        self.total_pendapatan += produk_terpilih.harga_produk # Mencatat total pendapatan dari mesin

        # Bagian yang mengecek sisa uang
        if sisa_uang == 0: # Jika true, maka tidak kembalian (uangnya pas)
            print(f"{Warna.CYAN}    Uang anda Pas{Warna.RESET}")
            return
        print(f"{Warna.KUNING}    Sisa Kembalian Anda: Rp{sisa_uang:,}{Warna.RESET}") # Selain dari itu, maka kembaliannya lebih dari 0 Rupiah


# === ERROR HANDLING CLASSESS ===
# Catatan: Karena bahasa yang digunakan adalah Python, maka tidak ada pemisahan checked/unchecked seperti di Java. 
class MesinError(Exception):
    """Induk Semua Error yang Berhubungan dengan Mesin"""


class ProdukTidakAdaError(MesinError):
    """Muncul Saat Kode Produk yang Dimasukkan dengan Kode Produk yang ada pada Mesin"""
    def __init__(self, kode_masuk: str):
        self.kode_error = kode_masuk
        super().__init__(f"Kode {self.kode_error} Tidak ada terdaftar didalam Mesin! Silahkan Masukkan Kode yang benar.") # Pesan yang diberikan ketika Error


class StokHabisError(MesinError):
    """Muncul Saat Stok Produk yang ada didalam Mesin berjumlah nol (Stok Habis)"""
    def __init__(self, nama_produk: str):
        self.nama_error = nama_produk
        super().__init__(f"{self.nama_error} Kehabisan Stok! Silahkan pilih Minuman yang Lain.") # Pesan yang diberikan ketika Error


class UangKurangError(MesinError):
    """Muncul Saat Nominal Uang yang Dimasukkan Kurang dari Harga Produk yang ada"""
    def __init__(self, harga_produk: int, uang_masuk: int):
        self.harga_produk = harga_produk # Harga Produk aslinya dalam mesin minuman
        self.uang_masuk = uang_masuk # Uang yang dimasukkan pembeli ke dalam mesin

        # Memberikan Teks Error Saldo tidak cukup
        super().__init__(f"Saldo Anda Tidak Cukup! Saldo yang dimasukkan sebesar Rp{uang_masuk:,} \n"
                         f"Harga Minuman sebesar Rp{harga_produk:,}, jadi Saldo anda kurang Rp{harga_produk - uang_masuk:,}")

    @property
    def kekurangan(self) -> int: # Mengembalikan berapa banyak kembalian pembeli
        return self.harga_produk - self.uang_masuk


if __name__ == "__main__":
    # Inisiasi Produk Awal Mesin Minuman
    daftar_minuman = [
        {"kode": "M-01", "nama": "Teh Botol", "harga": 5000, "stok": 10},
        {"kode": "M-02", "nama": "Kopi Susu", "harga": 8000, "stok": 5},
        {"kode": "M-03", "nama": "Air Mineral", "harga": 4000, "stok": 15},
        {"kode": "M-04", "nama": "Soda Jeruk", "harga": 7000, "stok": 0},
        {"kode": "M-05", "nama": "Energy Drink", "harga": 6500, "stok": 4},
        {"kode": "M-06", "nama": "Kopi Cappuccino", "harga": 4500, "stok": 10},
        
        # Nama Minuman di generate melalui website: https://fungenerators.com/random/thing/beverage
        {"kode": "M-07", "nama": "Milkshake", "harga": 4000, "stok": 8}, 
        {"kode": "M-08", "nama": "Lemonade", "harga": 9000, "stok": 2}, 
        {"kode": "M-09", "nama": "Jus Jeruk", "harga": 5500, "stok": 9},
        {"kode": "M-10", "nama": "Diet Coke", "harga": 8599, "stok": 6}
    ]

    # Inisiasi struk belanja
    struk = []

    # Inisiasi Mesin Minuman
    mesin = MesinMinuman()

    # Buat Header untuk tampilan program 
    judul("MESIN MINUMAN OTOMATIS", LEBAR)
    print()

    # Tambahkan Produk-Produk Minuman ke dalam Mesin dengan menggunakan perulangan
    for item in daftar_minuman:
        mesin.tambah_produk(Produk(item["kode"], item["nama"], item["harga"], item["stok"]))

    # Memberi Jarak serta mencetak daftar produk
    print()
    mesin.lihat_produk()
    print()

    # Jumlah Pengujian: Minimal enam Pengujian, bebas mau situasi berhasil atau tidak
    daftar_pengujian = [
        {"kode": "M-08", "uang": 9000}, # Pengujian Berhasil
        {"kode": "M-01", "uang": 5000}, # Pengujian Berhasil
        {"kode": "M-100", "uang": 5000}, # Pengujian Gagal
        {"kode": "M-02", "uang": 10000}, # Pengujian Berhasil
        {"kode": "M-01", "uang": 9000}, # Pengujian Berhasil
        {"kode": "M-04", "uang": 7000}, # Pengujian Gagal
        {"kode": "M-08", "uang": 12000}, # Pengujian Berhasil
        {"kode": "M-03", "uang": 3000}, # Pengujian Gagal
        {"kode": "M-05", "uang": 7000}, # Pengujian Berhasil
        {"kode": "M-08", "uang": 12000}, # Pengujian Gagal
    ]

    # Melakukan Pengujian untuk masing-masing entri yang ada pada list daftar_pengujian
    for i, test in enumerate(daftar_pengujian, start=1):
        print()
        judul(f"TRANSAKSI #{i}  |  Kode: {test['kode']}  |  Uang: Rp{test['uang']:,}")
        try:
            mesin.beli_produk(test["kode"], test["uang"])
        except ProdukTidakAdaError as e:
            print(f"{Warna.MERAH}[!] {e}{Warna.RESET}")
        except StokHabisError as e:
            print(f"{Warna.MERAH}[!] {e}{Warna.RESET}")
        except UangKurangError as e:
            print(f"{Warna.MERAH}[!] {e}{Warna.RESET}")
        except MesinError as e:
            print(f"{Warna.MERAH}[!] {e}{Warna.RESET}")
        finally:
            garis()
            print(f"{Warna.ABU}Mesin siap melayani pembeli berikutnya!{Warna.RESET}")
            jeda()

    # Mencetak Struk setelah Pembelian sudah selesai
    mesin.cetak_struk()