from flask import Blueprint, render_template, request, redirect, url_for
from app.config import get_supabase_client
from datetime import datetime
from collections import Counter


public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    """ Halaman utama portal informasi. """
    supabase = get_supabase_client()
    
    # 1. Ambil Slide Hero yang Aktif
    try:
        slides_res = supabase.table("hero_slides").select("*").eq("aktif", True).order("urutan").execute()
        slides = slides_res.data
        print(f"DEBUG: Menemukan {len(slides)} slide aktif")
    except Exception as e:
        print(f"DEBUG: Error saat mengambil slide: {str(e)}")
        slides = []

    # 2. Ambil Berita Terbaru (Limit 6)
    try:
        berita_res = supabase.table("berita").select("*").order("created_at", desc=True).limit(6).execute()
        berita_list = berita_res.data
        
        # Konversi string created_at menjadi objek datetime
        for item in berita_list:
            if item.get('created_at'):
                try:
                    dt_str = item['created_at'].replace('Z', '+00:00')
                    item['created_at'] = datetime.fromisoformat(dt_str)
                except Exception:
                    pass
                    
        print(f"DEBUG: Menemukan {len(berita_list)} berita")
    except Exception as e:
        print(f"DEBUG: Error saat mengambil berita: {str(e)}")
        berita_list = []

    # 3. Ambil Layanan yang Aktif (Limit 5)
    try:
        layanan_res = supabase.table("layanan").select("*").eq("aktif", True).order("urutan").limit(5).execute()
        layanan_list = layanan_res.data
    except Exception:
        layanan_list = []

    return render_template("index.html", 
                           slides=slides, 
                           berita_list=berita_list, 
                           layanan_list=layanan_list)


class Pagination:
    """ Kelas pembantu untuk menangani logika pagination. """
    def __init__(self, items, page, per_page, total_count):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.pages = (total_count + per_page - 1) // per_page
        self.has_prev = page > 1
        self.has_next = page < self.pages
        self.prev_num = page - 1
        self.next_num = page + 1

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        """ Generator untuk iterasi nomor halaman di UI. """
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

@public_bp.route("/berita")
def berita_list():
    """ Halaman daftar berita dengan pencarian dan filter kategori. """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    per_page = 6
    
    supabase = get_supabase_client()
    
    try:
        # Membangun query dasar
        query = supabase.table("berita").select("*", count="exact").order("created_at", desc=True)
        
        # Tambahkan filter jika ada input pencarian
        if search:
            query = query.ilike("judul", f"%{search}%")
        
        # Tambahkan filter kategori jika dipilih
        if category:
            query = query.eq("kategori", category)
            
        # Tentukan rentang data untuk pagination
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        res = query.range(start, end).execute()
        
        total_count = res.count if res.count is not None else 0
        berita_data = res.data
        
        # Konversi created_at menjadi objek datetime
        for item in berita_data:
            if item.get('created_at'):
                try:
                    dt_str = item['created_at'].replace('Z', '+00:00')
                    item['created_at'] = datetime.fromisoformat(dt_str)
                except Exception:
                    pass
        
        pagination = Pagination(berita_data, page, per_page, total_count)
        
        # Ambil data kategori unik untuk sidebar dengan menghitung jumlahnya
        cat_res = supabase.table("berita").select("kategori").execute()
        categories_raw = [item['kategori'] for item in cat_res.data]
        cat_counts = Counter(categories_raw)
        
    except Exception as e:
        print(f"DEBUG: Error saat mengambil daftar berita: {str(e)}")
        pagination = Pagination([], 1, per_page, 0)
        cat_counts = {}

    return render_template("berita/index.html", 
                           pagination=pagination, 
                           cat_counts=cat_counts,
                           current_category=category,
                           search_query=search)


@public_bp.route("/berita/<id_or_slug>")
def berita_detail(id_or_slug):
    """ Halaman detail berita berdasarkan ID atau Slug. """
    supabase = get_supabase_client()
    try:
        # Coba cari berdasarkan slug terlebih dahulu
        res = supabase.table("berita").select("*").eq("slug", id_or_slug).execute()
        if not res.data:
            # Jika tidak ketemu, coba cari berdasarkan ID
            res = supabase.table("berita").select("*").eq("id", id_or_slug).execute()
            
        if res.data:
            item = res.data[0]
            
            # Tambahkan jumlah tayangan (views) secara otomatis di backend
            try:
                supabase.rpc('increment_berita_views', {'row_id': item['id']}).execute()
            except Exception as e:
                print(f"DEBUG: Gagal menambahkan jumlah tayangan: {str(e)}")

            # Konversi tanggal untuk tampilan template
            if item.get('created_at'):
                try:
                    dt_str = item['created_at'].replace('Z', '+00:00')
                    item['created_at'] = datetime.fromisoformat(dt_str)
                except Exception:
                    pass
        else:
            return "Berita tidak ditemukan", 404
    except Exception:
        return "Terjadi kesalahan", 500
        
    return render_template("berita/detail.html", item=item)


@public_bp.route("/profil")
def profil():
    """ Halaman Profil Wilayah. """
    return render_template("profil.html")


@public_bp.route("/layanan")
def layanan():
    """ Halaman Daftar Layanan Publik. """
    return render_template("layanan/index.html")


@public_bp.route("/layanan/kependudukan")
def layanan_kependudukan():
    """ Halaman Layanan Kependudukan. """
    return render_template("layanan/kependudukan.html")


@public_bp.route("/layanan/kesehatan")
def layanan_kesehatan():
    """ Halaman Layanan Kesehatan. """
    return render_template("layanan/kesehatan.html")


@public_bp.route("/layanan/kebencanaan")
def layanan_kebencanaan():
    """ Halaman Monitoring Informasi Kebencanaan. """
    supabase = get_supabase_client()
    try:
        # Ambil data bencana yang masih aktif
        res = supabase.table("bencana").select("*").eq("aktif", True).order("created_at", desc=True).execute()
        bencana_list = res.data
    except Exception:
        bencana_list = []
    return render_template("layanan/kebencanaan.html", bencana_list=bencana_list)


@public_bp.route("/layanan/pariwisata")
def layanan_pariwisata():
    """ Halaman Katalog Pariwisata Unggulan. """
    supabase = get_supabase_client()
    try:
        # Ambil semua data objek wisata
        res = supabase.table("pariwisata").select("*").order("created_at", desc=True).execute()
        wisata_list = res.data
    except Exception:
        wisata_list = []
    return render_template("layanan/pariwisata.html", wisata_list=wisata_list)


@public_bp.route("/pengaduan", methods=["GET", "POST"])
def pengaduan():
    """ Halaman formulir pengaduan masyarakat. """
    if request.method == "POST":
        nama = request.form.get("nama")
        nik = request.form.get("nik")
        contact = request.form.get("contact")
        kategori = request.form.get("kategori")
        judul = request.form.get("judul")
        pesan = request.form.get("pesan")
        lampiran_file = request.files.get("lampiran")
        
        # Identifikasi tipe kontak (email atau telepon)
        email = contact if "@" in contact else "-"
        nomor_hp = contact if "@" not in contact else "-"
        
        # Menggabungkan NIK ke dalam deskripsi karena skema tabel tidak memiliki kolom NIK khusus
        full_description = f"[NIK: {nik}]\n\n{pesan}"
        
        lampiran_url = None
        supabase = get_supabase_client()
        
        # Memproses unggahan lampiran jika ada
        if lampiran_file and lampiran_file.filename != '':
            try:
                import uuid
                # Menggunakan UUID untuk menjamin nama file yang unik dan aman
                ext = lampiran_file.filename.split('.')[-1]
                file_path = f"pengaduan/{uuid.uuid4()}.{ext}"
                file_content = lampiran_file.read()
                
                print(f"DEBUG: Mengunggah lampiran ke 'pengaduan-lampiran' path: {file_path}")
                supabase.storage.from_("pengaduan-lampiran").upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": lampiran_file.content_type}
                )
                # Mendapatkan URL publik untuk file yang diunggah
                public_res = supabase.storage.from_("pengaduan-lampiran").get_public_url(file_path)
                lampiran_url = public_res
                print(f"DEBUG: Unggah berhasil! URL: {lampiran_url}")
            except Exception as e:
                print(f"DEBUG: Gagal mengunggah lampiran: {str(e)}")
                # Proses tetap dilanjutkan meskipun unggahan gagal, hanya lampiran yang kosong

        try:
            # Menyimpan data pengaduan ke database Supabase
            res = supabase.table("pengaduan").insert({
                "nama_pelapor": nama,
                "email": email,
                "nomor_hp": nomor_hp,
                "judul": judul,
                "deskripsi": full_description,
                "kategori": kategori,
                "status": "baru",
                "lampiran_url": lampiran_url
            }).execute()
            
            if res.data:
                # Ambil UUID aduan yang dihasilkan untuk dijadikan nomor tiket
                ticket_id = res.data[0]['id']
                return redirect(url_for('public.pengaduan_sukses', id=ticket_id))
        except Exception as e:
            print(f"Error saat menyimpan pengaduan: {str(e)}")
            return f"Terjadi kesalahan saat menyimpan data: {str(e)}", 500

    return render_template("pengaduan/index.html")


@public_bp.route("/pengaduan/sukses/<id>")
def pengaduan_sukses(id):
    """ Halaman konfirmasi setelah berhasil mengirim pengaduan. """
    return render_template("pengaduan/sukses.html", id=id)


@public_bp.route("/pengaduan/cek", methods=["GET", "POST"])
def pengaduan_cek():
    """ Halaman pelacakan status pengaduan berdasarkan ID Tiket. """
    hasil = None
    error = None
    if request.method == "POST":
        ticket_id = request.form.get('ticket_id', '').strip()
        if ticket_id:
            supabase = get_supabase_client()
            try:
                # Cari aduan berdasarkan ID tiket (UUID)
                res = supabase.table("pengaduan").select("*").eq("id", ticket_id).execute()
                if res.data:
                    hasil = res.data[0]
                else:
                    error = "ID Tiket tidak ditemukan."
            except Exception as e:
                error = f"Kesalahan: {str(e)}"
        else:
            error = "Masukkan ID Tiket."
            
    return render_template("pengaduan/cek.html", hasil=hasil, error=error)