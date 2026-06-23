# Mengimpor fungsi create_app dari paket app
from app import create_app

# Membuat instance aplikasi Flask menggunakan factory function
app = create_app()

# Menjalankan aplikasi jika file ini dieksekusi secara langsung
if __name__ == "__main__":
    # Menjalankan server pengembangan Flask dengan mode debug aktif
    app.run(debug=True)