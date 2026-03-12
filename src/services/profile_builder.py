import asyncio
from urllib.parse import urlparse
from src.services.extractor import extract_url
from src.services.ai_service import ai_service

async def build_profile_from_url(url: str, user_type: str = None) -> dict:
    """
    Core business logic to extract a profile from a URL and analyze it with AI.
    This function is framework-agnostic and portable.
    """
    parsed_url = urlparse(url)
    is_instagram = "instagram.com" in parsed_url.netloc.lower()

    extracted_data = {}

    # 1. Extract the URL (run in executor since it's blocking)
    loop = asyncio.get_event_loop()
    extracted_data = await loop.run_in_executor(None, extract_url, url)
    
    # print(f"\n--- Extracted Data ---")
    # print(extracted_data)

    if not extracted_data.get("text") and not extracted_data.get("images") and not is_instagram:
        raise ValueError("Could not extract any content from the provided URL.")

    # 2. Analyze with Gemini
    ai_result = await ai_service.analyze_profile(extracted_data=extracted_data, url=url, user_type=user_type)
    
    # 4. Construct response dictionary
    response_dict = ai_result.copy()
    response_dict["url"] = url

    # Sanitize AI results to replace None with appropriate empty values
    for key in ["name", "profile_type", "short_description", "long_description"]:
        if response_dict.get(key) is None:
            response_dict[key] = ""
    for key in ["image_urls", "keywords"]:
        if response_dict.get(key) is None:
            response_dict[key] = []
            
    response_dict["debug_data"] = {
        "extractor_used": "gemini_direct" if is_instagram else extracted_data.get("extractor", "unknown"),
        "extracted_text_length": len(extracted_data.get("text", "")) if extracted_data else 0,
        "extracted_images_count": len(extracted_data.get("images", [])) if extracted_data else 0,
        "extracted_links_count": len(extracted_data.get("links", [])) if extracted_data else 0,
        "about_page_found": "\n\n--- ABOUT PAGE ---\n\n" in extracted_data.get("text", "") if extracted_data else False,
        "metadata": extracted_data.get("metadata", {}) if extracted_data else {},
        "raw_extracted_data": extracted_data if extracted_data else None
    }
    return response_dict
