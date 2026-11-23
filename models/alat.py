from abc import ABC, abstractmethod


class AlatKampus(ABC):
    """Abstract base class untuk seluruh alat yang dapat dipinjam di kampus."""

    def __init__(self, kode_alat: str, nama: str, stok_total: int, stok_tersedia: int | None = None):
        if not kode_alat or not kode_alat.strip():
            raise ValueError("Kode alat tidak boleh kosong.")
        if not nama or not nama.strip():
            raise ValueError("Nama alat tidak boleh kosong.")
        if stok_total < 0:
            raise ValueError("Stok total tidak boleh negatif.")

        tersedia = stok_total if stok_tersedia is None else stok_tersedia
        if tersedia < 0 or tersedia > stok_total:
            raise ValueError("Stok tersedia harus berada antara 0 dan stok total.")

        self._kode_alat = kode_alat.strip().upper()
        self._nama = nama.strip()
        self.__stok_total = int(stok_total)
        self.__stok_tersedia = int(tersedia)

    @property
    def kode_alat(self) -> str:
        return self._kode_alat

    @property
    def nama(self) -> str:
        return self._nama

    @property
    def stok_total(self) -> int:
        return self.__stok_total

    @property
    def stok_tersedia(self) -> int:
        return self.__stok_tersedia

    @property
    def sedang_dipinjam(self) -> int:
        return self.__stok_total - self.__stok_tersedia

    @property
    def status(self) -> str:
        return "Tersedia" if self.__stok_tersedia > 0 else "Habis"

    def perbarui_dasar(self, nama_baru: str, stok_total_baru: int) -> None:
        if not nama_baru or not nama_baru.strip():
            raise ValueError("Nama alat tidak boleh kosong.")
        if stok_total_baru < self.sedang_dipinjam:
            raise ValueError(f"Stok total tidak boleh kurang dari unit yang sedang dipinjam ({self.sedang_dipinjam}).")
        self._nama = nama_baru.strip()
        self.__stok_tersedia = int(stok_total_baru) - self.sedang_dipinjam
        self.__stok_total = int(stok_total_baru)

    def kurangi_stok(self, jumlah: int = 1) -> None:
        if jumlah <= 0:
            raise ValueError("Jumlah peminjaman harus lebih dari 0.")
        if jumlah > self.__stok_tersedia:
            raise ValueError(
                f"Stok '{self._nama}' tidak mencukupi (tersedia: {self.__stok_tersedia})."
            )
        self.__stok_tersedia -= jumlah

    def tambah_stok(self, jumlah: int = 1) -> None:
        if jumlah <= 0:
            raise ValueError("Jumlah pengembalian harus lebih dari 0.")
        if self.__stok_tersedia + jumlah > self.__stok_total:
            raise ValueError("Jumlah pengembalian melebihi stok total alat.")
        self.__stok_tersedia += jumlah

    @abstractmethod
    def jenis_alat(self) -> str:
        pass

    @abstractmethod
    def hitung_denda(self, hari_terlambat: int) -> int:
        pass

    @abstractmethod
    def info_spesifikasi(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(data: dict) -> "AlatKampus":
        jenis = data.get("jenis")
        if jenis == "Elektronik":
            return AlatElektronik(
                kode_alat=data["kode_alat"],
                nama=data["nama"],
                stok_total=data["stok_total"],
                stok_tersedia=data["stok_tersedia"],
                daya_watt=data.get("daya_watt", 50),
                merek=data.get("merek", "Umum"),
            )
        if jenis == "Laboratorium":
            return AlatLaboratorium(
                kode_alat=data["kode_alat"],
                nama=data["nama"],
                stok_total=data["stok_total"],
                stok_tersedia=data["stok_tersedia"],
                kategori_lab=data.get("kategori_lab", "Komputer"),
                butuh_kalibrasi=data.get("butuh_kalibrasi", False),
            )
        raise ValueError(f"Jenis alat tidak dikenal: {jenis}")


class AlatElektronik(AlatKampus):
    """Subkelas untuk peralatan elektronik kampus seperti proyektor, kamera, dan speaker."""

    TARIF_DENDA_HARIAN = 10_000

    def __init__(
        self,
        kode_alat: str,
        nama: str,
        stok_total: int,
        daya_watt: int,
        merek: str,
        stok_tersedia: int | None = None,
    ):
        super().__init__(kode_alat, nama, stok_total, stok_tersedia)
        if daya_watt <= 0:
            raise ValueError("Daya listrik (Watt) harus lebih dari 0.")
        self._daya_watt = int(daya_watt)
        self._merek = merek.strip() or "Umum"

    @property
    def daya_watt(self) -> int:
        return self._daya_watt

    @property
    def merek(self) -> str:
        return self._merek

    def perbarui_spesifikasi(self, merek_baru: str, daya_watt_baru: int) -> None:
        if daya_watt_baru <= 0:
            raise ValueError("Daya listrik (Watt) harus lebih dari 0.")
        self._merek = merek_baru.strip() or "Umum"
        self._daya_watt = int(daya_watt_baru)

    def jenis_alat(self) -> str:
        return "Elektronik"

    def hitung_denda(self, hari_terlambat: int) -> int:
        if hari_terlambat <= 0:
            return 0
        return hari_terlambat * self.TARIF_DENDA_HARIAN

    def info_spesifikasi(self) -> str:
        return f"Merek {self._merek}, Daya {self._daya_watt}W"

    def to_dict(self) -> dict:
        return {
            "jenis": self.jenis_alat(),
            "kode_alat": self.kode_alat,
            "nama": self.nama,
            "stok_total": self.stok_total,
            "stok_tersedia": self.stok_tersedia,
            "daya_watt": self._daya_watt,
            "merek": self._merek,
        }


class AlatLaboratorium(AlatKampus):
    """Subkelas untuk peralatan laboratorium yang membutuhkan ketelitian dan inspeksi kalibrasi."""

    TARIF_DENDA_HARIAN = 15_000
    BIAYA_INSPEKSI_KALIBRASI = 10_000

    def __init__(
        self,
        kode_alat: str,
        nama: str,
        stok_total: int,
        kategori_lab: str,
        butuh_kalibrasi: bool = True,
        stok_tersedia: int | None = None,
    ):
        super().__init__(kode_alat, nama, stok_total, stok_tersedia)
        self._kategori_lab = kategori_lab.strip() or "Umum"
        self._butuh_kalibrasi = bool(butuh_kalibrasi)

    @property
    def kategori_lab(self) -> str:
        return self._kategori_lab

    @property
    def butuh_kalibrasi(self) -> bool:
        return self._butuh_kalibrasi

    def perbarui_spesifikasi(self, kategori_lab_baru: str, butuh_kalibrasi_baru: bool) -> None:
        self._kategori_lab = kategori_lab_baru.strip() or "Umum"
        self._butuh_kalibrasi = bool(butuh_kalibrasi_baru)

    def jenis_alat(self) -> str:
        return "Laboratorium"

    def hitung_denda(self, hari_terlambat: int) -> int:
        if hari_terlambat <= 0:
            return 0
        denda = hari_terlambat * self.TARIF_DENDA_HARIAN
        if self._butuh_kalibrasi and hari_terlambat > 2:
            denda += self.BIAYA_INSPEKSI_KALIBRASI
        return denda

    def info_spesifikasi(self) -> str:
        kal = "Perlu Kalibrasi" if self._butuh_kalibrasi else "Standar"
        return f"Lab {self._kategori_lab} ({kal})"

    def to_dict(self) -> dict:
        return {
            "jenis": self.jenis_alat(),
            "kode_alat": self.kode_alat,
            "nama": self.nama,
            "stok_total": self.stok_total,
            "stok_tersedia": self.stok_tersedia,
            "kategori_lab": self._kategori_lab,
            "butuh_kalibrasi": self._butuh_kalibrasi,
        }
