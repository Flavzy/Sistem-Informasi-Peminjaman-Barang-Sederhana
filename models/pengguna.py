from abc import ABC, abstractmethod


class Pengguna(ABC):
    """Abstract base class untuk aktor pengguna sistem peminjaman alat."""

    def __init__(self, id_pengguna: str, nama: str, password: str = "user123"):
        if not id_pengguna or not id_pengguna.strip():
            raise ValueError("ID pengguna tidak boleh kosong.")
        if not nama or not nama.strip():
            raise ValueError("Nama pengguna tidak boleh kosong.")
        self._id_pengguna = id_pengguna.strip().upper()
        self._nama = nama.strip()
        self.__password = password

    @property
    def id_pengguna(self) -> str:
        return self._id_pengguna

    @property
    def nama(self) -> str:
        return self._nama

    def verifikasi_password(self, password: str) -> bool:
        return self.__password == password

    def _password_raw(self) -> str:
        return self.__password

    @abstractmethod
    def peran(self) -> str:
        pass

    @abstractmethod
    def batas_hari_pinjam(self) -> int:
        pass

    @abstractmethod
    def maks_unit_pinjam(self) -> int:
        pass

    def boleh_kelola_alat(self) -> bool:
        return False

    def role_portal(self) -> str:
        return "admin" if self.boleh_kelola_alat() else "pengguna"

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(data: dict) -> "Pengguna":
        peran = data.get("peran")
        pw = data.get("password", "admin123" if peran == "Admin" else "user123")
        if peran == "Mahasiswa":
            return Mahasiswa(data["id_pengguna"], data["nama"], data.get("prodi", "Sistem Informasi"), pw)
        if peran == "Dosen":
            return Dosen(data["id_pengguna"], data["nama"], data.get("fakultas", "Teknik"), pw)
        if peran == "Admin":
            return Admin(data["id_pengguna"], data["nama"], data.get("unit", "Laboratorium SI"), pw)
        raise ValueError(f"Peran pengguna tidak dikenal: {peran}")


class Mahasiswa(Pengguna):
    def __init__(self, npm: str, nama: str, prodi: str = "Sistem Informasi", password: str = "user123"):
        super().__init__(npm, nama, password)
        self._prodi = prodi.strip() or "Sistem Informasi"

    @property
    def prodi(self) -> str:
        return self._prodi

    def peran(self) -> str:
        return "Mahasiswa"

    def batas_hari_pinjam(self) -> int:
        return 3

    def maks_unit_pinjam(self) -> int:
        return 2

    def to_dict(self) -> dict:
        return {
            "peran": self.peran(),
            "id_pengguna": self.id_pengguna,
            "nama": self.nama,
            "prodi": self._prodi,
            "password": self._password_raw(),
        }


class Dosen(Pengguna):
    def __init__(self, nidn: str, nama: str, fakultas: str = "Teknik", password: str = "user123"):
        super().__init__(nidn, nama, password)
        self._fakultas = fakultas.strip() or "Teknik"

    @property
    def fakultas(self) -> str:
        return self._fakultas

    def peran(self) -> str:
        return "Dosen"

    def batas_hari_pinjam(self) -> int:
        return 7

    def maks_unit_pinjam(self) -> int:
        return 5

    def to_dict(self) -> dict:
        return {
            "peran": self.peran(),
            "id_pengguna": self.id_pengguna,
            "nama": self.nama,
            "fakultas": self._fakultas,
            "password": self._password_raw(),
        }


class Admin(Pengguna):
    def __init__(self, id_petugas: str, nama: str, unit: str = "Laboratorium SI", password: str = "admin123"):
        super().__init__(id_petugas, nama, password)
        self._unit = unit.strip() or "Laboratorium SI"

    @property
    def unit(self) -> str:
        return self._unit

    def peran(self) -> str:
        return "Admin"

    def batas_hari_pinjam(self) -> int:
        return 14

    def maks_unit_pinjam(self) -> int:
        return 10

    def boleh_kelola_alat(self) -> bool:
        return True

    def to_dict(self) -> dict:
        return {
            "peran": self.peran(),
            "id_pengguna": self.id_pengguna,
            "nama": self.nama,
            "unit": self._unit,
            "password": self._password_raw(),
        }
