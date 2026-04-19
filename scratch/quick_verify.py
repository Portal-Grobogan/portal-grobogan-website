import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

supabase = create_client(url, key)
row_id = supabase.table("pengaduan").select("id").limit(1).execute().data[0]['id']

def test(val):
    try:
        supabase.table("pengaduan").update({"status": val}).eq("id", row_id).execute()
        return True
    except:
        return False

print(f"baru: {test('baru')}")
print(f"proses: {test('proses')}")
print(f"diproses: {test('diproses')}")
print(f"selesai: {test('selesai')}")
print(f"ditolak: {test('ditolak')}")
