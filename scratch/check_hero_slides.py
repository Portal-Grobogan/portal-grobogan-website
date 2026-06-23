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
        res = supabase.table("hero_slides").select("*").execute()
        if res.data:
            print(f"Total slides: {len(res.data)}")
            print(f"Sample slide: {res.data[0]}")
        else:
            print("Table 'hero_slides' is empty.")
    except Exception as e:
        print(f"Error: {str(e)}")
