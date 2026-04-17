from flask import Blueprint, render_template, request, redirect, url_for


public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    # Placeholder data for Phase 3 development
    slides = [
        {
            "judul": "Portal Layanan Publik Terpadu",
            "deskripsi": "Akses berbagai layanan pemerintah Kabupaten Grobogan dengan mudah dan transparan dari satu pintu.",
            "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&q=80&w=2070",
            "link_url": "#"
        },
        {
            "judul": "Pengaduan Warga Cepat Tanggap",
            "deskripsi": "Sampaikan aspirasi dan keluhan Anda secara langsung kepada instansi terkait untuk penanganan yang lebih cepat.",
            "image_url": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?auto=format&fit=crop&q=80&w=2069",
            "link_url": "#"
        },
        {
            "judul": "Informasi Kebencanaan Realtime",
            "deskripsi": "Dapatkan update terkini mengenai situasi darurat dan peta rawan bencana di wilayah Grobogan.",
            "image_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=2070",
            "link_url": "#"
        }
    ]
    return render_template("index.html", slides=slides)


@public_bp.route("/berita")
def berita_list():
    return render_template("berita/index.html")


@public_bp.route("/berita/<slug>")
def berita_detail(slug):
    # For now, using shared placeholder data
    item = {
        'judul': slug.replace('-', ' ').title(),
        'kategori': 'Informasi',
        'created_at': None,
        'konten': '<p>Ini adalah konten berita placeholder untuk simulasi layout Fase 3.5. Kabupaten Grobogan terus berbenah dalam meningkatkan kualitas layanan publik bagi seluruh warga masyarakat.</p>'
    }
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
    return render_template("layanan/kebencanaan.html")


@public_bp.route("/layanan/pariwisata")
def layanan_pariwisata():
    return render_template("layanan/pariwisata.html")


@public_bp.route("/pengaduan", methods=["GET", "POST"])
def pengaduan():
    if request.method == "POST":
        # Placeholder logic for submission
        return redirect(url_for('public.pengaduan_sukses', id="GRB-2026-001"))
    return render_template("pengaduan/index.html")


@public_bp.route("/pengaduan/sukses/<id>")
def pengaduan_sukses(id):
    return render_template("pengaduan/sukses.html", id=id)


@public_bp.route("/pengaduan/cek", methods=["GET", "POST"])
def pengaduan_cek():
    hasil = None
    if request.method == "POST":
        # Placeholder result
        hasil = {
            'id': request.form.get('ticket_id'),
            'status': 'Proses',
            'tanggal': '17 April 2026',
            'perihal': 'Perbaikan lampu jalan di Purwodadi'
        }
    return render_template("pengaduan/cek.html", hasil=hasil)
