import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
# Try Service Role Key first
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or keys not found in environment.")
else:
    supabase = create_client(url, key)
    try:
        res = supabase.storage.list_buckets()
        if not res:
            print("No buckets found.")
        else:
            print(f"Found {len(res)} buckets:")
            for b in res:
                print(f"- Name: {b.name}, Public: {b.public}, ID: {b.id}")
    except Exception as e:
        print(f"Detailed Error: {str(e)}")
