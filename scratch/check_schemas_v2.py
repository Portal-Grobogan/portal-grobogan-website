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
        # Check bencana
        res_b = supabase.table("bencana").select("*").limit(1).execute()
        if res_b.data:
            print(f"Bencana columns: {list(res_b.data[0].keys())}")
            print(f"Bencana sample: {res_b.data[0]}")
        
        # Check pariwisata
        res_p = supabase.table("pariwisata").select("*").limit(1).execute()
        if res_p.data:
            print(f"Pariwisata columns: {list(res_p.data[0].keys())}")
            print(f"Pariwisata sample: {res_p.data[0]}")
    except Exception as e:
        print(f"Error: {str(e)}")
