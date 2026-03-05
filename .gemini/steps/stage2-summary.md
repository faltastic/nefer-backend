# Stage 2 Implementation Summary

1.  **Web Extracting Service (`src/services/extractor.py`):** Built a general-purpose extractor utilizing `requests`, `BeautifulSoup`, and `trafilatura` to extract main text content, images, and links. It also automatically attempts to check the `/about` route.
2.  **AI Analysis Service (`src/services/ai_service.py`):** Configured the `google-genai` client using the `gemini-2.5-flash` model exactly as shown in the example. It is prompted to extract data strictly adhering to the requested format (Name, type, short & long descriptions, 3 images, Instagram link, and styling keywords) by leveraging structured JSON output.
3.  **Profile Generation API (`src/api/profiles.py`):** Created the `POST /api/v1/profiles/generate` endpoint with Pydantic validation for the URL and optional `user_type`. It integrates the extractor, the AI service, and includes an attempted (but graceful) Supabase database insertion.
4.  **Testing UI (`static/index.html`):** Developed a clean, styled HTML/JS testing interface that calls the API endpoint and displays the generated Profile Card, served directly from the FastAPI root (`/`).

### Debugging Note: `Unterminated string` Error on Instagram

**Issue:** When attempting to extract Instagram profiles, the backend encountered an `Unterminated string` error during Gemini AI analysis. This was caused by massive arrays of base64-encoded SVG images and very long tracking URLs consuming all output tokens and causing repetition loops. Furthermore, Instagram blocked basic requests with a login wall.

**Current Status:** Resolved. Implemented a robust data sanitization layer in `extractor.py` to filter out base64 images and tracking parameters, and limit the number of assets. Added a specific `extract_instagram_url` function that uses a `Googlebot` User-Agent to bypass the login wall and pull valid `og:` meta tags (like `og:image` and `og:description`). Updated the Gemini configuration to increase `max_output_tokens` to 4000 and instructed it to use metadata as a fallback for profile pictures. This successfully eliminated the truncation errors and AI hallucinations.

### Decoupling Profile Storage
Extracted the Supabase database storage logic from `profile_builder.py` into a new, dedicated `src/services/profile_storage.py` service. This allows the frontend to trigger the save action with reviewed data later, rather than automatically saving during the initial URL extraction and analysis.

### TODO: Image Selection Improvement

*   **Action:** Investigate and implement better logic for the AI to select more optimal and representative images from the extracted data for the profile card. The current AI selection process may not always yield the best visual results.

### Architecture Refactoring (The "Flat MVP" Structure)
The project structure was updated to a cleaner, flatter hierarchy to better accommodate MVP additions (like the suggestion engine and email service in Stage 3) while removing deep folder nesting.
- `src/core/config.py` was moved to `src/config.py`.
- `src/db/supabase.py` was moved to `src/database.py`.
- `src/schemas/profile.py` was moved to `src/schemas.py`.
- `src/api/v1/endpoints/profiles.py` was flattened to `src/api/profiles.py` and `src/api/router.py`.

### Logic Portability (`profile_builder.py`)
To ensure the profile generation logic is reusable outside of the web API context (e.g. cron jobs, CLI tools, other scripts), the core execution code was decoupled from FastAPI logic.
- A new service called `build_profile_from_url` was created in `src/services/profile_builder.py`.
- The `generate_profile` HTTP endpoint in `src/api/profiles.py` now serves as a thin wrapper that invokes `build_profile_from_url` and returns a standard FastAPI/Pydantic response.