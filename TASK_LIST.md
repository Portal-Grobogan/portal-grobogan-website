# Task List — Portal Grobogan
> Stack: Flask Fullstack · Tailwind CSS v3 · Flutter · Supabase | April 2026

---

## 🗄️ FASE 1 — Supabase Setup

### 1.1 Inisialisasi Project
- [ ] Buat project baru di Supabase Dashboard
- [ ] Simpan `SUPABASE_URL` dan `SUPABASE_ANON_KEY` di `.env`
- [ ] Aktifkan Email Auth (Settings → Auth)
- [ ] Nonaktifkan "Confirm email" untuk akun admin internal (dev)

### 1.2 Schema Database
- [ ] Tabel `profiles` — id (uuid FK auth.users), nama, role, created_at
- [ ] Tabel `hero_slides` — id, judul, deskripsi, image_url, link_url, urutan, aktif, created_at
- [ ] Tabel `berita` — id, judul, slug (unique), konten, thumbnail_url, kategori, status, penulis_id, created_at, updated_at
- [ ] Tabel `pengumuman` — id, judul, konten, file_url, aktif, created_at
- [ ] Tabel `pengaduan` — id, nama_pelapor, email, nomor_hp, kategori, judul, deskripsi, status, lampiran_url, admin_notes, created_at, updated_at
- [ ] Tabel `layanan` — id, nama, deskripsi, icon_name, url_path, kategori, urutan, aktif
- [ ] Tabel `bencana` — id, judul, lokasi, tingkat_bahaya, deskripsi, lat, lng, aktif, created_at
- [ ] Tabel `pariwisata` — id, nama, deskripsi, alamat, foto_urls (text[]), kategori, lat, lng, created_at
- [ ] Buat trigger `update_updated_at()` untuk tabel `berita` dan `pengaduan`
- [ ] Seed data: 5 layanan publik, 1 hero slide placeholder

### 1.3 Row Level Security (RLS)
- [ ] Aktifkan RLS semua tabel
- [ ] Policy `berita`: SELECT published, ALL authenticated
- [ ] Policy `pengumuman`: SELECT aktif, ALL authenticated
- [ ] Policy `pengaduan`: INSERT all, SELECT/UPDATE authenticated
- [ ] Policy `hero_slides`: SELECT aktif, ALL authenticated
- [ ] Policy `layanan`, `bencana`, `pariwisata`: SELECT all, ALL authenticated

### 1.4 Storage Buckets
- [ ] `hero-images` (public), `berita-thumbnails` (public)
- [ ] `pengaduan-lampiran` (private), `pariwisata-foto` (public)
- [ ] `pengumuman-files` (public)
- [ ] Set max file size: gambar 5MB, dokumen 10MB

### 1.5 Realtime & Edge Function
- [ ] Aktifkan Realtime: tabel `bencana`, `pengaduan`, `berita`
- [ ] Setup Supabase CLI lokal
- [ ] Buat Edge Function `send-push-notification`
- [ ] Integrasikan Firebase Admin SDK ke Edge Function
- [ ] Simpan `FCM_SERVICE_ACCOUNT` di Supabase Secrets
- [ ] Buat Database Webhook: trigger push saat `bencana` INSERT/UPDATE

---

## ⚙️ FASE 2 — Setup Flask + Tailwind

### 2.1 Inisialisasi Flask
- [ ] Buat virtual environment Python
- [ ] Install: `flask flask-wtf flask-login supabase python-dotenv gunicorn`
- [ ] Buat struktur folder proyek (lihat PLAN_SUPABASE.md)
- [ ] Konfigurasi `.env` lengkap
- [ ] Buat Flask app factory di `app/__init__.py`
- [ ] Inisialisasi Supabase client di `app/config.py`
- [ ] Setup Flask-Login user loader

### 2.2 Setup Tailwind CSS

#### Build via Node (Produksi)
- [ ] Inisialisasi Node di folder proyek: `npm init -y`
- [ ] Install: `npm install -D tailwindcss`
- [ ] Buat `tailwind.config.js` dengan custom colors dan fonts brand Grobogan
- [ ] Buat `postcss.config.js`
- [ ] Buat `app/static/css/src/input.css` dengan `@tailwind` directives
- [ ] Tambahkan script build di `package.json`:
  ```json
  "scripts": {
    "build:css": "tailwindcss -i ./app/static/css/src/input.css -o ./app/static/css/main.css --minify",
    "watch:css": "tailwindcss -i ./app/static/css/src/input.css -o ./app/static/css/main.css --watch"
  }
  ```
- [ ] Konfigurasi `content` di `tailwind.config.js` untuk scan template Jinja2:
  ```js
  content: ["./app/templates/**/*.html", "./app/static/js/**/*.js"]
  ```
- [ ] Run `npm run build:css` dan link `main.css` di `base.html`
- [ ] Tambahkan `npm run build:css` ke deployment pipeline

### 2.3 Alpine.js (Interaktivitas Ringan)
- [ ] Tambahkan Alpine.js CDN di `base.html`:
  ```html
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  ```
- [ ] Buat komponen slider hero dengan `x-data`
- [ ] Buat komponen tabs berita/pengumuman dengan Alpine
- [ ] Buat hamburger menu mobile dengan Alpine

### 2.4 Lucide Icons
- [ ] Tambahkan Lucide CDN:
  ```html
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>lucide.createIcons();</script>
  ```
- [ ] Gunakan dengan `<i data-lucide="map-pin" class="w-5 h-5"></i>`

---

## 🎨 FASE 3 — Flask Website (Halaman Publik) + Design Rules

### 3.0 Pedoman Desain (Design System Rules) Terimplementasi
 Aturan ini wajib diimplementasikan di seluruh halaman untuk menjaga konsistensi gaya "Modern SaaS/Government".

- Filosofi: "Clean & Functional". Fokus pada hierarki informasi, bukan dekorasi berlebihan.
- Warna (Color Palette):
  - Primary (Branding): bg-primary (Contoh: Slate Blue/Indigo untuk kepercayaan).
  - Accent (CTA): bg-accent (Contoh: Emerald/Teal untuk tombol aksi).
  - Backgrounds: bg-site-bg (Slate 50/Gray 50) sebagai latar utama, bg-white untuk kartu.
  - Text: text-slate-900 (Heading), text-slate-600 (Body), text-slate-400 (Non-active).
  - Larangan: Dilarang keras menggunakan gradien warna-warni (bg-gradient-to-r from-pink-500...) pada area besar. Gunakan warna solid (Solid Colors) atau gradien monokromatik yang sangat samar.
- Tipografi:
  - Font Family: font-sans (Inter, Plus Jakarta Sans, atau Open Sans).
  - Hierarki: Heading tebal (font-bold), Body normal (font-normal), Line height longgar (leading-relaxed).
- Bayangan & Border (Elevation):
  - Gunakan shadow-sm atau shadow-card (custom: 0 1px 3px rgba(0,0,0,0.05)).
  - Border tipis border border-slate-100 untuk memisahkan elemen tanpa kesan "berat".
  - Radius konsisten: rounded-xl (12px) untuk kartu, rounded-lg (8px) untuk tombol/input.
- Spacing: Gunakan kelipatan 4px/8px (Tailwind default). Hindari nilai ganjil.

### 3.1 Template Global
 - [x] base.html — struktur HTML, pasang Google Fonts (Inter), Tailwind CDN, Lucide, Alpine.js.
 - [x] components/navbar.html — Styling: bg-white/80 backdrop-blur-lg border-b border-slate-100 sticky top-0 z-50. Hamburger Alpine dengan transisi mulus.
 - [x] components/footer.html — Styling: bg-slate-900 text-slate-300. 4 kolom grid. Hindari gambar background berat, gunakan warna solid.
 - [x] components/card_berita.html — macro dengan style clean: bg-white border border-slate-100 rounded-xl overflow-hidden. Thumbnail aspect-video object-cover. Tanpa border tebal.
 - [x] components/card_layanan.html — macro with style interactive: bg-white p-6 rounded-xl border border-slate-100 hover:border-primary hover:shadow-lg transition-all duration-300. Ikon Lucide berukuran w-10 h-10 text-primary.
 - [x] components/pagination.html — navigasi dengan style button: px-4 py-2 rounded-lg text-sm font-medium. Aktif: bg-primary text-white.
 - [x] components/hero_slider.html — slider Alpine.js. Styling: Gunakan overlay bg-gradient-to-t from-black/60 to-transparent (hanya gradien hitam transparan untuk keterbacaan teks, bukan warna cerah).

### 3.2 Halaman Beranda (/)
 - [x] Route GET / — fetch data.
 - [x] Hero Section: relative h-[520px], teks judul text-white text-4xl md:text-6xl font-bold drop-shadow-md. Tombol CTA bg-accent hover:bg-accent-dark text-white px-8 py-3 rounded-lg shadow-lg.
 - [x] Layanan Section: py-20 bg-site-bg. Judul section text-center mb-12. Grid grid-cols-2 lg:grid-cols-5 gap-6.
 - [x] Berita Section: py-20 bg-white. Tab Alpine dengan style px-4 py-2 rounded-full bg-slate-100 text-slate-600 (aktif: bg-primary text-white).
 - [x] CTA Banner: bg-primary text-white py-16. Gunakan pattern SVG samar (subtle pattern) jika perlu, hindari gradien warna.
 - [x] Validasi: Semua card harus memiliki efek hover yang halus: hover:-translate-y-1 dan hover:shadow-xl.

### 3.3 Halaman Profil (/profil)
 - [x] Route GET /profil
 - [x] Layout: max-w-4xl mx-auto (update: max-w-6xl untuk sidebar), px-6 py-16.
 - [x] Styling Konten: Gunakan Tailwind Typography (prose) untuk body teks agar rapi. Judul text-3xl font-bold text-slate-900 border-b pb-4 mb-8. Foto pimpinan gunakan rounded-xl shadow-sm.

### 3.4 Halaman Layanan (/layanan dan sub-halaman)
 - [x] Route GET /layanan — Layout: Grid dengan filter sidebar. Card layanan gaya "Dashboard App".
 - [x] Route GET /layanan/kependudukan — List persyaratan menggunakan divide-y divide-slate-100 agar rapi tanpa border penuh.
 - [x] Route GET /layanan/kesehatan — Tabel table-auto w-full bg-white rounded-xl overflow-hidden. Header bg-slate-50 text-slate-600 uppercase text-xs. Baris hover:bg-slate-50.
 - [x] Route GET /layanan/kebencanaan — Kartu status: Gunakan badge warna solid (tanpa gradien). Contoh: bg-red-100 text-red-700 (Bahaya), bg-yellow-100 text-yellow-700 (Waspada).
 - [x] Route GET /layanan/pariwisata — Galeri grid-cols-2 md:grid-cols-3 gap-4. Gambar rounded-xl. Modal Alpine dengan latar bg-black/50 backdrop-blur-sm.

### 3.5 Halaman Berita
 - [x] Route GET /berita — Layout: Sidebar filter kiri (desktop), list kanan. Card berita tampilan list (horizontal) untuk mobile, grid untuk desktop.
 - [x] Route GET /berita/<slug> — Artikel detail. Styling: prose prose-slate max-w-3xl mx-auto. Breadcrumb text-sm text-slate-500 mb-6. Gambar utama rounded-xl.

### 3.6 Halaman Pengaduan
 - [x] Route GET /pengaduan — Layout: Form centered max-w-xl mx-auto. Label text-sm font-medium text-slate-700. Input mt-1 block w-full px-4 py-3 bg-white border border-slate-200 rounded-lg shadow-sm focus:ring-primary focus:border-primary.
 - [x] Route POST /pengaduan — validasi error: text-red-500 text-xs mt-1.
 - [x] Route GET /pengaduan/sukses/<id> — Konfirmasi: Ikon ceklis besar hijau, ID dengan font font-mono bg-slate-100 px-2 py-1 rounded.
 - [x] Route GET+POST /pengaduan/cek — Hasil: Tampilan card status yang jelas. Badge status: px-3 py-1 rounded-full text-sm font-medium.

### 3.7 Halaman Error
 - [x] 404.html & 500.html — Layout: Flexbox centered full height. Ikon Lucide w-24 h-24 text-slate-300. Teks text-slate-600. Tombol btn-primary untuk kembali. Hindari ilustrasi yang terlalu ramai.

---

## 🛠️ FASE 4 — Dashboard Admin Flask + Design Rules

### 4.0 Pedoman Desain Admin (Admin UI Design System)
 - [x] Tujuan: Menciptakan antarmuka yang fokus pada produktivitas, kepadatan data yang nyaman, dan navigasi yang jelas.
 - [x] Filosofi: "Data-Density & Clarity". Admin panel harus bersih, tidak mencolok, dan fokus pada konten.
 - [x] Warna (Admin Palette):
 - [x] Sidebar: bg-slate-900 (Gelap netral) atau bg-primary-900 (Gelap branded). Teks text-slate-300.
 - [x] Background Konten: bg-slate-100 (Abu-abu terang) untuk memisahkan area kerja.
 - [x] Card/Box: bg-white dengan shadow sangat lembut.
 - [x] Status Badge:
 - [x] Success: bg-green-100 text-green-800
 - [x] Warning: bg-yellow-100 text-yellow-800
 - [x] Danger: bg-red-100 text-red-800
 - [x] Info: bg-blue-100 text-blue-800
 - [x] Navigasi:
 - [x] Menu Aktif: bg-slate-800 text-white (Indikator kuat).
 - [x] Menu Hover: bg-slate-800/50 text-white.
 - [x] Tabel Data: Header bg-slate-50 text-slate-500 uppercase text-xs. Border border-slate-200. Hover baris hover:bg-slate-50.
 - [x] Form: Label di atas input (block). Konsisten menggunakan rounded-lg.
### 4.1 Autentikasi
 - [x] Route GET/POST /admin/login — Layout: Centered card max-w-md mx-auto mt-20. Styling: Card bg-white p-8 rounded-xl shadow-xl. Input w-full.
 - [x] Route GET /admin/logout — Flash message "Anda telah logout" dengan kategori info.
 - [x] Decorator @login_required — Redirect ke login dengan next parameter.
### 4.2 Layout Admin
 - [x] admin/base.html — Layout: Flexbox flex min-h-screen.
 - [x] Sidebar: w-64 bg-slate-900 text-white flex-col. Logo area p-6 border-b border-slate-700.
 - [x] Menu Navigasi: Ikon Lucide w-5 h-5 mr-3. Link block px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white transition-colors rounded-md mx-2. Active state: bg-slate-700 text-white.
 - [x] Main Content: Area kerja flex-1 bg-slate-100.
 - [x] Header: bg-white h-16 border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10. Info user text-sm text-slate-600.
 - [x] Breadcrumb: flex items-center gap-2 text-sm text-slate-500 mb-6.
### 4.3 Dashboard
 - [x] Route GET /admin — Layout: Grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6.
 - [x] Kartu Statistik: bg-white p-6 rounded-xl shadow-sm border-l-4 border-primary. Angka text-3xl font-bold text-slate-800. Label text-sm text-slate-500. Gunakan warna border berbeda per kategori (misal: Hijau untuk Selesai, Merah untuk Baru).
### 4.4 CRUD Berita
 - [x] GET /admin/berita — Layout: Card bg-white rounded-xl shadow-sm overflow-hidden. Tabel min-w-full divide-y divide-slate-200.
 - [x] Tabel: Kolol aksi text-right. Tombol aksi text-sm text-primary hover:underline.
 - [x] GET/POST /admin/berita/tambah — Form: max-w-3xl mx-auto bg-white p-8 rounded-xl shadow. Input slug bg-slate-50 (readonly/auto).
 - [x] GET/POST /admin/berita/<id>/edit — Pre-filled value.
 - [x] POST /admin/berita/<id>/hapus — Konfirmasi dengan Alpine.js x-on:click atau modal sederhana.
### 4.5 CRUD Hero Slides
 - [x] List: Tabel sederhana dengan thumbnail kecil w-20 h-12 object-cover rounded.
 - [x] Form: Upload gambar dengan preview w-full aspect-video bg-slate-100 rounded-lg flex items-center justify-center border-2 border-dashed. Input urutan w-24.
### 4.6 Manajemen Pengaduan
 - [x] List: Tabel dengan fitur search px-4 py-2 border rounded-lg di atas tabel. Filter dropdown.
 - [x] Halaman Detail: grid grid-cols-3 gap-8. Area info pengadu (col-1), area isi pengaduan (col-2), area aksi admin (col-1 sidebar).
 - [x] Area Aksi Admin: Card bg-slate-50 p-6 rounded-xl. Select status w-full, Textarea catatan. Tombol btn-primary.
### 4.7 CRUD Layanan, Kebencanaan, Pariwisata
 - [x] CRUD Standar: Gunakan template tabel yang sama seperti modul Berita untuk konsistensi.
 - [x] Multi-upload Foto (Pariwisata): Area drag-and-drop atau tombol upload multiple. Tampilkan preview gambar dalam grid kecil di bawah input dengan tombol hapus (X) di pojok gambar.

---

## 📱 FASE 5 — Flutter Mobile

### 5.1 Setup Project
- [ ] `flutter create portal_grobogan --org id.grobogan`
- [ ] Tambah dependencies: supabase_flutter, firebase_messaging, go_router, flutter_riverpod, cached_network_image, google_fonts
- [ ] Inisialisasi Supabase + Firebase di `main.dart`
- [ ] Setup `google-services.json` (Android) dan `GoogleService-Info.plist` (iOS)

### 5.2 Design System Flutter
- [ ] `lib/theme/app_colors.dart` — semua konstanta warna (sama dengan Tailwind config)
- [ ] `lib/theme/app_text_styles.dart` — Montserrat + Inter TextStyle
- [ ] `lib/theme/app_theme.dart` — ThemeData hijau tua
- [ ] Widget `AppCard` — rounded 12, border tipis, shadow ringan
- [ ] Widget `AppButton` — primary/accent/outline variants
- [ ] Widget `AppBadge` — kategori dan status berwarna
- [ ] Widget `SkeletonLoader` — loading placeholder abu

### 5.3 Routing & Navigasi
- [ ] `go_router` dengan `ScaffoldWithBottomNavBar`
- [ ] Bottom nav: Beranda, Layanan, Pengaduan, Berita, Profil
- [ ] Deep link routes

### 5.4 Data Layer
- [ ] Services: BeritaService, LayananService, PengaduanService, BencanaService
- [ ] Riverpod providers untuk semua service
- [ ] Upload lampiran via `supabase.storage`

### 5.5 Screens
- [ ] **Beranda**: hero carousel, grid 5 layanan, berita terbaru
- [ ] **Layanan**: daftar card + sub-screen per layanan
- [ ] **Kebencanaan**: realtime stream, badge level bahaya merah/kuning/hijau
- [ ] **Pengaduan**: form + cek status
- [ ] **Berita**: list + detail dengan gambar hero + overlay
- [ ] **Pariwisata**: galeri grid foto
- [ ] **Profil**: info instansi statis

### 5.6 Push Notification
- [ ] Inisialisasi FCM, request permission
- [ ] Subscribe topik: `semua-warga`, `bencana-darurat`
- [ ] Handle foreground/background/terminated
- [ ] Deep link dari notifikasi ke screen relevan

### 5.7 UX Polish
- [ ] Skeleton loading semua list
- [ ] Pull-to-refresh
- [ ] Empty state + error state dengan retry
- [ ] Haptic feedback pada submit form

---

## 🧪 FASE 6 — QA & Deployment

### 6.1 QA Website
- [ ] Test semua route (200, 404, 500)
- [ ] Test form pengaduan end-to-end
- [ ] Test CRUD dashboard admin
- [ ] Cek kontras warna WCAG (DevTools → Accessibility)
- [ ] Responsive test: 320px, 375px, 768px, 1024px, 1440px
- [ ] Cross-browser: Chrome, Firefox, Safari
- [ ] Pastikan Tailwind purge tidak menghapus class dinamis (safelist jika perlu)

### 6.2 QA Flutter
- [ ] Widget test komponen utama
- [ ] Integration test flow pengaduan
- [ ] Test push notification di perangkat fisik
- [ ] Test realtime bencana
- [ ] Test Android API 21 minimum

### 6.3 Deployment Website
- [ ] Setup server + environment variables
- [ ] `npm run build:css` (Tailwind production build, minified)
- [ ] Konfigurasi Gunicorn + NGINX
- [ ] SSL Certbot: `certbot --nginx -d portal.grobogan.go.id`
- [ ] Test HTTPS redirect

### 6.4 Deployment Mobile
- [ ] `flutter build apk --release --obfuscate`
- [ ] Test APK release di 3+ perangkat
- [ ] Upload Google Play Console

### 6.5 Post-Launch
- [ ] Monitor Supabase (DB, storage, auth usage)
- [ ] Setup Sentry Flask + Flutter
- [ ] Dokumentasi admin + panduan warga
- [ ] Training petugas pemda
