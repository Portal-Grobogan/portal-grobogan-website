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
        # Fetch status and any other info
        res = supabase.table("pengaduan").select("status").execute()
        if res.data:
            statuses = [row['status'] for row in res.data]
            print(f"Current statuses in DB: {statuses}")
            unique_statuses = set(statuses)
            print(f"Unique statuses: {unique_statuses}")
        else:
            print("No data in pengaduan table.")
            
        # Try to insert a dummy to see if it fails (using rollback-like behavior if possible, or just a new row)
        # But we don't want to mess up the DB.
        
    except Exception as e:
        print(f"Error: {str(e)}")
