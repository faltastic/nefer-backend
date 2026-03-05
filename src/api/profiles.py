from fastapi import APIRouter, HTTPException
from src.schemas import ProfileGenerateRequest, ProfileCard
from src.services.profile_builder import build_profile_from_url

router = APIRouter()

@router.post("/generate", response_model=ProfileCard)
async def generate_profile(request: ProfileGenerateRequest):
    try:
        # The core logic has been moved to a portable service function
        result_dict = await build_profile_from_url(request.url, request.user_type)
        return ProfileCard(**result_dict)
    except ValueError as e:
        # Catch our custom value errors from the builder
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
