from flask import Blueprint, render_template


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


@public_bp.route("/berita/<slug>")
def berita_detail(slug):
    # Placeholder for news detail
    return f"Halaman berita: {slug}"
