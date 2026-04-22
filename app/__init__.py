from flask import Flask, render_template
from flask_login import LoginManager, UserMixin

from app.config import Config
from app.routes.public import public_bp

# Inisialisasi Flask-Login untuk manajemen sesi pengguna
login_manager = LoginManager()
# Tentukan endpoint route untuk halaman login jika pengguna belum terautentikasi
login_manager.login_view = "admin.login"


class AdminUser(UserMixin):
    """
    Model pengguna minimal untuk tahap setup Flask-Login.
    Mewarisi UserMixin untuk menyediakan properti default seperti is_authenticated.
    """

    def __init__(self, user_id: str) -> None:
        self.id = user_id


@login_manager.user_loader
def load_user(user_id: str) -> AdminUser:
    """
    Memuat data pengguna dari ID yang tersimpan di sesi.
    """
    # Placeholder loader sementara untuk fase pengembangan.
    return AdminUser(user_id=user_id)


def create_app() -> Flask:
    """
    Application Factory: Fungsi untuk membuat dan mengonfigurasi instance aplikasi Flask.
    """
    app = Flask(__name__)
    
    # Memuat konfigurasi dari objek Config
    app.config.from_object(Config)

    # Impor blueprint admin di dalam fungsi untuk menghindari circular import
    from app.routes.admin import admin_bp

    # Integrasikan Flask-Login dengan aplikasi
    login_manager.init_app(app)
    
    # Mendaftarkan blueprint untuk rute publik dan admin
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    # Handler untuk error 404 (Halaman Tidak Ditemukan)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    # Handler untuk error 500 (Kesalahan Internal Server)
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    return app

