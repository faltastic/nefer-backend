import importlib.metadata
import bs4
import requests
import trafilatura
import fastapi
import uvicorn
import jinja2
import markupsafe
import google.genai
import pydantic_settings
import multipart
import supabase

def test_imports():
    print(f"BeautifulSoup version: {bs4.__version__}")
    print(f"requests version: {requests.__version__}")
    print(f"trafilatura version: {importlib.metadata.version('trafilatura')}")
    print(f"fastapi version: {fastapi.__version__}")
    print(f"uvicorn version: {uvicorn.__version__}")
    print(f"jinja2 version: {jinja2.__version__}")
    print(f"markupsafe version: {markupsafe.__version__}")
    print(f"google-genai version: {importlib.metadata.version('google-genai')}")
    print(f"pydantic-settings version: {importlib.metadata.version('pydantic-settings')}")
    print(f"python-multipart version: {importlib.metadata.version('python-multipart')}")
    print(f"supabase version: {importlib.metadata.version('supabase')}")

if __name__ == "__main__":
    test_imports()
