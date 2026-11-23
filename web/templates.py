import html
from datetime import date


def format_rupiah(nominal: int) -> str:
    return f"Rp {nominal:,.0f}".replace(",", ".")


BASE_HEAD = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SIMPA-Lab | Sistem Peminjaman Alat Kampus</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.14/dist/lenis.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/motion@11.11.13/dist/motion.js" defer></script>
<style>
  :root { --bg:#fafafa; --surface:#fff; --ink:#0f172a; --muted:#64748b; --line:#e2e8f0; --teal:#0f766e; --danger:#b91c1c; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { font-family:'Inter',system-ui,sans-serif; background:var(--bg); color:var(--ink); line-height:1.55; }
  .word-wrap { display:inline-block; overflow:hidden; vertical-align:bottom; margin-right:0.24em; }
  .word-inner { display:inline-block; }
  .topbar { position:sticky; top:0; z-index:40; background:rgba(250,250,250,0.88); backdrop-filter:blur(12px); border-bottom:1px solid var(--line); padding:14px 24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }
  .brand { display:flex; align-items:center; gap:10px; }
  .brand-mark { width:32px; height:32px; border-radius:9px; background:var(--ink); color:#fff; display:grid; place-items:center; font-weight:700; font-size:13px; }
  .brand-name { font-weight:700; font-size:15px; }
  .brand-sub { font-size:12px; color:var(--muted); }
  .nav-right { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
  .role-chip { font-size:12px; font-weight:600; padding:5px 11px; border-radius:999px; border:1px solid var(--line); background:var(--surface); }
  .role-chip.admin { background:var(--ink); color:#fff; border-color:var(--ink); }
  .btn { display:inline-flex; align-items:center; justify-content:center; padding:9px 15px; border-radius:8px; border:1px solid transparent; font-size:13px; font-weight:600; cursor:pointer; text-decoration:none; }
  .btn-primary { background:var(--ink); color:#fff; }
  .btn-teal { background:var(--teal); color:#fff; }
  .btn-ghost { background:#fff; color:var(--ink); border-color:var(--line); }
  .btn-danger { background:#fff; color:var(--danger); border-color:#fecaca; }
  .btn-sm { padding:6px 10px; font-size:12px; border-radius:7px; }
  .container { max-width:1120px; margin:0 auto; padding:26px 20px 60px; }
  .alert { padding:12px 16px; border-radius:10px; margin-bottom:18px; font-size:13.5px; font-weight:500; border:1px solid transparent; }
  .alert-success { background:#f0fdf4; color:#166534; border-color:#bbf7d0; }
  .alert-error { background:#fef2f2; color:#991b1b; border-color:#fecaca; }
  .login-shell { min-height:calc(100vh - 64px); display:grid; place-items:center; padding:32px 20px; }
  .login-grid { width:100%; max-width:940px; display:grid; grid-template-columns:1.1fr 0.9fr; gap:32px; align-items:center; }
  @media (max-width:780px) { .login-grid { grid-template-columns:1fr; } }
  .hero-title { font-size:clamp(28px,4vw,38px); font-weight:700; line-height:1.15; letter-spacing:-0.03em; margin:10px 0 14px; }
  .hero-desc { font-size:14.5px; color:var(--muted); margin-bottom:18px; }
  .card, .motion-card { background:var(--surface); border:1px solid var(--line); border-radius:14px; padding:20px; }
  .card { margin-bottom:18px; }
  .kpi-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:14px; margin-bottom:22px; }
  .kpi-label { font-size:11.5px; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:0.05em; }
  .kpi-val { font-size:25px; font-weight:700; margin-top:5px; }
  .grid-3 { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px; }
  .form-row { margin-bottom:12px; }
  label { display:block; font-size:12.5px; font-weight:600; color:#334155; margin-bottom:4px; }
  input, select { width:100%; padding:9px 10px; border:1px solid var(--line); border-radius:8px; font-size:13.5px; background:#fff; }
  .table-wrap { width:100%; overflow-x:auto; }
  table { width:100%; border-collapse:collapse; font-size:13px; min-width:620px; }
  th { text-align:left; padding:10px; font-size:11.5px; text-transform:uppercase; color:var(--muted); border-bottom:1px solid var(--line); }
  td { padding:10px; border-bottom:1px solid #f1f5f9; vertical-align:middle; }
  td.num, th.num { text-align:right; }
  .badge { padding:3px 9px; border-radius:999px; font-size:11.5px; font-weight:600; display:inline-block; }
  .badge-ok { background:#ecfdf5; color:#065f46; }
  .badge-warn { background:#fffbeb; color:#92400e; }
  .badge-empty { background:#fef2f2; color:#991b1b; }
  .tag { padding:2px 8px; border-radius:6px; font-size:11.5px; font-weight:600; border:1px solid var(--line); background:#f8fafc; }
  .inline-form { display:flex; gap:6px; align-items:center; flex-wrap:wrap; }
  .inline-form input[type="date"] { width:135px; padding:5px 7px; font-size:12px; }
  .demo-list { display:grid; gap:8px; font-size:12.5px; color:var(--muted); }
  .demo-item { background:#fff; border:1px solid var(--line); border-radius:10px; padding:10px 14px; }
  .demo-item strong { color:var(--ink); display:block; }
  details summary { cursor:pointer; font-size:12px; font-weight:600; color:var(--teal); }
</style>
</head>
<body>
"""

ANIM_SCRIPT = """
<script>
window.addEventListener("load", function() {
  if (typeof window.Lenis !== "undefined") {
    const lenis = new window.Lenis({ duration: 1.05, smoothWheel: true });
    if (typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined") {
      window.gsap.registerPlugin(window.ScrollTrigger);
      lenis.on("scroll", window.ScrollTrigger.update);
      window.gsap.ticker.add((t) => lenis.raf(t * 1000));
      window.gsap.ticker.lagSmoothing(0);
    } else {
      const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }
  document.querySelectorAll(".split-words").forEach((el) => {
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map((w) => '<span class="word-wrap"><span class="word-inner">' + w + '</span></span>').join("");
  });
  if (typeof window.gsap !== "undefined") {
    if (typeof window.ScrollTrigger !== "undefined") window.gsap.registerPlugin(window.ScrollTrigger);
    window.gsap.fromTo(".word-inner", { yPercent: 110, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.65, stagger: 0.065, ease: "power3.out" });
    document.querySelectorAll(".reveal-item").forEach((item, idx) => {
      if (typeof window.ScrollTrigger !== "undefined" && idx >= 3) {
        window.gsap.fromTo(item, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, scrollTrigger: { trigger: item, start: "top 92%", once: true } });
      } else {
        window.gsap.fromTo(item, { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, delay: 0.1 + idx * 0.06 });
      }
    });
  }
  document.querySelectorAll(".motion-card").forEach((card, idx) => {
    if (window.Motion && typeof window.Motion.animate === "function") {
      window.Motion.animate(card, { opacity: [0, 1], transform: ["translateY(14px) scale(0.985)", "translateY(0) scale(1)"] }, { duration: 0.45, delay: idx * 0.05 });
    }
    card.addEventListener("mouseenter", () => {
      if (window.Motion && typeof window.Motion.animate === "function") {
        window.Motion.animate(card, { transform: "translateY(-3px)", boxShadow: "0 12px 24px rgba(15,23,42,0.07)" }, { duration: 0.2 });
      }
    });
    card.addEventListener("mouseleave", () => {
      if (window.Motion && typeof window.Motion.animate === "function") {
        window.Motion.animate(card, { transform: "translateY(0px)", boxShadow: "0 1px 2px rgba(15,23,42,0.03)" }, { duration: 0.22 });
      }
    });
  });
});
</script>
</body></html>
"""


def _alert(pesan: str, tipe: str) -> str:
    if not pesan:
        return ""
    cls = "alert-success" if tipe == "success" else "alert-error"
    return f'<div class="alert {cls}">{html.escape(pesan)}</div>'


def render_login(pesan: str = "", tipe_pesan: str = "info") -> str:
    return BASE_HEAD + f"""
<nav class="topbar">
  <div class="brand"><div class="brand-mark">SL</div><div><div class="brand-name">SIMPA-Lab</div><div class="brand-sub">Sistem Peminjaman Alat Kampus &bull; SI UNIB</div></div></div>
</nav>
<main class="login-shell">
  <div class="login-grid">
    <div>
      <h1 class="hero-title split-words">Kelola Peminjaman Alat Kampus Tanpa Ribet.</h1>
    </div>
    <div class="card motion-card reveal-item" style="margin-bottom:0;padding:26px;">
      <h2 style="font-size:18px;margin-bottom:4px;">Masuk ke SIMPA-Lab</h2>
      <p style="font-size:13px;color:#64748b;margin-bottom:18px;">Masukkan ID akun dan kata sandi Anda.</p>
      {_alert(pesan, tipe_pesan)}
      <form method="POST" action="/login">
        <div class="form-row"><label>ID Pengguna (Admin / NPM / NIDN)</label><input type="text" name="id_pengguna" placeholder="Mis. ADM-001 atau G1F025020" required></div>
        <div class="form-row"><label>Kata Sandi</label><input type="password" name="password" placeholder="Masukkan kata sandi" required></div>
        <button type="submit" class="btn btn-primary" style="width:100%;">Masuk Sekarang</button>
      </form>
    </div>
  </div>
</main>
""" + ANIM_SCRIPT


def render_dashboard_admin(user, stats, daftar_alat, transaksi_aktif, riwayat_transaksi, daftar_pengguna=None, pesan="", tipe_pesan="info", kata_kunci="", filter_jenis="", halaman="beranda"):
    hari_ini = date.today().isoformat()
    if daftar_pengguna is None:
        daftar_pengguna = []

    baris_alat = ""
    for a in daftar_alat:
        is_elk = a.jenis_alat() == "Elektronik"
        det_teks = a.merek if is_elk else a.kategori_lab
        det_extra = str(a.daya_watt) if is_elk else ("ya" if a.butuh_kalibrasi else "tidak")
        baris_alat += f"""
        <tr>
          <td><strong>{html.escape(a.kode_alat)}</strong></td>
          <td>{html.escape(a.nama)}</td>
          <td><span class="tag">{html.escape(a.jenis_alat())}</span></td>
          <td>{html.escape(a.info_spesifikasi())}</td>
          <td class="num">{a.stok_tersedia} / {a.stok_total}</td>
          <td><span class="badge {'badge-ok' if a.stok_tersedia > 0 else 'badge-empty'}">{html.escape(a.status)}</span></td>
          <td>
            <div class="inline-form">
              <details>
                <summary>Edit</summary>
                <form method="POST" action="/ubah-alat" style="margin-top:8px;min-width:210px;">
                  <input type="hidden" name="kode_alat" value="{html.escape(a.kode_alat)}">
                  <input type="text" name="nama" value="{html.escape(a.nama)}" required style="margin-bottom:5px;">
                  <input type="number" name="stok_total" value="{a.stok_total}" min="1" required style="margin-bottom:5px;">
                  <input type="text" name="detail_teks" value="{html.escape(det_teks)}" required style="margin-bottom:5px;">
                  <input type="text" name="detail_extra" value="{html.escape(det_extra)}" required style="margin-bottom:5px;">
                  <button type="submit" class="btn btn-primary btn-sm">Simpan</button>
                </form>
              </details>
              <form method="POST" action="/hapus-alat">
                <input type="hidden" name="kode_alat" value="{html.escape(a.kode_alat)}">
                <button type="submit" class="btn btn-danger btn-sm">Hapus</button>
              </form>
            </div>
          </td>
        </tr>"""

    baris_aktif = "".join(f"""
      <tr>
        <td><strong>{html.escape(t.id_transaksi)}</strong></td>
        <td>{html.escape(t.nama_pengguna)} ({html.escape(t.peran_pengguna)})</td>
        <td>{html.escape(t.kode_alat)} - {html.escape(t.nama_alat)}</td>
        <td class="num">{t.jumlah}</td>
        <td>{html.escape(t.tanggal_pinjam)} &rarr; {html.escape(t.batas_kembali)}</td>
        <td>
          <form method="POST" action="/kembalikan" class="inline-form">
            <input type="hidden" name="id_transaksi" value="{html.escape(t.id_transaksi)}">
            <input type="date" name="tanggal_kembali" value="{hari_ini}" min="{hari_ini}" required>
            <button type="submit" class="btn btn-teal btn-sm">Kembalikan</button>
          </form>
        </td>
      </tr>""" for t in transaksi_aktif) or '<tr><td colspan="6" style="text-align:center;color:#64748b;">Tidak ada peminjaman aktif.</td></tr>'

    baris_riwayat = "".join(f"""
      <tr>
        <td><strong>{html.escape(t.id_transaksi)}</strong></td>
        <td>{html.escape(t.nama_pengguna)} ({html.escape(t.peran_pengguna)})</td>
        <td>{html.escape(t.nama_alat)} ({t.jumlah})</td>
        <td>{html.escape(t.tanggal_pinjam)} &rarr; {html.escape(t.batas_kembali)}</td>
        <td>{html.escape(t.tanggal_kembali or '-')}</td>
        <td class="num">{t.hari_terlambat} hari</td>
        <td class="num">{format_rupiah(t.denda)}</td>
        <td><span class="badge {'badge-warn' if t.status == 'Dipinjam' else 'badge-ok'}">{html.escape(t.status)}</span></td>
      </tr>""" for t in riwayat_transaksi)

    def _baris_p(p):
        detail = getattr(p, 'prodi', getattr(p, 'fakultas', getattr(p, 'unit', '-')))
        if p.peran() == 'Admin':
            aksi_td = '<em style="color:var(--muted);font-size:12px;">—</em>'
        else:
            aksi_td = (
                f'<form method="POST" action="/hapus-pengguna">'
                f'<input type="hidden" name="id_pengguna" value="{html.escape(p.id_pengguna)}">'
                f'<button type="submit" class="btn btn-danger btn-sm" '
                f'onclick="return confirm(\'Hapus pengguna {html.escape(p.nama)}?\')">Hapus</button>'
                f'</form>'
            )
        return (
            f'<tr>'
            f'<td><strong>{html.escape(p.id_pengguna)}</strong></td>'
            f'<td>{html.escape(p.nama)}</td>'
            f'<td><span class="tag">{html.escape(p.peran())}</span></td>'
            f'<td>{html.escape(detail)}</td>'
            f'<td class="num">{p.maks_unit_pinjam()} unit / {p.batas_hari_pinjam()} hari</td>'
            f'<td>{aksi_td}</td>'
            f'</tr>'
        )

    baris_pengguna = "".join(_baris_p(p) for p in daftar_pengguna) or '<tr><td colspan="6" style="text-align:center;color:#64748b;">Tidak ada pengguna.</td></tr>'

    nav_items = [
        ("beranda",        "bi-house-door",    "Beranda"),
        ("kelola-alat",    "bi-tools",         "Kelola Alat"),
        ("peminjaman",     "bi-clipboard-check","Peminjaman"),
        ("riwayat",        "bi-clock-history", "Riwayat Transaksi"),
        ("kelola-pengguna","bi-people",        "Kelola Pengguna"),
    ]
    sidebar_links = "".join(
        f'<a href="/?halaman={slug}" class="sidebar-link {"active" if halaman == slug else ""}">'
        f'<i class="bi {icon} sidebar-icon"></i>{label}</a>'
        for slug, icon, label in nav_items
    )

    # Konten utama berdasarkan halaman aktif
    if halaman == "kelola-alat":
        konten = f"""
        <h2 class="section-title">Kelola Alat</h2>
        <section class="card reveal-item">
          <h3 style="font-size:15px;margin-bottom:14px;font-weight:600;">Tambah Alat Baru</h3>
          <form method="POST" action="/tambah-alat">
            <div class="grid-3">
              <div class="form-row"><label>Jenis Alat</label><select name="jenis"><option value="Elektronik">Alat Elektronik</option><option value="Laboratorium">Alat Laboratorium</option></select></div>
              <div class="form-row"><label>Kode Alat</label><input type="text" name="kode_alat" placeholder="ELK-004 / LAB-004" required></div>
              <div class="form-row"><label>Stok Total</label><input type="number" name="stok_total" value="2" min="1" required></div>
            </div>
            <div class="grid-3">
              <div class="form-row"><label>Nama Alat</label><input type="text" name="nama" placeholder="Nama alat..." required></div>
              <div class="form-row"><label>Merek / Kategori Lab</label><input type="text" name="detail_teks" value="Umum" required></div>
              <div class="form-row"><label>Daya (Watt) / Kalibrasi (ya/tidak)</label><input type="text" name="detail_extra" value="50" required></div>
            </div>
            <button type="submit" class="btn btn-primary">Simpan Alat Baru</button>
          </form>
        </section>
        <section class="card reveal-item">
          <h3 style="font-size:15px;margin-bottom:12px;font-weight:600;">Inventaris Alat</h3>
          <form method="GET" action="/?halaman=kelola-alat" class="inline-form" style="margin-bottom:14px;">
            <input type="text" name="q" value="{html.escape(kata_kunci)}" placeholder="Cari alat..." style="flex:2;">
            <select name="jenis" style="flex:1;"><option value="">Semua Jenis</option><option value="Elektronik" {'selected' if filter_jenis=='Elektronik' else ''}>Elektronik</option><option value="Laboratorium" {'selected' if filter_jenis=='Laboratorium' else ''}>Laboratorium</option></select>
            <button type="submit" class="btn btn-ghost">Filter</button>
          </form>
          <div class="table-wrap"><table><thead><tr><th>Kode</th><th>Nama</th><th>Jenis</th><th>Spesifikasi</th><th class="num">Stok</th><th>Status</th><th>Aksi</th></tr></thead><tbody>{baris_alat}</tbody></table></div>
        </section>"""
    elif halaman == "peminjaman":
        konten = f"""
        <h2 class="section-title">Peminjaman Aktif &amp; Pengembalian</h2>
        <section class="card reveal-item">
          <div class="table-wrap"><table><thead><tr><th>ID Trx</th><th>Peminjam</th><th>Alat</th><th class="num">Unit</th><th>Periode</th><th>Aksi</th></tr></thead><tbody>{baris_aktif}</tbody></table></div>
        </section>"""
    elif halaman == "riwayat":
        konten = f"""
        <h2 class="section-title">Riwayat Seluruh Transaksi</h2>
        <section class="card reveal-item">
          <div class="table-wrap"><table><thead><tr><th>ID Trx</th><th>Peminjam</th><th>Alat</th><th>Periode</th><th>Kembali</th><th class="num">Telat</th><th class="num">Denda</th><th>Status</th></tr></thead><tbody>{baris_riwayat}</tbody></table></div>
        </section>"""
    elif halaman == "kelola-pengguna":
        konten = f"""
        <h2 class="section-title">Kelola Pengguna</h2>
        <section class="card reveal-item">
          <h3 style="font-size:15px;margin-bottom:14px;font-weight:600;">Tambah Pengguna Baru</h3>
          <form method="POST" action="/tambah-pengguna">
            <div class="grid-3">
              <div class="form-row"><label>Peran</label><select name="peran"><option value="Mahasiswa">Mahasiswa</option><option value="Dosen">Dosen</option></select></div>
              <div class="form-row"><label>ID (NPM / NIDN)</label><input type="text" name="id_pengguna" placeholder="G1F025099 / 001234567" required></div>
              <div class="form-row"><label>Nama Lengkap</label><input type="text" name="nama" placeholder="Nama pengguna..." required></div>
            </div>
            <div class="grid-3">
              <div class="form-row"><label>Prodi / Fakultas</label><input type="text" name="detail" placeholder="Sistem Informasi / Teknik" value="Sistem Informasi" required></div>
              <div class="form-row"><label>Kata Sandi</label><input type="password" name="password" value="user123" required></div>
            </div>
            <button type="submit" class="btn btn-primary">Tambah Pengguna</button>
          </form>
        </section>
        <section class="card reveal-item">
          <h3 style="font-size:15px;margin-bottom:12px;font-weight:600;">Daftar Pengguna Terdaftar</h3>
          <div class="table-wrap"><table><thead><tr><th>ID</th><th>Nama</th><th>Peran</th><th>Prodi / Fakultas / Unit</th><th>Kuota</th><th>Aksi</th></tr></thead><tbody>{baris_pengguna}</tbody></table></div>
        </section>"""
    else:  # beranda (default)
        baris_aktif_mini = "".join(
            f'<tr><td><strong>{html.escape(t.id_transaksi)}</strong></td>'
            f'<td>{html.escape(t.nama_pengguna)}</td>'
            f'<td>{html.escape(t.nama_alat)}</td>'
            f'<td class="num">{t.jumlah}</td>'
            f'<td>{html.escape(t.batas_kembali)}</td></tr>'
            for t in transaksi_aktif[:5]
        ) or '<tr><td colspan="5" style="text-align:center;color:#64748b;">Tidak ada peminjaman aktif.</td></tr>'
        konten = f"""
        <h2 class="section-title">Beranda</h2>
        <div class="kpi-grid">
          <div class="motion-card reveal-item"><div class="kpi-label">Jenis Alat</div><div class="kpi-val">{stats['total_jenis']}</div></div>
          <div class="motion-card reveal-item"><div class="kpi-label">Unit Tersedia</div><div class="kpi-val">{stats['unit_tersedia']} / {stats['total_unit']}</div></div>
          <div class="motion-card reveal-item"><div class="kpi-label">Peminjaman Aktif</div><div class="kpi-val">{stats['transaksi_aktif']}</div></div>
          <div class="motion-card reveal-item"><div class="kpi-label">Total Denda</div><div class="kpi-val">{format_rupiah(stats['total_denda'])}</div></div>
        </div>
        <div class="kpi-grid" style="margin-top:0;">
          <div class="motion-card reveal-item"><div class="kpi-label">Total Pengguna</div><div class="kpi-val">{len(daftar_pengguna)}</div></div>
          <div class="motion-card reveal-item"><div class="kpi-label">Total Transaksi</div><div class="kpi-val">{stats['total_transaksi']}</div></div>
        </div>
        <section class="card reveal-item" style="margin-top:4px;">
          <h3 style="font-size:14px;font-weight:600;margin-bottom:10px;">Peminjaman Aktif Terkini</h3>
          <div class="table-wrap"><table><thead><tr><th>ID Trx</th><th>Peminjam</th><th>Alat</th><th class="num">Unit</th><th>Batas Kembali</th></tr></thead>
          <tbody>{baris_aktif_mini}</tbody>
          </table></div>
        </section>"""

    return BASE_HEAD + f"""
<style>
  .admin-shell {{ display:flex; min-height:calc(100vh - 57px); }}
  .sidebar {{ width:220px; min-width:220px; background:var(--ink); color:#fff; display:flex; flex-direction:column; padding:20px 0; position:fixed; top:57px; left:0; height:calc(100vh - 57px); overflow-y:auto; z-index:30; }}
  .sidebar-title {{ font-size:11px; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:0.08em; padding:0 20px 10px; }}
  .sidebar-link {{ display:flex; align-items:center; gap:10px; padding:10px 20px; color:#cbd5e1; font-size:13.5px; font-weight:500; text-decoration:none; border-left:3px solid transparent; transition:all 0.15s; }}
  .sidebar-link:hover {{ background:rgba(255,255,255,0.07); color:#fff; }}
  .sidebar-link.active {{ background:rgba(255,255,255,0.1); color:#fff; border-left-color:var(--teal); font-weight:600; }}
  .sidebar-icon {{ font-size:17px; width:20px; text-align:center; line-height:1; }}
  .sidebar-footer {{ margin-top:auto; padding:16px 20px; border-top:1px solid #1e293b; }}
  .admin-content {{ flex:1; padding:28px 28px 60px; overflow-x:hidden; margin-left:220px; }}
  .section-title {{ font-size:20px; font-weight:700; margin-bottom:18px; color:var(--ink); }}
  @media(max-width:720px) {{ .sidebar {{ display:none; }} .admin-content {{ margin-left:0; }} }}
</style>
<nav class="topbar">
  <div class="brand"><div class="brand-mark">SL</div><div><div class="brand-name">SIMPA-Lab</div><div class="brand-sub">Dashboard Admin</div></div></div>
  <div class="nav-right">
    <span class="role-chip admin">{html.escape(user.nama)} (Admin)</span>
    <a href="/logout" class="btn btn-ghost btn-sm">Keluar</a>
  </div>
</nav>
<div class="admin-shell">
  <aside class="sidebar">
    <div class="sidebar-title">Menu Utama</div>
    {sidebar_links}
    <div class="sidebar-footer">
      <a href="/logout" class="btn btn-ghost btn-sm" style="width:100%;justify-content:center;">Keluar</a>
    </div>
  </aside>
  <main class="admin-content">
    {_alert(pesan, tipe_pesan)}
    {konten}
  </main>
</div>
""" + ANIM_SCRIPT


def render_dashboard_pengguna(user, stats, daftar_alat, transaksi_saya, pesan="", tipe_pesan="info", kata_kunci="", filter_jenis=""):
    hari_ini = date.today().isoformat()
    aktif_saya = [t for t in transaksi_saya if t.status == "Dipinjam"]
    opsi_alat = "".join(f'<option value="{html.escape(a.kode_alat)}">{html.escape(a.kode_alat)} - {html.escape(a.nama)} (Sisa: {a.stok_tersedia})</option>' for a in daftar_alat if a.stok_tersedia > 0)
    baris_alat = "".join(f"""
      <tr>
        <td><strong>{html.escape(a.kode_alat)}</strong></td>
        <td>{html.escape(a.nama)}</td>
        <td><span class="tag">{html.escape(a.jenis_alat())}</span></td>
        <td>{html.escape(a.info_spesifikasi())}</td>
        <td class="num">{a.stok_tersedia} / {a.stok_total}</td>
        <td><span class="badge {'badge-ok' if a.stok_tersedia > 0 else 'badge-empty'}">{html.escape(a.status)}</span></td>
      </tr>""" for a in daftar_alat)

    baris_aktif = "".join(f"""
      <tr>
        <td><strong>{html.escape(t.id_transaksi)}</strong></td>
        <td>{html.escape(t.kode_alat)} - {html.escape(t.nama_alat)}</td>
        <td class="num">{t.jumlah}</td>
        <td>{html.escape(t.tanggal_pinjam)} &rarr; {html.escape(t.batas_kembali)}</td>
        <td><span class="badge badge-warn">Menunggu Pengembalian ke Admin</span></td>
      </tr>""" for t in aktif_saya) or '<tr><td colspan="5" style="text-align:center;color:#64748b;">Belum ada peminjaman aktif.</td></tr>'

    baris_riwayat = "".join(f"""
      <tr>
        <td><strong>{html.escape(t.id_transaksi)}</strong></td>
        <td>{html.escape(t.nama_alat)} ({t.jumlah})</td>
        <td>{html.escape(t.tanggal_pinjam)} &rarr; {html.escape(t.batas_kembali)}</td>
        <td>{html.escape(t.tanggal_kembali or '-')}</td>
        <td class="num">{t.hari_terlambat} hari</td>
        <td class="num">{format_rupiah(t.denda)}</td>
        <td><span class="badge {'badge-warn' if t.status == 'Dipinjam' else 'badge-ok'}">{html.escape(t.status)}</span></td>
      </tr>""" for t in transaksi_saya) or '<tr><td colspan="7" style="text-align:center;color:#64748b;">Belum ada riwayat transaksi.</td></tr>'

    return BASE_HEAD + f"""
<nav class="topbar">
  <div class="brand"><div class="brand-mark">SL</div><div><div class="brand-name">SIMPA-Lab</div><div class="brand-sub">Dashboard Pengguna</div></div></div>
  <div class="nav-right">
    <span class="role-chip">{html.escape(user.nama)} ({html.escape(user.peran())})</span>
    <a href="/logout" class="btn btn-ghost btn-sm">Keluar</a>
  </div>
</nav>
<main class="container">
  {_alert(pesan, tipe_pesan)}
  <h1 class="hero-title split-words" style="font-size:30px;margin-top:0;">Dashboard Peminjaman Pengguna</h1>
  <p class="hero-desc reveal-item">Kuota Anda: maksimal {user.maks_unit_pinjam()} unit aktif dengan durasi {user.batas_hari_pinjam()} hari.</p>
  <div class="kpi-grid">
    <div class="motion-card reveal-item"><div class="kpi-label">Unit Tersedia di Lab</div><div class="kpi-val">{stats['unit_tersedia']}</div></div>
    <div class="motion-card reveal-item"><div class="kpi-label">Pinjaman Aktif Saya</div><div class="kpi-val">{len(aktif_saya)}</div></div>
    <div class="motion-card reveal-item"><div class="kpi-label">Total Denda Saya</div><div class="kpi-val">{format_rupiah(sum(t.denda for t in transaksi_saya))}</div></div>
  </div>
  <section class="card reveal-item">
    <h2 style="font-size:16px;margin-bottom:14px;">Ajukan Peminjaman Alat</h2>
    <form method="POST" action="/pinjam">
      <div class="grid-3">
        <div class="form-row"><label>Pilih Alat</label><select name="kode_alat" required>{opsi_alat}</select></div>
        <div class="form-row"><label>Jumlah Unit</label><input type="number" name="jumlah" value="1" min="1" max="{user.maks_unit_pinjam()}" required></div>
        <div class="form-row"><label>Tanggal Pinjam</label><input type="date" name="tanggal_pinjam" value="{hari_ini}" min="{hari_ini}" required></div>
      </div>
      <button type="submit" class="btn btn-teal">Ajukan Peminjaman</button>
    </form>
  </section>
  <section class="card reveal-item">
    <h2 style="font-size:16px;margin-bottom:12px;">Katalog Alat Kampus</h2>
    <form method="GET" action="/" class="inline-form" style="margin-bottom:14px;">
      <input type="text" name="q" value="{html.escape(kata_kunci)}" placeholder="Cari alat..." style="flex:2;">
      <select name="jenis" style="flex:1;"><option value="">Semua Jenis</option><option value="Elektronik" {'selected' if filter_jenis=='Elektronik' else ''}>Elektronik</option><option value="Laboratorium" {'selected' if filter_jenis=='Laboratorium' else ''}>Laboratorium</option></select>
      <button type="submit" class="btn btn-ghost">Filter</button>
    </form>
    <div class="table-wrap"><table><thead><tr><th>Kode</th><th>Nama</th><th>Jenis</th><th>Spesifikasi</th><th class="num">Stok</th><th>Status</th></tr></thead><tbody>{baris_alat}</tbody></table></div>
  </section>
  <section class="card reveal-item">
    <h2 style="font-size:16px;margin-bottom:12px;">Peminjaman Aktif Saya</h2>
    <div class="table-wrap"><table><thead><tr><th>ID Trx</th><th>Alat</th><th class="num">Unit</th><th>Periode</th><th>Status</th></tr></thead><tbody>{baris_aktif}</tbody></table></div>
  </section>
  <section class="card reveal-item">
    <h2 style="font-size:16px;margin-bottom:12px;">Riwayat Transaksi Saya</h2>
    <div class="table-wrap"><table><thead><tr><th>ID Trx</th><th>Alat</th><th>Periode</th><th>Kembali</th><th class="num">Telat</th><th class="num">Denda</th><th>Status</th></tr></thead><tbody>{baris_riwayat}</tbody></table></div>
  </section>
</main>
""" + ANIM_SCRIPT
