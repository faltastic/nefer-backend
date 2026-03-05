import json
from google.genai import Client
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field
from typing import Optional, List
from src.config import settings

MODELS = { "google": "gemini-2.5-flash" }

class ProfileExtractionSchema(BaseModel):
    name: Optional[str] = Field(description="The person's or brand's name")
    profile_type: Optional[str] = Field(description="The type of profile (e.g., Model, Photographer, Brand)")
    short_description: Optional[str] = Field(description="A very brief 1-2 sentence description")
    long_description: Optional[str] = Field(description="A longer description, max 400 characters")
    image_urls: List[str] = Field(description="Select up to 10 representative image URLs from the provided list including one photo of the person if available.")
    keywords: List[str] = Field(description="6 stylistic keywords or tags (e.g., #streetwear, #analog, #portrait)")

class GeminiAIService:
    def __init__(self):
        self._gemini_client: Client | None = None

    async def _get_gemini_client(self) -> Client:
        if self._gemini_client is None:
            self._gemini_client = Client(api_key=settings.GEMINI_API_KEY)
        return self._gemini_client

    async def analyze_profile(self, extracted_data: dict | None = None, url: str | None = None, user_type: str | None = None) -> dict:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured. Please check your .env file.")

        if not extracted_data and not url:
            raise ValueError("Either extracted_data or url must be provided.")

        gemini_client = await self._get_gemini_client()
        model_name = MODELS.get("google")

        system_prompt_content = """
        You are an expert cultural curator that creates a structured profile from a user's data.
        You will be provided with the page metadata, text content, image URLs, and links found on a web page.
        Use the metadata (author, sitename, title) as strong hints for the person's or brand's name.
        
        Identify the user profile type. 
        Rewrite the descriptions if needed, and choose keywords which fit the style, content, mediums of the user.  
        """

        if user_type:
            system_prompt_content += f"\n\nThe user specified their profile type as: {user_type}. Prioritize this type if there is ambiguity."

        if extracted_data:
            content_to_analyze = f"""
            Source URL: {url}
            Page Metadata: {extracted_data.get('metadata', {})}
            Extracted Text: {extracted_data['text'][:5000]} 
            Found Images: {extracted_data['images'][:50]}
            Found Links: {extracted_data['links'][:50]}
            """
        else:
            content_to_analyze = f"Extract profile from this URL: {url}"

        try:
            generate_content_config = GenerateContentConfig(
                temperature=0.5,
                max_output_tokens=3000,
                system_instruction=system_prompt_content,
                response_mime_type="application/json",
                response_schema=ProfileExtractionSchema,
            )

            response = await gemini_client.aio.models.generate_content(
                model=model_name,
                contents=[content_to_analyze],
                config=generate_content_config,
            )

            return json.loads(response.text.strip())

        except Exception as exc:
            raise RuntimeError(f"Gemini analysis failed: {exc}") from exc

ai_service = GeminiAIService()
