# Portal Grobogan Website

Website portal layanan Pemerintah Kabupaten Grobogan berbasis Flask + Supabase + Tailwind CSS.

## Setup Setelah `git pull`

Jalankan langkah ini setiap selesai pull di environment baru (atau saat dependency berubah):

1. Install dependency Python
   ```bash
   pip install -r requirements.txt
   ```
2. Install dependency Node/Tailwind
   ```bash
   npm install
   ```
3. Build CSS Tailwind
   ```bash
   npm run build:css
   ```
4. Siapkan file environment
   - Copy `.env.example` menjadi `.env`
   - Isi nilai `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, dan `SECRET_KEY`

## Menjalankan Aplikasi

```bash
python app.py
```

atau:

```bash
flask --app run.py run --debug
```
