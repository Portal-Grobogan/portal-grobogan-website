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
    try:
        # Try to insert a test record with minimal fields
        res = supabase.table("pengaduan").insert({
            "nama_pelapor": "Test System",
            "judul": "Test Insert",
            "deskripsi": "Testing enum values",
            "kategori": "lainnya",
            "status": "Baru"
        }).execute()
        print("Insert successful!")
    except Exception as e:
        print(f"FAILED: {str(e)}")
