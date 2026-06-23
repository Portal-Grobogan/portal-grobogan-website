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
        # Fetch one record to see columns
        res = supabase.table("berita").select("*").limit(1).execute()
        if res.data:
            print(f"Columns in 'berita': {list(res.data[0].keys())}")
            print(f"Sample data: {res.data[0]}")
        else:
            print("Table 'berita' is empty or not found.")
    except Exception as e:
        print(f"Error: {str(e)}")
