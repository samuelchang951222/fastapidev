import os
from pathlib import Path
from dotenv import load_dotenv

# Read backend/.env
env_file = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_file)

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SECRET_KEY"]