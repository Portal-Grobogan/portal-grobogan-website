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
        file_path = "test_upload_folder/test.png"
        content = b"fake image content"
        
        print(f"Uploading to {bucket_name}/{file_path} as image/png...")
        res = supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=content,
            file_options={"content-type": "image/png"}
        )
        print(f"Upload Result: {res}")
        
    except Exception as e:
        print(f"Upload failed: {str(e)}")
