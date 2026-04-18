from flask import Blueprint, render_template, request, redirect, url_for
from app.config import get_supabase_client


public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    supabase = get_supabase_client()
    
    # 1. Fetch Active Hero Slides
    try:
        slides_res = supabase.table("hero_slides").select("*").eq("aktif", True).order("urutan").execute()
        slides = slides_res.data
        print(f"DEBUG: Found {len(slides)} active slides")
    except Exception as e:
        print(f"DEBUG: Error fetching slides: {str(e)}")
        slides = []

    # 2. Fetch Latest Berita (Limit 6)
    try:
        berita_res = supabase.table("berita").select("*").order("created_at", desc=True).limit(6).execute()
        berita_list = berita_res.data
        print(f"DEBUG: Found {len(berita_list)} berita")
    except Exception as e:
        print(f"DEBUG: Error fetching berita: {str(e)}")
        berita_list = []

    # 3. Fetch Active Layanan (Limit 5)
    try:
        layanan_res = supabase.table("layanan").select("*").eq("aktif", True).order("urutan").limit(5).execute()
        layanan_list = layanan_res.data
    except Exception:
        layanan_list = []

    return render_template("index.html", 
                           slides=slides, 
                           berita_list=berita_list, 
                           layanan_list=layanan_list)


@public_bp.route("/berita")
def berita_list():
    return render_template("berita/index.html")


@public_bp.route("/berita/<id_or_slug>")
def berita_detail(id_or_slug):
    supabase = get_supabase_client()
    try:
        # Try finding by slug first, then by id
        res = supabase.table("berita").select("*").eq("slug", id_or_slug).execute()
        if not res.data:
            res = supabase.table("berita").select("*").eq("id", id_or_slug).execute()
            
        if res.data:
            item = res.data[0]
        else:
            return "Berita tidak ditemukan", 404
    except Exception:
        return "Terjadi kesalahan", 500
        
    return render_template("berita/detail.html", item=item)


@public_bp.route("/profil")
def profil():
    return render_template("profil.html")


@public_bp.route("/layanan")
def layanan():
    return render_template("layanan/index.html")


@public_bp.route("/layanan/kependudukan")
def layanan_kependudukan():
    return render_template("layanan/kependudukan.html")


@public_bp.route("/layanan/kesehatan")
def layanan_kesehatan():
    return render_template("layanan/kesehatan.html")


@public_bp.route("/layanan/kebencanaan")
def layanan_kebencanaan():
    supabase = get_supabase_client()
    try:
        res = supabase.table("bencana").select("*").eq("aktif", True).order("created_at", desc=True).execute()
        bencana_list = res.data
    except Exception:
        bencana_list = []
    return render_template("layanan/kebencanaan.html", bencana_list=bencana_list)


@public_bp.route("/layanan/pariwisata")
def layanan_pariwisata():
    supabase = get_supabase_client()
    try:
        res = supabase.table("pariwisata").select("*").order("created_at", desc=True).execute()
        wisata_list = res.data
    except Exception:
        wisata_list = []
    return render_template("layanan/pariwisata.html", wisata_list=wisata_list)


@public_bp.route("/pengaduan", methods=["GET", "POST"])
def pengaduan():
    if request.method == "POST":
        nama = request.form.get("nama")
        nik = request.form.get("nik")
        contact = request.form.get("contact")
        kategori = request.form.get("kategori")
        judul = request.form.get("judul")
        pesan = request.form.get("pesan")
        lampiran_file = request.files.get("lampiran")
        
        # Determine email/phone but provide a '-' default for NOT NULL columns
        email = contact if "@" in contact else "-"
        nomor_hp = contact if "@" not in contact else "-"
        
        # Merge NIK into description since the table doesn't have a NIK column
        full_description = f"[NIK: {nik}]\n\n{pesan}"
        
        lampiran_url = None
        supabase = get_supabase_client()
        
        # Handle file upload if present
        if lampiran_file and lampiran_file.filename != '':
            try:
                # Use a safe filename
                safe_name = "".join([c if c.isalnum() else "_" for c in nama]).lower()
                file_path = f"pengaduan/{safe_name}_{lampiran_file.filename}"
                file_content = lampiran_file.read()
                
                supabase.storage.from_("pengaduan-lampiran").upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": lampiran_file.content_type}
                )
                lampiran_url = supabase.storage.from_("pengaduan-lampiran").get_public_url(file_path)
            except Exception as e:
                print(f"Attachment upload failed: {str(e)}")

        try:
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
                # Use the generated UUID as ticket ID
                ticket_id = res.data[0]['id']
                return redirect(url_for('public.pengaduan_sukses', id=ticket_id))
        except Exception as e:
            print(f"Error submitting report: {str(e)}")
            return f"Terjadi kesalahan saat menyimpan data: {str(e)}", 500

    return render_template("pengaduan/index.html")


@public_bp.route("/pengaduan/sukses/<id>")
def pengaduan_sukses(id):
    return render_template("pengaduan/sukses.html", id=id)


@public_bp.route("/pengaduan/cek", methods=["GET", "POST"])
def pengaduan_cek():
    hasil = None
    error = None
    if request.method == "POST":
        ticket_id = request.form.get('ticket_id', '').strip()
        if ticket_id:
            supabase = get_supabase_client()
            try:
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