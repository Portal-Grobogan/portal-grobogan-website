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
        # We can't easily query enum types directly through the client, 
        # but we can try to insert a test record and see if it fails.
        # Or better, just try to FETCH if there are any records.
        res = supabase.table("pengaduan").select("status").execute()
        if res.data:
            statuses = set(r['status'] for r in res.data)
            print(f"Existing statuses in DB: {statuses}")
        else:
            print("No records yet to check enum values.")
    except Exception as e:
        print(f"Error: {str(e)}")
