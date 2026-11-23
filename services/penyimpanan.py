import json
import os
from models import AlatKampus, Pengguna, TransaksiPeminjaman


class PenyimpananJSON:
    """Mengelola pembacaan dan penyimpanan data inventaris serta transaksi ke file JSON."""

    def __init__(self, file_path: str):
        self._file_path = file_path
        folder = os.path.dirname(os.path.abspath(file_path))
        os.makedirs(folder, exist_ok=True)

    @property
    def file_path(self) -> str:
        return self._file_path

    def muat(self) -> tuple[dict[str, AlatKampus], dict[str, Pengguna], list[TransaksiPeminjaman]]:
        if not os.path.exists(self._file_path):
            return {}, {}, []

        with open(self._file_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        daftar_alat = {
            item["kode_alat"]: AlatKampus.from_dict(item) for item in raw.get("alat", [])
        }
        daftar_pengguna = {
            item["id_pengguna"]: Pengguna.from_dict(item) for item in raw.get("pengguna", [])
        }
        daftar_transaksi = [
            TransaksiPeminjaman.from_dict(item) for item in raw.get("transaksi", [])
        ]
        return daftar_alat, daftar_pengguna, daftar_transaksi

    def simpan(
        self,
        daftar_alat: dict[str, AlatKampus],
        daftar_pengguna: dict[str, Pengguna],
        daftar_transaksi: list[TransaksiPeminjaman],
    ) -> None:
        payload = {
            "alat": [a.to_dict() for a in daftar_alat.values()],
            "pengguna": [p.to_dict() for p in daftar_pengguna.values()],
            "transaksi": [t.to_dict() for t in daftar_transaksi],
        }
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
