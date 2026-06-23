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
        # Check total count
        res = supabase.table("pengaduan").select("id", count="exact").execute()
        print(f"Total rows: {res.count}")
        
        # Check rows with status NOT 'baru'
        res_other = supabase.table("pengaduan").select("status").neq("status", "baru").execute()
        if res_other.data:
            print(f"Other statuses found: {set(row['status'] for row in res_other.data)}")
        else:
            print("No statuses other than 'baru' found in DB.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
