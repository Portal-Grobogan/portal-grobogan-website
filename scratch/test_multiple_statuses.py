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
        res = supabase.table("pengaduan").select("id").limit(1).execute()
        if res.data:
            row_id = res.data[0]['id']
            print(f"Attempting to update row {row_id} to status 'diproses'...")
            update_res = supabase.table("pengaduan").update({"status": "diproses"}).eq("id", row_id).execute()
            print("Update success! status: diproses")
        else:
            print("No rows found.")
    except Exception as e:
        print(f"Update failed for 'diproses': {str(e)}")
        
        # Try 'selesai'
        try:
             print(f"Attempting to update row {row_id} to status 'selesai'...")
             update_res = supabase.table("pengaduan").update({"status": "selesai"}).eq("id", row_id).execute()
             print("Update success! status: selesai")
        except Exception as e2:
             print(f"Update failed for 'selesai': {str(e2)}")
             
             # Try 'menunggu'
             try:
                  print(f"Attempting to update row {row_id} to status 'menunggu'...")
                  update_res = supabase.table("pengaduan").update({"status": "menunggu"}).eq("id", row_id).execute()
                  print("Update success! status: menunggu")
             except Exception as e3:
                  print(f"Update failed for 'menunggu': {str(e3)}")
