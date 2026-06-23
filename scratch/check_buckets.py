import os
from supabase import create_client
from dotenv import load_dotenv

# Load env from the app's location if needed, but assuming they are in the environment
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in environment.")
else:
    supabase = create_client(url, key)
    try:
        buckets = supabase.storage.list_buckets()
        print("Available Buckets:")
        for bucket in buckets:
            print(f"- {bucket.name} (Public: {bucket.public})")
    except Exception as e:
        print(f"Error listing buckets: {str(e)}")
