from datetime import date
from models import (
    AlatKampus,
    AlatElektronik,
    AlatLaboratorium,
    Pengguna,
    Mahasiswa,
    Dosen,
    Admin,
    TransaksiPeminjaman,
)
from .penyimpanan import PenyimpananJSON


class LayananPeminjaman:
    """Service utama yang mengorkestrasi katalog alat, peminjaman, pengembalian, dan statistik."""

    def __init__(self, penyimpanan: PenyimpananJSON):
        self._penyimpanan = penyimpanan
        self._alat, self._pengguna, self._transaksi = self._penyimpanan.muat()
        if not self._alat and not self._pengguna:
            self._inisialisasi_data_awal()

    def _inisialisasi_data_awal(self) -> None:
        data_alat = [
            AlatElektronik("ELK-001", "Proyektor Epson EB-X51", 4, 327, "Epson"),
            AlatElektronik("ELK-002", "Kamera DSLR Canon EOS 2000D", 2, 18, "Canon"),
            AlatElektronik("ELK-003", "Speaker Portable Bluetooth", 3, 40, "JBL"),
            AlatLaboratorium("LAB-001", "Crimping Tool & LAN Tester Kit", 6, "Jaringan Komputer", False),
            AlatLaboratorium("LAB-002", "Oscilloscope Digital Rigol", 2, "Elektronika", True),
            AlatLaboratorium("LAB-003", "Arduino Uno & Sensor Starter Kit", 5, "IoT & Sistem Tertanam", True),
        ]
        data_pengguna = [
            Mahasiswa("G1F025020", "Asri Ayu Julita", "Sistem Informasi"),
            Mahasiswa("G1F025014", "Mahasiswa Uji 2", "Sistem Informasi"),
            Dosen("0012058701", "Dr. Della Maulidiya, M.Kom", "Teknik"),
            Admin("ADM-001", "Petugas Lab SI", "Laboratorium SI"),
        ]
        for a in data_alat:
            self._alat[a.kode_alat] = a
        for p in data_pengguna:
            self._pengguna[p.id_pengguna] = p
        self._penyimpanan.simpan(self._alat, self._pengguna, self._transaksi)

    def daftar_alat(self, kata_kunci: str = "", jenis: str = "") -> list[AlatKampus]:
        hasil = list(self._alat.values())
        if kata_kunci.strip():
            q = kata_kunci.strip().lower()
            hasil = [
                a for a in hasil
                if q in a.kode_alat.lower() or q in a.nama.lower() or q in a.info_spesifikasi().lower()
            ]
        if jenis.strip():
            hasil = [a for a in hasil if a.jenis_alat().lower() == jenis.strip().lower()]
        return hasil

    def daftar_pengguna(self) -> list[Pengguna]:
        return list(self._pengguna.values())

    def daftar_transaksi(self, hanya_aktif: bool = False) -> list[TransaksiPeminjaman]:
        if hanya_aktif:
            return [t for t in self._transaksi if t.status == "Dipinjam"]
        return list(reversed(self._transaksi))

    def tambah_alat(self, id_admin: str, alat_baru: AlatKampus) -> AlatKampus:
        admin = self._pengguna.get(id_admin.strip().upper())
        if not admin or not admin.boleh_kelola_alat():
            raise PermissionError("Hanya Admin yang berhak menambahkan alat ke inventaris.")
        if alat_baru.kode_alat in self._alat:
            raise ValueError(f"Kode alat '{alat_baru.kode_alat}' sudah terdaftar.")
        self._alat[alat_baru.kode_alat] = alat_baru
        self._penyimpanan.simpan(self._alat, self._pengguna, self._transaksi)
        return alat_baru

    def pinjam_alat(
        self,
        id_pengguna: str,
        kode_alat: str,
        jumlah: int = 1,
        tanggal_pinjam: str | None = None,
    ) -> TransaksiPeminjaman:
        pengguna = self._pengguna.get(id_pengguna.strip().upper())
        if not pengguna:
            raise ValueError(f"Pengguna dengan ID '{id_pengguna}' tidak ditemukan.")

        alat = self._alat.get(kode_alat.strip().upper())
        if not alat:
            raise ValueError(f"Alat dengan kode '{kode_alat}' tidak ditemukan.")

        if jumlah <= 0:
            raise ValueError("Jumlah unit peminjaman harus minimal 1.")

        unit_aktif = sum(
            t.jumlah
            for t in self._transaksi
            if t.id_pengguna == pengguna.id_pengguna and t.status == "Dipinjam"
        )
        if unit_aktif + jumlah > pengguna.maks_unit_pinjam():
            raise ValueError(
                f"{pengguna.peran()} maksimal meminjam {pengguna.maks_unit_pinjam()} unit aktif "
                f"(saat ini sedang meminjam {unit_aktif} unit)."
            )

        alat.kurangi_stok(jumlah)

        tgl_pinjam = tanggal_pinjam or date.today().isoformat()
        batas_kembali = TransaksiPeminjaman.hitung_batas_kembali(
            tgl_pinjam, pengguna.batas_hari_pinjam()
        )
        id_trx = f"TRX-{len(self._transaksi) + 1:04d}"

        trx = TransaksiPeminjaman(
            id_transaksi=id_trx,
            id_pengguna=pengguna.id_pengguna,
            nama_pengguna=pengguna.nama,
            peran_pengguna=pengguna.peran(),
            kode_alat=alat.kode_alat,
            nama_alat=alat.nama,
            jumlah=jumlah,
            tanggal_pinjam=tgl_pinjam,
            batas_kembali=batas_kembali,
        )
        self._transaksi.append(trx)
        self._penyimpanan.simpan(self._alat, self._pengguna, self._transaksi)
        return trx

    def kembalikan_alat(
        self, id_transaksi: str, tanggal_kembali: str | None = None
    ) -> TransaksiPeminjaman:
        trx = next(
            (t for t in self._transaksi if t.id_transaksi == id_transaksi.strip().upper()),
            None,
        )
        if not trx:
            raise ValueError(f"Transaksi '{id_transaksi}' tidak ditemukan.")

        alat = self._alat.get(trx.kode_alat)
        if not alat:
            raise ValueError(f"Data alat '{trx.kode_alat}' tidak ditemukan.")

        tgl_kembali = tanggal_kembali or date.today().isoformat()
        # Pemanggilan polimorfik: alat.hitung_denda berbeda antara Elektronik & Laboratorium
        trx.tandai_kembali(tgl_kembali, alat.hitung_denda)
        alat.tambah_stok(trx.jumlah)
        self._penyimpanan.simpan(self._alat, self._pengguna, self._transaksi)
        return trx

    def ringkasan_statistik(self) -> dict:
        total_jenis = len(self._alat)
        total_unit = sum(a.stok_total for a in self._alat.values())
        unit_tersedia = sum(a.stok_tersedia for a in self._alat.values())
        transaksi_aktif = sum(1 for t in self._transaksi if t.status == "Dipinjam")
        total_denda = sum(t.denda for t in self._transaksi)
        return {
            "total_jenis": total_jenis,
            "total_unit": total_unit,
            "unit_tersedia": unit_tersedia,
            "transaksi_aktif": transaksi_aktif,
            "total_transaksi": len(self._transaksi),
            "total_denda": total_denda,
        }


    def ambil_pengguna(self, id_pengguna: str) -> Pengguna | None:
        return self._pengguna.get(id_pengguna.strip().upper())

    def autentikasi(self, id_pengguna: str, password: str) -> Pengguna:
        pengguna = self._pengguna.get(id_pengguna.strip().upper())
        if not pengguna or not pengguna.verifikasi_password(password):
            raise ValueError("ID pengguna atau kata sandi salah.")
        return pengguna

    def ubah_alat(
        self,
        id_admin: str,
        kode_alat: str,
        nama_baru: str,
        stok_total_baru: int,
        detail_teks: str,
        detail_extra: str,
    ) -> AlatKampus:
        admin = self._pengguna.get(id_admin.strip().upper())
        if not admin or not admin.boleh_kelola_alat():
            raise PermissionError("Hanya Admin yang berhak mengubah data alat.")
        alat = self._alat.get(kode_alat.strip().upper())
        if not alat:
            raise ValueError(f"Alat '{kode_alat}' tidak ditemukan.")
        alat.perbarui_dasar(nama_baru, stok_total_baru)
        if isinstance(alat, AlatElektronik):
            alat.perbarui_spesifikasi(detail_teks, int(detail_extra))
        elif isinstance(alat, AlatLaboratorium):
            butuh_kal = detail_extra.strip().lower() in ("ya", "true", "1", "yes")
            alat.perbarui_spesifikasi(detail_teks, butuh_kal)
        self._penyimpanan.simpan(self._alat, self._pengguna, self._transaksi)
        return alat

    def hapus_alat(self, id_admin: str, kode_alat: str) -> None:
        admin = self._pengguna.get(id_admin.strip().upper())
        if not admin or not admin.boleh_kelola_alat():
            raise PermissionError("Hanya Admin yang berhak menghapus alat.")
        kode = kode_alat.strip().upper()
        alat = self._alat.get(kode)
        if not alat:
            raise ValueError(f"Alat '{kode_alat}' tidak ditemukan.")
        if alat.sedang_dipinjam > 0:
            raise ValueError(
                f"Alat '{alat.nama}' sedang dipinjam ({alat.sedang_dipinjam} unit) dan tidak dapat dihapus."
            )
        del self._alat[kode]
        self._penyimpanan.simpan(self._alat, self._pengguna, self._transaksi)

    def tambah_pengguna(self, id_admin: str, pengguna_baru: Pengguna) -> Pengguna:
        admin = self._pengguna.get(id_admin.strip().upper())
        if not admin or not admin.boleh_kelola_alat():
            raise PermissionError("Hanya Admin yang berhak menambahkan pengguna.")
        if pengguna_baru.id_pengguna in self._pengguna:
            raise ValueError(f"ID pengguna '{pengguna_baru.id_pengguna}' sudah terdaftar.")
        self._pengguna[pengguna_baru.id_pengguna] = pengguna_baru
        self._penyimpanan.simpan(self._alat, self._pengguna, self._transaksi)
        return pengguna_baru

    def hapus_pengguna(self, id_admin: str, id_pengguna: str) -> None:
        admin = self._pengguna.get(id_admin.strip().upper())
        if not admin or not admin.boleh_kelola_alat():
            raise PermissionError("Hanya Admin yang berhak menghapus pengguna.")
        target_id = id_pengguna.strip().upper()
        pengguna = self._pengguna.get(target_id)
        if not pengguna:
            raise ValueError(f"Pengguna '{id_pengguna}' tidak ditemukan.")
        if pengguna.boleh_kelola_alat():
            raise ValueError("Akun Admin tidak dapat dihapus.")
        punya_aktif = any(t.id_pengguna == target_id and t.status == "Dipinjam" for t in self._transaksi)
        if punya_aktif:
            raise ValueError(f"Pengguna '{pengguna.nama}' masih memiliki peminjaman aktif dan tidak dapat dihapus.")
        del self._pengguna[target_id]
        self._penyimpanan.simpan(self._alat, self._pengguna, self._transaksi)
