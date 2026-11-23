# SIMPA-Lab — Sistem Informasi Peminjaman Alat Kampus

Aplikasi web sederhana berbasis **Python (Object-Oriented Programming)** untuk mengelola peminjaman, pengembalian, dan perhitungan denda alat elektronik serta alat laboratorium di lingkungan Program Studi S1 Sistem Informasi, Fakultas Teknik, Universitas Bengkulu.

## Prasyarat
- **Python 3.10 atau lebih baru** (diuji pada Python 3.11.2)
- **Tidak memerlukan pustaka pihak ketiga** (100% menggunakan pustaka standar Python: `abc`, `datetime`, `json`, `http.server`, `urllib.parse`, `unittest`).

## Struktur Proyek
```text
simpa_lab/
├── main.py                     # Entry point menjalankan web server
├── models/
│   ├── __init__.py
│   ├── alat.py                 # Abstract class AlatKampus + AlatElektronik & AlatLaboratorium
│   ├── pengguna.py             # Abstract class Pengguna + Mahasiswa, Dosen, & Admin
│   └── transaksi.py            # Class TransaksiPeminjaman
├── services/
│   ├── __init__.py
│   ├── penyimpanan.py          # Class PenyimpananJSON (persistensi data)
│   └── peminjaman_service.py   # Class LayananPeminjaman (logika bisnis utama)
├── web/
│   ├── __init__.py
│   ├── server.py               # Class AplikasiWebSIMPA & HandlerSIMPA
│   └── templates.py            # Renderer halaman HTML/CSS
├── data/
│   └── database.json           # Data otomatis terbuat saat aplikasi dijalankan
├── tests/
│   └── test_simpa.py           # Pengujian otomatis (unittest)
└── README.md
```

## Cara Menjalankan Aplikasi
1. Buka terminal/Command Prompt dan masuk ke folder proyek `simpa_lab/`.
2. Jalankan perintah:
   ```bash
   python3 main.py
   ```
   *(Di Windows dapat menggunakan `python main.py`)*
3. Buka browser dan kunjungi alamat:
   ```text
   http://127.0.0.1:8000
   ```
4. Untuk menghentikan server, tekan `Ctrl + C` pada terminal.

## Akun Uji Bawaan
- **Mahasiswa**: `G1F025020` (Asri Ayu Julita) — maks. 2 unit, durasi 3 hari.
- **Mahasiswa**: `G1F025014` (Mahasiswa Uji 2) — maks. 2 unit, durasi 3 hari.
- **Dosen**: `0012058701` (Dr. Della Maulidiya, M.Kom) — maks. 5 unit, durasi 7 hari.
- **Admin**: `ADM-001` (Petugas Lab SI) — hak tambah alat baru.

## Menjalankan Pengujian Otomatis
```bash
python3 -m unittest discover -s tests -v
```
