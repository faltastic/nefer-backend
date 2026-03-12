# MVP Implementation Plan: NextVibe Backend

This plan outlines the staged implementation of the NextVibe MVP as defined in `.gemini/01_mvp_plan.md`.

## Stage 1: Foundation & Setup
**Goal:** Establish the core project structure and external service integrations.

*   [x] **1.1 FastAPI Project Scaffolding:**
    *   Initialize the standard directory structure: `src/api`, `src/core`, `src/services`, `src/models`, `src/db`.
    *   Create `main.py` with the base FastAPI app and CORS configuration.
*   [x] **1.2 Configuration Management:**
    *   Implement `src/core/config.py` using `pydantic-settings`.
    *   Define required environment variables: `SUPABASE_URL`, `SUPABASE_KEY`, `GEMINI_API_KEY`, `RESEND_API_KEY`.
*   [x] **1.3 Database Integration (Supabase):**
    *   Create the Supabase client utility in `src/db/supabase.py`.
    *   Define the `profiles` table schema (id, username, bio, profile_pic_url, keywords, role).
*   [x] **1.4 Dependency Update:**
    *   Add `pydantic-settings`, `python-multipart`, and any necessary database drivers.

## Stage 2: Component 1 - Profile Card Generator & UI
**Goal:** Enable users to generate profile keywords from a URL and visualize the result.

*   [x] **2.1 Web Extracting Service:**
    *   Implement `src/services/extractor.py` using `Requests`, `BeautifulSoup`, and `Trafilatura`.
    *   Add robust sanitization to prevent token exhaustion and handle Instagram metadata extraction.
*   [x] **2.2 AI Analysis Service (Gemini):**
    *   Implement `src/services/ai_service.py` using the `google-genai` SDK.
    *   Develop prompts for Gemini to analyze extracted data and metadata for structured profiles.
*   [x] **2.3 Profile Generation API:**
    *   Create an endpoint `POST /api/v1/profiles/generate` that accepts a URL and orchestrates extraction and AI analysis.
    *   Decouple Supabase storage logic into `src/services/profile_storage.py` for delayed saving after user review.
*   [x] **2.4 Testing UI:**
    *   Create a simple `index.html` (served by FastAPI) with an input field for the URL.
    *   Display a "Profile Card" preview showing the extracted image and AI-generated tags.

## Stage 3: Component 2 - Suggestion Engine & Cron
**Goal:** Implement the weekly matching logic and automated email delivery.

*   [ ] **3.1 Matching Logic:**
    *   Implement `src/services/matching.py` to calculate overlap in keywords between photographers and models.
    *   Ensure matches prioritize complementary roles (Photographer + Model).
*   [ ] **3.2 Email Service (Resend):**
    *   Implement `src/services/email_service.py` to send HTML emails via Resend. (examples https://github.com/resend/resend-examples/blob/main/python-resend-examples/examples/basic_send.py and https://github.com/resend/resend-examples/blob/main/python-resend-examples/examples/scheduled_send.py and https://github.com/resend/resend-examples/blob/main/python-resend-examples/examples/with_template.py and  https://github.com/resend/resend-examples/blob/main/python-resend-examples/examples/fastapi_app.py)
    *   Design a simple Jinja2 template for the "Suggested Collab" email.
*   [ ] **3.3 Scheduling (Cron):**
    *   Create an internal admin endpoint `POST /api/v1/internal/trigger-matching`.
    *   Configure the matching logic to run for all active users and queue emails.

## Stage 4: Testing & Railway Deployment
**Goal:** Ensure reliability and prepare for production hosting.

*   [x] **4.1 Automated Testing:**
    *   Add `pytest` and `httpx` to dev dependencies.
    *   Write unit tests for the extractor (mocking requests).
    *   Write integration tests for the profile generation endpoint.
*   [ ] **4.2 Production Hardening:**
    *   Configure logging.
    *   Add a `/health` endpoint for monitoring.
*   [ ] **4.3 Railway Preparation:**
    *   Create a `Dockerfile` for the FastAPI app.
    *   Create a `railway.toml` to define the deployment environment and cron schedules.
    *   Ensure all environment variables are documented for Railway setup.
