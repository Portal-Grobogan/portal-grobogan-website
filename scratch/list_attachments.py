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
        bucket_name = "pengaduan-lampiran"
        res = supabase.storage.from_(bucket_name).list("pengaduan")
        print(f"Files in '{bucket_name}/pengaduan/':")
        if res:
             for f in res:
                 print(f"- {f['name']}")
        else:
             print("No files found or empty folder.")
            
    except Exception as e:
        print(f"Error listing files: {str(e)}")
