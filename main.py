import os
from services import PenyimpananJSON, LayananPeminjaman
from web import AplikasiWebSIMPA


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "data", "database.json")
    penyimpanan = PenyimpananJSON(db_path)
    layanan = LayananPeminjaman(penyimpanan)
    app = AplikasiWebSIMPA(layanan, host="127.0.0.1", port=8000)
    app.jalankan()


if __name__ == "__main__":
    main()
