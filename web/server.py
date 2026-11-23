from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse, urlencode
from models import AlatElektronik, AlatLaboratorium, Mahasiswa, Dosen
from services import LayananPeminjaman
from .templates import render_login, render_dashboard_admin, render_dashboard_pengguna


class HandlerSIMPA(BaseHTTPRequestHandler):
    layanan: LayananPeminjaman = None

    def _user_aktif(self):
        cookie_hdr = self.headers.get("Cookie", "")
        if not cookie_hdr:
            return None
        c = SimpleCookie()
        c.load(cookie_hdr)
        if "simpa_user" not in c:
            return None
        return self.layanan.ambil_pengguna(c["simpa_user"].value)

    def _kirim_html(self, konten: str, status: int = 200) -> None:
        data = konten.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _redirect(self, pesan: str = "", tipe: str = "success", cookie_val: str | None = None, clear_cookie: bool = False, halaman: str = "") -> None:
        query: dict = {}
        if pesan:
            query["pesan"] = pesan
            query["tipe"] = tipe
        if halaman:
            query["halaman"] = halaman
        loc = "/" + (f"?{urlencode(query)}" if query else "")
        self.send_response(303)
        if cookie_val is not None:
            self.send_header("Set-Cookie", f"simpa_user={cookie_val}; Path=/; HttpOnly")
        if clear_cookie:
            self.send_header("Set-Cookie", "simpa_user=; Path=/; Max-Age=0")
        self.send_header("Location", loc)
        self.end_headers()

    def _baca_form(self) -> dict[str, str]:
        panjang = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(panjang).decode("utf-8")
        return {k: v[0] for k, v in parse_qs(body).items()}

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/logout":
            self._redirect("Anda telah keluar dari sistem.", "success", clear_cookie=True)
            return

        params = parse_qs(parsed.query)
        pesan = params.get("pesan", [""])[0]
        tipe = params.get("tipe", ["info"])[0]
        kata_kunci = params.get("q", [""])[0]
        filter_jenis = params.get("jenis", [""])[0]

        user = self._user_aktif()
        if not user:
            self._kirim_html(render_login(pesan, tipe))
            return

        if user.role_portal() == "admin":
            halaman = params.get("halaman", ["beranda"])[0]
            html_out = render_dashboard_admin(
                user=user,
                stats=self.layanan.ringkasan_statistik(),
                daftar_alat=self.layanan.daftar_alat(kata_kunci, filter_jenis),
                transaksi_aktif=self.layanan.daftar_transaksi(hanya_aktif=True),
                riwayat_transaksi=self.layanan.daftar_transaksi(hanya_aktif=False),
                daftar_pengguna=self.layanan.daftar_pengguna(),
                pesan=pesan, tipe_pesan=tipe, kata_kunci=kata_kunci, filter_jenis=filter_jenis,
                halaman=halaman,
            )
        else:
            trx_saya = [t for t in self.layanan.daftar_transaksi(hanya_aktif=False) if t.id_pengguna == user.id_pengguna]
            html_out = render_dashboard_pengguna(
                user=user,
                stats=self.layanan.ringkasan_statistik(),
                daftar_alat=self.layanan.daftar_alat(kata_kunci, filter_jenis),
                transaksi_saya=trx_saya,
                pesan=pesan, tipe_pesan=tipe, kata_kunci=kata_kunci, filter_jenis=filter_jenis,
            )
        self._kirim_html(html_out)

    def do_POST(self) -> None:
        form = self._baca_form()
        try:
            if self.path == "/login":
                user = self.layanan.autentikasi(form.get("id_pengguna", ""), form.get("password", ""))
                self._redirect(f"Selamat datang, {user.nama}!", "success", cookie_val=user.id_pengguna)
                return

            user = self._user_aktif()
            if not user:
                self._redirect("Silakan login terlebih dahulu.", "error")
                return

            if self.path == "/pinjam":
                trx = self.layanan.pinjam_alat(user.id_pengguna, form.get("kode_alat", ""), int(form.get("jumlah", "1")), form.get("tanggal_pinjam") or None)
                self._redirect(f"Peminjaman {trx.id_transaksi} berhasil! Batas kembali: {trx.batas_kembali}.", "success")
            elif self.path == "/kembalikan":
                if user.role_portal() != "admin":
                    self._redirect("Akses ditolak. Pengembalian hanya dapat dilakukan oleh Admin.", "error")
                    return
                trx = self.layanan.kembalikan_alat(form.get("id_transaksi", ""), form.get("tanggal_kembali") or None)
                self._redirect(f"Pengembalian {trx.id_transaksi} selesai. Terlambat: {trx.hari_terlambat} hari, Denda: Rp {trx.denda:,}.", "success", halaman="peminjaman")
            elif self.path == "/tambah-alat":
                jenis = form.get("jenis", "Elektronik")
                if jenis == "Elektronik":
                    alat = AlatElektronik(form.get("kode_alat", ""), form.get("nama", ""), int(form.get("stok_total", "1")), int(form.get("detail_extra", "50")), form.get("detail_teks", "Umum"))
                else:
                    butuh_kal = form.get("detail_extra", "ya").strip().lower() in ("ya", "true", "1", "yes")
                    alat = AlatLaboratorium(form.get("kode_alat", ""), form.get("nama", ""), int(form.get("stok_total", "1")), form.get("detail_teks", "Umum"), butuh_kal)
                self.layanan.tambah_alat(user.id_pengguna, alat)
                self._redirect(f"Alat baru {alat.kode_alat} berhasil ditambahkan.", "success", halaman="kelola-alat")
            elif self.path == "/ubah-alat":
                alat = self.layanan.ubah_alat(user.id_pengguna, form.get("kode_alat", ""), form.get("nama", ""), int(form.get("stok_total", "1")), form.get("detail_teks", "Umum"), form.get("detail_extra", "50"))
                self._redirect(f"Data alat {alat.kode_alat} berhasil diperbarui.", "success", halaman="kelola-alat")
            elif self.path == "/hapus-alat":
                kode = form.get("kode_alat", "")
                self.layanan.hapus_alat(user.id_pengguna, kode)
                self._redirect(f"Alat {kode} berhasil dihapus.", "success", halaman="kelola-alat")
            elif self.path == "/tambah-pengguna":
                if user.role_portal() != "admin":
                    self._redirect("Akses ditolak.", "error", halaman="kelola-pengguna")
                    return
                peran = form.get("peran", "Mahasiswa")
                id_p = form.get("id_pengguna", "")
                nama = form.get("nama", "")
                detail = form.get("detail", "Sistem Informasi")
                pw = form.get("password", "user123")
                if peran == "Dosen":
                    pengguna_baru = Dosen(id_p, nama, detail, pw)
                else:
                    pengguna_baru = Mahasiswa(id_p, nama, detail, pw)
                self.layanan.tambah_pengguna(user.id_pengguna, pengguna_baru)
                self._redirect(f"Pengguna {pengguna_baru.nama} ({pengguna_baru.peran()}) berhasil ditambahkan.", "success", halaman="kelola-pengguna")
            elif self.path == "/hapus-pengguna":
                if user.role_portal() != "admin":
                    self._redirect("Akses ditolak.", "error", halaman="kelola-pengguna")
                    return
                id_p = form.get("id_pengguna", "")
                self.layanan.hapus_pengguna(user.id_pengguna, id_p)
                self._redirect(f"Pengguna {id_p} berhasil dihapus.", "success", halaman="kelola-pengguna")
            else:
                self._redirect("Endpoint tidak ditemukan.", "error")
        except Exception as exc:
            self._redirect(f"Gagal memproses: {exc}", "error")

    def log_message(self, format: str, *args) -> None:
        return


class AplikasiWebSIMPA:
    def __init__(self, layanan: LayananPeminjaman, host: str = "127.0.0.1", port: int = 8000):
        self._layanan = layanan
        self._host = host
        self._port = port

    def jalankan(self) -> None:
        HandlerSIMPA.layanan = self._layanan
        server = HTTPServer((self._host, self._port), HandlerSIMPA)
        print(f"SIMPA-Lab berjalan di http://{self._host}:{self._port} (Tekan Ctrl+C untuk berhenti)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer SIMPA-Lab dihentikan.")
        finally:
            server.server_close()
