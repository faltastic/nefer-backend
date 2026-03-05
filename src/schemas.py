from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class ProfileGenerateRequest(BaseModel):
    url: str
    user_type: Optional[str] = None

class ProfileCard(BaseModel):
    url: Optional[str] = ""
    name: Optional[str] = ""
    profile_type: Optional[str] = ""
    short_description: Optional[str] = ""
    long_description: Optional[str] = ""
    image_urls: List[str] = []
    keywords: List[str] = []
    debug_data: Optional[dict] = None
