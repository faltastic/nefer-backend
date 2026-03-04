from supabase import create_client, Client
from src.core.config import settings

def get_supabase() -> Client:
    """
    Returns an authenticated Supabase client using environment variables.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Supabase credentials not configured. Please check your .env file.")
        
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Note: The database schema for 'profiles' will be managed on the Supabase dashboard.
# The table 'profiles' will have the following schema based on the MVP plan:
# - id: uuid (Primary Key)
# - username: string
# - bio: text
# - profile_pic_url: string
# - keywords: text[] (Array of strings)
# - role: string (e.g., "Photographer", "Model")
