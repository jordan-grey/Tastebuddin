# db.py
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv() 


# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create and export a single Supabase client for the whole app
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
