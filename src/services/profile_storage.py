from src.database import get_supabase

def store_profile(profile_data: dict) -> dict:
    """
    Stores the final, reviewed profile data in the Supabase database.
    """
    try:
        supabase = get_supabase()
        
        # Format the data for the database schema if needed, 
        # assuming the frontend passes data mapped to the DB columns.
        db_payload = {
            "name": profile_data.get("name", ""),
            "profile_type": profile_data.get("profile_type", ""),
            "short_description": profile_data.get("short_description", ""),
            "long_description": profile_data.get("long_description", ""),
            "image_urls": profile_data.get("image_urls", []),
            "keywords": profile_data.get("keywords", [])
        }
        
        # Execute the insert
        response = supabase.table("profiles").insert(db_payload).execute()
        return response.data
    except ValueError:
        print("Warning: Supabase credentials not configured. Skipping database storage.")
        return None
    except Exception as db_error:
        print(f"Warning: Failed to save to Supabase database. {db_error}")
        return None
