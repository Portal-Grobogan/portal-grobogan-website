# Mengimpor fungsi create_app dari paket app
from app import create_app

# Membuat instance aplikasi untuk dijalankan oleh server WSGI (seperti Gunicorn)
app = create_app()
