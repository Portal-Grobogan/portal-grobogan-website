import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or keys not found in environment.")
else:
    supabase = create_client(url, key)
    try:
        res = supabase.table("pengaduan").select("id").limit(1).execute()
        if res.data:
            row_id = res.data[0]['id']
            
            for status in ['baru', 'proses', 'diproses', 'selesai', 'ditolak']:
                try:
                    print(f"Testing status: '{status}'...")
                    supabase.table("pengaduan").update({"status": status}).eq("id", row_id).execute()
                    print(f"  OK: '{status}' is valid.")
                except Exception as e:
                    print(f"  FAIL: '{status}' is invalid. Error: {str(e)[:50]}...")
        else:
            print("No rows found.")
    except Exception as e:
        print(f"Critical error: {str(e)}")
