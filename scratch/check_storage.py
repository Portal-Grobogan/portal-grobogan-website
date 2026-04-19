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
        # Check buckets
        buckets = supabase.storage.list_buckets()
        print("Buckets found:")
        for b in buckets:
            print(f"- {b.name} (Public: {b.public})")
            
        bucket_name = "pengaduan-lampiran"
        exists = any(b.name == bucket_name for b in buckets)
        
        if not exists:
            print(f"Bucket '{bucket_name}' DOES NOT EXIST!")
        else:
            print(f"Bucket '{bucket_name}' exists.")
            
    except Exception as e:
        print(f"Error checking storage: {str(e)}")
