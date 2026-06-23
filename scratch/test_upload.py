import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not found.")
else:
    supabase = create_client(url, key)
    try:
        bucket_name = "pengaduan-lampiran"
        file_path = "test_upload_folder/test.txt"
        content = b"Hello Supabase Storage"
        
        print(f"Uploading to {bucket_name}/{file_path}...")
        res = supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=content,
            file_options={"content-type": "text/plain"}
        )
        print(f"Upload Result: {res}")
        
        url_res = supabase.storage.from_(bucket_name).get_public_url(file_path)
        print(f"Generated URL: {url_res}")
        
    except Exception as e:
        print(f"Upload failed: {str(e)}")
