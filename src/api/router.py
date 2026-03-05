from fastapi import APIRouter
from src.api import profiles

api_router = APIRouter()
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
