import os

from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    UPLOAD_MAX_SIZE_MB = int(os.getenv("UPLOAD_MAX_SIZE_MB", "10"))


def get_supabase_client() -> Client:
    """
    Returns a Supabase client using service role key when available,
    then falls back to anon key.
    """
    key = Config.SUPABASE_SERVICE_ROLE_KEY or Config.SUPABASE_ANON_KEY
    if not Config.SUPABASE_URL or not key:
        raise RuntimeError("SUPABASE_URL dan key belum diset di .env")
    return create_client(Config.SUPABASE_URL, key)
