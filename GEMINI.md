# Project Overview

The `nefer-backend` project serves as the backend infrastructure for the **NextVibe** platform, an AI-powered service designed to connect creative professionals (photographers, models, brands).

It is designed as an API-first application built with Python. Its primary functions include:
1. **Profile Card Generation:** Scraping creative portfolios and social media using web scraping tools (`BeautifulSoup`, `Requests`, `trafilatura`).
2. **AI Analysis:** Utilizing Google's Gemini Pro Vision (`google-genai`) to analyze images and text from scraped profiles to generate representative tags/keywords.
3. **Collaboration Engine:** A planned system to match complementary users based on AI-extracted styling keywords.

**Core Technologies:**
*   **Framework:** FastAPI (Python >= 3.11)
*   **Server:** Uvicorn
*   **Dependency Management:** `uv`
*   **Web Scraping:** BeautifulSoup4, Requests, Trafilatura
*   **AI Integration:** Google GenAI SDK
*   **Templating:** Jinja2 & MarkupSafe
*   **Planned Infrastructure (from MVP specs):** Supabase (Database), Resend (Emails), Railway/Vercel (Hosting)

# Building and Running

The project utilizes `uv` for lightning-fast dependency management and virtual environment execution.

**Installation & Synchronization:**
```bash
uv sync
```

**Running the Application:**
Currently, a basic entry point exists in `main.py`:
```bash
uv run python main.py
```
*(Once the FastAPI application is fully defined in `main.py` or an `app` module, the typical run command will be: `uv run uvicorn main:app --reload`)*

**Running Tests:**
*(TODO: A test suite structure is partially initiated in `src/tests`. Testing commands will likely involve `pytest`, which needs to be added.)*
```bash
uv run pytest src/tests/
```

# Development Conventions

*   **Dependency Management:** All Python dependencies are managed through `uv` and defined in `pyproject.toml`.
*   **Architecture:** The project is migrating towards a structured API architecture (e.g., `src/api`, `src/core`, `src/services`, `src/db`) to separate routing, business logic, AI interactions, and database operations.
*   **AI & Scraping:** Scraping services and AI processing should be isolated in dedicated modules to maintain clear separation of concerns from standard API endpoints.
