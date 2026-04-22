import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or keys not found in environment.")
else:
    supabase = create_client(url, key)
    # Try lowercase
    try:
        res = supabase.table("pengaduan").insert({
            "nama_pelapor": "Test System",
            "judul": "Test Lowercase",
            "deskripsi": "Testing enum baru",
            "kategori": "lainnya",
            "status": "baru"
        }).execute()
        print("Success with 'baru'!")
    except Exception as e:
        print(f"Failed with 'baru': {str(e)}")

    # Try title case Indonesian
    try:
        res = supabase.table("pengaduan").insert({
            "nama_pelapor": "Test System",
            "judul": "Test Indo",
            "deskripsi": "Testing enum Laporan Masuk",
            "kategori": "lainnya",
            "status": "Laporan Masuk"
        }).execute()
        print("Success with 'Laporan Masuk'!")
    except Exception as e:
        print(f"Failed with 'Laporan Masuk': {str(e)}")
