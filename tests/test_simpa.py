import os
import tempfile
import unittest
from models import AlatElektronik, AlatLaboratorium
from services import PenyimpananJSON, LayananPeminjaman


class TestSIMPALab(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp.name, "test_db.json")
        self.layanan = LayananPeminjaman(PenyimpananJSON(self.db_path))

    def tearDown(self):
        self.tmp.cleanup()

    def test_01_katalog_dan_filter(self):
        semua = self.layanan.daftar_alat()
        self.assertEqual(len(semua), 6)
        lab = self.layanan.daftar_alat(jenis="Laboratorium")
        self.assertEqual(len(lab), 3)
        cari = self.layanan.daftar_alat(kata_kunci="Proyektor")
        self.assertEqual(len(cari), 1)

    def test_02_peminjaman_mahasiswa_valid(self):
        trx = self.layanan.pinjam_alat("G1F025020", "ELK-001", 1, "2026-11-23")
        self.assertEqual(trx.status, "Dipinjam")
        self.assertEqual(trx.batas_kembali, "2026-11-26")  # 3 hari untuk Mahasiswa
        alat = self.layanan.daftar_alat(kata_kunci="ELK-001")[0]
        self.assertEqual(alat.stok_tersedia, 3)

    def test_03_batas_unit_mahasiswa_ditolak(self):
        with self.assertRaises(ValueError):
            self.layanan.pinjam_alat("G1F025020", "ELK-001", 3, "2026-11-23")

    def test_04_peminjaman_dosen_batas_lebih_tinggi(self):
        trx = self.layanan.pinjam_alat("0012058701", "LAB-001", 4, "2026-11-23")
        self.assertEqual(trx.batas_kembali, "2026-11-30")  # 7 hari untuk Dosen

    def test_05_pengembalian_tepat_waktu_tanpa_denda(self):
        trx = self.layanan.pinjam_alat("G1F025020", "ELK-001", 1, "2026-11-23")
        hasil = self.layanan.kembalikan_alat(trx.id_transaksi, "2026-11-25")
        self.assertEqual(hasil.hari_terlambat, 0)
        self.assertEqual(hasil.denda, 0)
        self.assertEqual(hasil.status, "Dikembalikan")

    def test_06_polymorphism_denda_elektronik_vs_lab(self):
        trx_elk = self.layanan.pinjam_alat("G1F025020", "ELK-001", 1, "2026-11-01")
        # Batas 2026-11-04, kembali 2026-11-07 -> telat 3 hari -> 3 * 10.000 = 30.000
        res_elk = self.layanan.kembalikan_alat(trx_elk.id_transaksi, "2026-11-07")
        self.assertEqual(res_elk.hari_terlambat, 3)
        self.assertEqual(res_elk.denda, 30_000)

        trx_lab = self.layanan.pinjam_alat("G1F025020", "LAB-002", 1, "2026-11-01")
        # Batas 2026-11-04, kembali 2026-11-07 -> telat 3 hari -> 3 * 15.000 + 10.000 kalibrasi = 55.000
        res_lab = self.layanan.kembalikan_alat(trx_lab.id_transaksi, "2026-11-07")
        self.assertEqual(res_lab.hari_terlambat, 3)
        self.assertEqual(res_lab.denda, 55_000)

    def test_07_tambah_alat_otorisasi_admin(self):
        alat_baru = AlatElektronik("ELK-004", "Tripod Kamera", 3, 5, "Takara")
        with self.assertRaises(PermissionError):
            self.layanan.tambah_alat("G1F025020", alat_baru)
        disimpan = self.layanan.tambah_alat("ADM-001", alat_baru)
        self.assertEqual(disimpan.kode_alat, "ELK-004")

    def test_08_stok_tidak_mencukupi_ditolak(self):
        with self.assertRaises(ValueError):
            self.layanan.pinjam_alat("0012058701", "ELK-002", 3, "2026-11-23")



    def test_09_login_admin_dan_pengguna(self):
        adm = self.layanan.autentikasi("ADM-001", "admin123")
        self.assertEqual(adm.role_portal(), "admin")
        mhs = self.layanan.autentikasi("G1F025020", "user123")
        self.assertEqual(mhs.role_portal(), "pengguna")
        with self.assertRaises(ValueError):
            self.layanan.autentikasi("ADM-001", "salah")

    def test_10_admin_update_dan_delete_alat(self):
        diubah = self.layanan.ubah_alat("ADM-001", "ELK-003", "Speaker JBL Pro", 5, "JBL", "60")
        self.assertEqual(diubah.nama, "Speaker JBL Pro")
        self.assertEqual(diubah.stok_total, 5)
        self.layanan.hapus_alat("ADM-001", "ELK-003")
        self.assertEqual(len(self.layanan.daftar_alat(kata_kunci="ELK-003")), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
