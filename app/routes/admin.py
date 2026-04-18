import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.config import get_supabase_client
from app import AdminUser

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

@admin_bp.route("/")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")

# --- LOGIN / LOGOUT ---
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        supabase = get_supabase_client()
        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if res.user:
                user = AdminUser(user_id=res.user.id)
                login_user(user)
                flash("Login berhasil! Selamat datang kembali.", "success")
                next_page = request.args.get('next')
                return redirect(next_page or url_for('admin.dashboard'))
        except Exception:
            flash(f"Login gagal: Email atau password salah.", "error")
            
    return render_template("admin/login.html")

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "info")
    return redirect(url_for('admin.login'))

# --- BERITA CRUD (Phase 4.4) ---
@admin_bp.route("/berita")
@login_required
def list_berita():
    supabase = get_supabase_client()
    try:
        res = supabase.table("berita").select("*").order("created_at", desc=True).execute()
        berita_list = res.data
    except Exception as e:
        flash(f"Gagal mengambil data berita: {str(e)}", "error")
        berita_list = []
    
    return render_template("admin/berita/index.html", berita_list=berita_list)

@admin_bp.route("/berita/tambah", methods=["GET", "POST"])
@login_required
def tambah_berita():
    if request.method == "POST":
        judul = request.form.get("judul")
        content = request.form.get("content")
        kategori = request.form.get("kategori")
        image_file = request.files.get("thumbnail_file")
        thumbnail_url = request.form.get("thumbnail_url")
        slug = slugify(judul)
        
        supabase = get_supabase_client()
        
        if image_file and image_file.filename != '':
            try:
                file_path = f"{slug}_{image_file.filename}"
                file_content = image_file.read()
                supabase.storage.from_("berita-thumbnails").upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": image_file.content_type}
                )
                thumbnail_url = supabase.storage.from_("berita-thumbnails").get_public_url(file_path)
            except Exception as e:
                flash(f"Gagal upload thumbnail: {str(e)}", "error")

        try:
            supabase.table("berita").insert({
                "judul": judul,
                "slug": slug,
                "content": content,
                "kategori": kategori,
                "thumbnail_url": thumbnail_url
            }).execute()
            flash("Berita berhasil ditambahkan!", "success")
            return redirect(url_for('admin.list_berita'))
        except Exception as e:
            flash(f"Gagal menambah berita: {str(e)}", "error")
            
    return render_template("admin/berita/form.html", berita=None)

@admin_bp.route("/berita/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_berita(id):
    supabase = get_supabase_client()
    
    if request.method == "POST":
        judul = request.form.get("judul")
        content = request.form.get("content")
        kategori = request.form.get("kategori")
        image_file = request.files.get("thumbnail_file")
        thumbnail_url = request.form.get("thumbnail_url")
        slug = slugify(judul)
        
        if image_file and image_file.filename != '':
            try:
                file_path = f"{slug}_{image_file.filename}"
                file_content = image_file.read()
                supabase.storage.from_("berita-thumbnails").upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": image_file.content_type}
                )
                thumbnail_url = supabase.storage.from_("berita-thumbnails").get_public_url(file_path)
            except Exception as e:
                flash(f"Gagal upload thumbnail baru: {str(e)}", "error")

        try:
            supabase.table("berita").update({
                "judul": judul,
                "slug": slug,
                "content": content,
                "kategori": kategori,
                "thumbnail_url": thumbnail_url
            }).eq("id", id).execute()
            flash("Berita berhasil diperbarui!", "success")
            return redirect(url_for('admin.list_berita'))
        except Exception as e:
            flash(f"Gagal memperbarui berita: {str(e)}", "error")
            
    # GET: Fetch existing data
    try:
        res = supabase.table("berita").select("*").eq("id", id).single().execute()
        berita = res.data
    except Exception as e:
        flash("Berita tidak ditemukan.", "error")
        return redirect(url_for('admin.list_berita'))
        
    return render_template("admin/berita/form.html", berita=berita)

@admin_bp.route("/berita/hapus/<id>", methods=["POST"])
@login_required
def hapus_berita(id):
    supabase = get_supabase_client()
    try:
        supabase.table("berita").delete().eq("id", id).execute()
        flash("Berita berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus berita: {str(e)}", "error")
    return redirect(url_for('admin.list_berita'))

# --- HERO SLIDES CRUD (Phase 4.5) ---
@admin_bp.route("/hero")
@login_required
def list_hero():
    supabase = get_supabase_client()
    try:
        res = supabase.table("hero_slides").select("*").order("urutan").execute()
        hero_list = res.data
    except Exception as e:
        flash(f"Gagal mengambil data hero slide: {str(e)}", "error")
        hero_list = []
    
    return render_template("admin/hero/index.html", hero_list=hero_list)

@admin_bp.route("/hero/tambah", methods=["GET", "POST"])
@login_required
def tambah_hero():
    if request.method == "POST":
        judul = request.form.get("judul")
        deskripsi = request.form.get("deskripsi")
        link_url = request.form.get("link_url")
        urutan = request.form.get("urutan", type=int, default=0)
        aktif = "aktif" in request.form
        
        image_file = request.files.get("image_file")
        image_url = request.form.get("image_url") # Fallback to URL if no file
        
        supabase = get_supabase_client()
        
        if image_file and image_file.filename != '':
            try:
                # Upload to Supabase Storage
                file_path = f"{slugify(judul)}_{image_file.filename}"
                file_content = image_file.read()
                
                # Check if bucket exists/accessible - though we assume it's there per Phase 1.4
                supabase.storage.from_("hero-images").upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": image_file.content_type}
                )
                
                # Get public URL
                public_res = supabase.storage.from_("hero-images").get_public_url(file_path)
                image_url = public_res
            except Exception as e:
                flash(f"Gagal upload gambar: {str(e)}", "error")
                return render_template("admin/hero/form.html", hero=None)

        try:
            supabase.table("hero_slides").insert({
                "judul": judul,
                "deskripsi": deskripsi,
                "image_url": image_url,
                "link_url": link_url,
                "urutan": urutan,
                "aktif": aktif
            }).execute()
            flash("Hero slide berhasil ditambahkan!", "success")
            return redirect(url_for('admin.list_hero'))
        except Exception as e:
            flash(f"Gagal menambah hero slide: {str(e)}", "error")
            
    return render_template("admin/hero/form.html", hero=None)

@admin_bp.route("/hero/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_hero(id):
    supabase = get_supabase_client()
    
    if request.method == "POST":
        judul = request.form.get("judul")
        deskripsi = request.form.get("deskripsi")
        link_url = request.form.get("link_url")
        urutan = request.form.get("urutan", type=int, default=0)
        aktif = "aktif" in request.form
        
        image_file = request.files.get("image_file")
        image_url = request.form.get("image_url") # Current URL
        
        if image_file and image_file.filename != '':
            try:
                file_path = f"{slugify(judul)}_{image_file.filename}"
                file_content = image_file.read()
                
                supabase.storage.from_("hero-images").upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": image_file.content_type}
                )
                
                public_res = supabase.storage.from_("hero-images").get_public_url(file_path)
                image_url = public_res
            except Exception as e:
                flash(f"Gagal upload gambar baru: {str(e)}", "error")

        try:
            supabase.table("hero_slides").update({
                "judul": judul,
                "deskripsi": deskripsi,
                "image_url": image_url,
                "link_url": link_url,
                "urutan": urutan,
                "aktif": aktif
            }).eq("id", id).execute()
            flash("Hero slide berhasil diperbarui!", "success")
            return redirect(url_for('admin.list_hero'))
        except Exception as e:
            flash(f"Gagal memperbarui hero slide: {str(e)}", "error")
            
    # GET: Fetch existing data
    try:
        res = supabase.table("hero_slides").select("*").eq("id", id).single().execute()
        hero = res.data
    except Exception as e:
        flash("Hero slide tidak ditemukan.", "error")
        return redirect(url_for('admin.list_hero'))
        
    return render_template("admin/hero/form.html", hero=hero)

@admin_bp.route("/hero/hapus/<id>", methods=["POST"])
@login_required
def hapus_hero(id):
    supabase = get_supabase_client()
    try:
        supabase.table("hero_slides").delete().eq("id", id).execute()
        flash("Hero slide berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus hero slide: {str(e)}", "error")
    return redirect(url_for('admin.list_hero'))

# --- PENGADUAN MANAGEMENT (Phase 4.6) ---
@admin_bp.route("/pengaduan")
@login_required
def list_pengaduan():
    supabase = get_supabase_client()
    search = request.args.get("search", "")
    status_filter = request.args.get("status", "")
    
    try:
        query = supabase.table("pengaduan").select("*").order("created_at", desc=True)
        
        if search:
            query = query.ilike("judul", f"%{search}%")
        if status_filter:
            query = query.eq("status", status_filter)
            
        res = query.execute()
        pengaduan_list = res.data
    except Exception as e:
        flash(f"Gagal mengambil data pengaduan: {str(e)}", "error")
        pengaduan_list = []
    
    return render_template("admin/pengaduan/index.html", pengaduan_list=pengaduan_list, search=search, status_filter=status_filter)

@admin_bp.route("/pengaduan/<id>")
@login_required
def detail_pengaduan(id):
    supabase = get_supabase_client()
    try:
        res = supabase.table("pengaduan").select("*").eq("id", id).single().execute()
        item = res.data
        if not item:
            flash("Pengaduan tidak ditemukan.", "error")
            return redirect(url_for('admin.list_pengaduan'))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('admin.list_pengaduan'))
        
    return render_template("admin/pengaduan/detail.html", item=item)

@admin_bp.route("/pengaduan/<id>/update", methods=["POST"])
@login_required
def update_pengaduan(id):
    status = request.form.get("status")
    admin_notes = request.form.get("admin_notes")
    
    supabase = get_supabase_client()
    try:
        supabase.table("pengaduan").update({
            "status": status,
            "admin_notes": admin_notes,
            "updated_at": "now()"
        }).eq("id", id).execute()
        flash("Status pengaduan berhasil diperbarui!", "success")
    except Exception as e:
        flash(f"Gagal memperbarui pengaduan: {str(e)}", "error")
        
    return redirect(url_for('admin.detail_pengaduan', id=id))

# --- MASTER LAYANAN CRUD (Phase 4.7) ---
@admin_bp.route("/layanan")
@login_required
def list_layanan():
    supabase = get_supabase_client()
    try:
        res = supabase.table("layanan").select("*").order("urutan").execute()
        layanan_list = res.data
    except Exception as e:
        flash(f"Gagal mengambil data layanan: {str(e)}", "error")
        layanan_list = []
    return render_template("admin/layanan/index.html", layanan_list=layanan_list)

@admin_bp.route("/layanan/tambah", methods=["GET", "POST"])
@login_required
def tambah_layanan():
    if request.method == "POST":
        data = {
            "nama": request.form.get("nama"),
            "deskripsi": request.form.get("deskripsi"),
            "icon_name": request.form.get("icon_name"),
            "url_path": request.form.get("url_path"),
            "kategori": request.form.get("kategori"),
            "urutan": request.form.get("urutan", type=int) or 0,
            "aktif": "aktif" in request.form
        }
        supabase = get_supabase_client()
        try:
            supabase.table("layanan").insert(data).execute()
            flash("Layanan berhasil ditambahkan!", "success")
            return redirect(url_for('admin.list_layanan'))
        except Exception as e:
            flash(f"Gagal menambah layanan: {str(e)}", "error")
    return render_template("admin/layanan/form.html", layanan=None)

@admin_bp.route("/layanan/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_layanan(id):
    supabase = get_supabase_client()
    if request.method == "POST":
        data = {
            "nama": request.form.get("nama"),
            "deskripsi": request.form.get("deskripsi"),
            "icon_name": request.form.get("icon_name"),
            "url_path": request.form.get("url_path"),
            "kategori": request.form.get("kategori"),
            "urutan": request.form.get("urutan", type=int) or 0,
            "aktif": "aktif" in request.form
        }
        try:
            supabase.table("layanan").update(data).eq("id", id).execute()
            flash("Layanan berhasil diperbarui!", "success")
            return redirect(url_for('admin.list_layanan'))
        except Exception as e:
            flash(f"Gagal memperbarui layanan: {str(e)}", "error")
    
    try:
        res = supabase.table("layanan").select("*").eq("id", id).single().execute()
        layanan = res.data
    except Exception:
        flash("Layanan tidak ditemukan.", "error")
        return redirect(url_for('admin.list_layanan'))
    return render_template("admin/layanan/form.html", layanan=layanan)

@admin_bp.route("/layanan/hapus/<id>", methods=["POST"])
@login_required
def hapus_layanan(id):
    supabase = get_supabase_client()
    try:
        supabase.table("layanan").delete().eq("id", id).execute()
        flash("Layanan berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus layanan: {str(e)}", "error")
    return redirect(url_for('admin.list_layanan'))

# --- MANAJEMEN KEBENCANAAN CRUD (Phase 4.7) ---
@admin_bp.route("/bencana")
@login_required
def list_bencana():
    supabase = get_supabase_client()
    try:
        res = supabase.table("bencana").select("*").order("created_at", desc=True).execute()
        bencana_list = res.data
    except Exception as e:
        flash(f"Gagal mengambil data bencana: {str(e)}", "error")
        bencana_list = []
    return render_template("admin/bencana/index.html", bencana_list=bencana_list)

@admin_bp.route("/bencana/tambah", methods=["GET", "POST"])
@login_required
def tambah_bencana():
    if request.method == "POST":
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        
        data = {
            "judul": request.form.get("judul"),
            "lokasi": request.form.get("lokasi"),
            "tingkat_bahaya": request.form.get("tingkat_bahaya"),
            "deskripsi": request.form.get("deskripsi"),
            "lat": float(lat) if lat and lat != 'None' else None,
            "lng": float(lng) if lng and lng != 'None' else None,
            "aktif": "aktif" in request.form
        }
        supabase = get_supabase_client()
        try:
            supabase.table("bencana").insert(data).execute()
            flash("Laporan bencana berhasil ditambahkan!", "success")
            return redirect(url_for('admin.list_bencana'))
        except Exception as e:
            flash(f"Gagal menambah laporan bencana: {str(e)}", "error")
    return render_template("admin/bencana/form.html", bencana=None)

@admin_bp.route("/bencana/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_bencana(id):
    supabase = get_supabase_client()
    if request.method == "POST":
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        
        data = {
            "judul": request.form.get("judul"),
            "lokasi": request.form.get("lokasi"),
            "tingkat_bahaya": request.form.get("tingkat_bahaya"),
            "deskripsi": request.form.get("deskripsi"),
            "lat": float(lat) if lat and lat != 'None' else None,
            "lng": float(lng) if lng and lng != 'None' else None,
            "aktif": "aktif" in request.form
        }
        try:
            supabase.table("bencana").update(data).eq("id", id).execute()
            flash("Laporan bencana berhasil diperbarui!", "success")
            return redirect(url_for('admin.list_bencana'))
        except Exception as e:
            flash(f"Gagal memperbarui laporan bencana: {str(e)}", "error")
            
    try:
        res = supabase.table("bencana").select("*").eq("id", id).single().execute()
        bencana = res.data
    except Exception:
        flash("Data bencana tidak ditemukan.", "error")
        return redirect(url_for('admin.list_bencana'))
    return render_template("admin/bencana/form.html", bencana=bencana)

@admin_bp.route("/bencana/hapus/<id>", methods=["POST"])
@login_required
def hapus_bencana(id):
    supabase = get_supabase_client()
    try:
        supabase.table("bencana").delete().eq("id", id).execute()
        flash("Laporan bencana berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus laporan bencana: {str(e)}", "error")
    return redirect(url_for('admin.list_bencana'))

# --- MANAJEMEN PARIWISATA CRUD (Phase 4.7) ---
@admin_bp.route("/pariwisata")
@login_required
def list_pariwisata():
    supabase = get_supabase_client()
    try:
        res = supabase.table("pariwisata").select("*").order("created_at", desc=True).execute()
        wisata_list = res.data
    except Exception as e:
        flash(f"Gagal mengambil data pariwisata: {str(e)}", "error")
        wisata_list = []
    return render_template("admin/pariwisata/index.html", wisata_list=wisata_list)

@admin_bp.route("/pariwisata/tambah", methods=["GET", "POST"])
@login_required
def tambah_pariwisata():
    if request.method == "POST":
        # Handle multiple photo uploads
        files = request.files.getlist("foto_files")
        foto_urls = []
        supabase = get_supabase_client()
        
        for file in files:
            if file and file.filename != '':
                try:
                    file_path = f"wisata/{slugify(request.form.get('nama'))}_{file.filename}"
                    file_content = file.read()
                    supabase.storage.from_("pariwasa-foto").upload(
                        path=file_path,
                        file=file_content,
                        file_options={"content-type": file.content_type}
                    )
                    url = supabase.storage.from_("pariwasa-foto").get_public_url(file_path)
                    foto_urls.append(url)
                except Exception as e:
                    flash(f"Gagal upload foto: {str(e)}", "error")

        lat = request.form.get("lat")
        lng = request.form.get("lng")

        data = {
            "nama": request.form.get("nama"),
            "deskripsi": request.form.get("deskripsi"),
            "alamat": request.form.get("alamat"),
            "kategori": request.form.get("kategori"),
            "lat": float(lat) if lat and lat != 'None' else None,
            "lng": float(lng) if lng and lng != 'None' else None,
            "foto_urls": foto_urls
        }
        
        try:
            supabase.table("pariwisata").insert(data).execute()
            flash("Data pariwisata berhasil ditambahkan!", "success")
            return redirect(url_for('admin.list_pariwisata'))
        except Exception as e:
            flash(f"Gagal menambah data pariwisata: {str(e)}", "error")
            
    return render_template("admin/pariwisata/form.html", wisata=None)

@admin_bp.route("/pariwisata/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_pariwisata(id):
    supabase = get_supabase_client()
    
    if request.method == "POST":
        # Handle multiple photo uploads (append or replace? replacement is simpler for MVP)
        files = request.files.getlist("foto_files")
        foto_urls = request.form.getlist("existing_foto_urls") # Keep existing ones if any
        
        for file in files:
            if file and file.filename != '':
                try:
                    file_path = f"wisata/{slugify(request.form.get('nama'))}_{file.filename}"
                    file_content = file.read()
                    supabase.storage.from_("pariwasa-foto").upload(
                        path=file_path,
                        file=file_content,
                        file_options={"content-type": file.content_type}
                    )
                    url = supabase.storage.from_("pariwasa-foto").get_public_url(file_path)
                    foto_urls.append(url)
                except Exception as e:
                    flash(f"Gagal upload foto baru: {str(e)}", "error")

        lat = request.form.get("lat")
        lng = request.form.get("lng")

        data = {
            "nama": request.form.get("nama"),
            "deskripsi": request.form.get("deskripsi"),
            "alamat": request.form.get("alamat"),
            "kategori": request.form.get("kategori"),
            "lat": float(lat) if lat and lat != 'None' else None,
            "lng": float(lng) if lng and lng != 'None' else None,
            "foto_urls": foto_urls
        }
        
        try:
            supabase.table("pariwisata").update(data).eq("id", id).execute()
            flash("Data pariwisata berhasil diperbarui!", "success")
            return redirect(url_for('admin.list_pariwisata'))
        except Exception as e:
            flash(f"Gagal memperbarui data pariwisata: {str(e)}", "error")
            
    try:
        res = supabase.table("pariwisata").select("*").eq("id", id).single().execute()
        wisata = res.data
    except Exception:
        flash("Data pariwisata tidak ditemukan.", "error")
        return redirect(url_for('admin.list_pariwisata'))
        
    return render_template("admin/pariwisata/form.html", wisata=wisata)

@admin_bp.route("/pariwisata/hapus/<id>", methods=["POST"])
@login_required
def hapus_pariwisata(id):
    supabase = get_supabase_client()
    try:
        supabase.table("pariwisata").delete().eq("id", id).execute()
        flash("Data pariwisata berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus data pariwisata: {str(e)}", "error")
    return redirect(url_for('admin.list_pariwisata'))
