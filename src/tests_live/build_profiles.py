import asyncio
import json
from src.services.profile_builder import build_profile_from_url

async def main():
    test_urls = [
        "https://thelouqii.com/",
        "https://www.instagram.com/matteo.digiulio/",
        "https://www.instagram.com/grumpy.gigi"
    ]
    
    for url in test_urls:
        print(f"\n--- Testing URL: {url} ---")
        try:
            res = await build_profile_from_url(url)
            print(f"SUCCESS!")
            print(json.dumps(res, indent=2))
        except Exception as e:
            print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
