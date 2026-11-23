from datetime import date, timedelta


class TransaksiPeminjaman:
    """Merepresentasikan satu transaksi peminjaman alat oleh seorang pengguna."""

    def __init__(
        self,
        id_transaksi: str,
        id_pengguna: str,
        nama_pengguna: str,
        peran_pengguna: str,
        kode_alat: str,
        nama_alat: str,
        jumlah: int,
        tanggal_pinjam: str,
        batas_kembali: str,
        status: str = "Dipinjam",
        tanggal_kembali: str | None = None,
        hari_terlambat: int = 0,
        denda: int = 0,
    ):
        if jumlah <= 0:
            raise ValueError("Jumlah unit peminjaman harus lebih dari 0.")
        self._id_transaksi = id_transaksi
        self._id_pengguna = id_pengguna
        self._nama_pengguna = nama_pengguna
        self._peran_pengguna = peran_pengguna
        self._kode_alat = kode_alat
        self._nama_alat = nama_alat
        self._jumlah = int(jumlah)
        self._tanggal_pinjam = tanggal_pinjam
        self._batas_kembali = batas_kembali
        self.__status = status
        self.__tanggal_kembali = tanggal_kembali
        self.__hari_terlambat = int(hari_terlambat)
        self.__denda = int(denda)

    @property
    def id_transaksi(self) -> str:
        return self._id_transaksi

    @property
    def id_pengguna(self) -> str:
        return self._id_pengguna

    @property
    def nama_pengguna(self) -> str:
        return self._nama_pengguna

    @property
    def peran_pengguna(self) -> str:
        return self._peran_pengguna

    @property
    def kode_alat(self) -> str:
        return self._kode_alat

    @property
    def nama_alat(self) -> str:
        return self._nama_alat

    @property
    def jumlah(self) -> int:
        return self._jumlah

    @property
    def tanggal_pinjam(self) -> str:
        return self._tanggal_pinjam

    @property
    def batas_kembali(self) -> str:
        return self._batas_kembali

    @property
    def status(self) -> str:
        return self.__status

    @property
    def tanggal_kembali(self) -> str | None:
        return self.__tanggal_kembali

    @property
    def hari_terlambat(self) -> int:
        return self.__hari_terlambat

    @property
    def denda(self) -> int:
        return self.__denda

    def tandai_kembali(self, tanggal_kembali_str: str, denda_per_unit_fn) -> int:
        if self.__status == "Dikembalikan":
            raise ValueError(f"Transaksi {self._id_transaksi} sudah dikembalikan sebelumnya.")

        tgl_pinjam = date.fromisoformat(self._tanggal_pinjam)
        tgl_batas = date.fromisoformat(self._batas_kembali)
        tgl_kembali = date.fromisoformat(tanggal_kembali_str)

        if tgl_kembali < tgl_pinjam:
            raise ValueError("Tanggal kembali tidak boleh lebih awal dari tanggal pinjam.")

        selisih = (tgl_kembali - tgl_batas).days
        self.__hari_terlambat = max(0, selisih)
        self.__denda = denda_per_unit_fn(self.__hari_terlambat) * self._jumlah
        self.__tanggal_kembali = tanggal_kembali_str
        self.__status = "Dikembalikan"
        return self.__denda

    @staticmethod
    def hitung_batas_kembali(tanggal_pinjam_str: str, durasi_hari: int) -> str:
        tgl = date.fromisoformat(tanggal_pinjam_str)
        return (tgl + timedelta(days=durasi_hari)).isoformat()

    def to_dict(self) -> dict:
        return {
            "id_transaksi": self._id_transaksi,
            "id_pengguna": self._id_pengguna,
            "nama_pengguna": self._nama_pengguna,
            "peran_pengguna": self._peran_pengguna,
            "kode_alat": self._kode_alat,
            "nama_alat": self._nama_alat,
            "jumlah": self._jumlah,
            "tanggal_pinjam": self._tanggal_pinjam,
            "batas_kembali": self._batas_kembali,
            "status": self.__status,
            "tanggal_kembali": self.__tanggal_kembali,
            "hari_terlambat": self.__hari_terlambat,
            "denda": self.__denda,
        }

    @staticmethod
    def from_dict(data: dict) -> "TransaksiPeminjaman":
        return TransaksiPeminjaman(
            id_transaksi=data["id_transaksi"],
            id_pengguna=data["id_pengguna"],
            nama_pengguna=data["nama_pengguna"],
            peran_pengguna=data["peran_pengguna"],
            kode_alat=data["kode_alat"],
            nama_alat=data["nama_alat"],
            jumlah=data["jumlah"],
            tanggal_pinjam=data["tanggal_pinjam"],
            batas_kembali=data["batas_kembali"],
            status=data.get("status", "Dipinjam"),
            tanggal_kembali=data.get("tanggal_kembali"),
            hari_terlambat=data.get("hari_terlambat", 0),
            denda=data.get("denda", 0),
        )
