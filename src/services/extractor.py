from trafilatura.settings import DEFAULT_CONFIG
import trafilatura
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests

# --- Trafilatura (General-Purpose) Extractor ---
def extract_generic_url(url: str) -> dict:
    config = DEFAULT_CONFIG
    config.set("DEFAULT", "USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html_content = response.text
        
        # 1. Use trafilatura to extract main text and metadata
        text = trafilatura.extract(html_content, config=config, include_links=True) or ""
        metadata_obj = trafilatura.extract_metadata(html_content)
        metadata = {}
        if metadata_obj:
            for k, v in metadata_obj.as_dict().items():
                # Convert complex types like lxml.etree._Element to string
                metadata[k] = str(v) if v is not None and not isinstance(v, (str, int, float, bool, list, dict)) else v
        
        # 2. Use BeautifulSoup to extract images and links
        soup = BeautifulSoup(html_content, 'html.parser')
        
        raw_images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                raw_images.append(src)
                
        raw_links = []
        for a in soup.find_all('a'):
            href = a.get('href')
            if href:
                raw_links.append(href)

        # Sanitize Images
        images = []
        valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
        for src in raw_images:
            if src.startswith(('data:image/', 'data:application/')):
                continue
                
            full_url = urljoin(url, src)
            parsed_img_url = urlparse(full_url)
            
            # Clean query parameters for cleaner URLs (optional, but helps save tokens)
            # Only keep path, drop query for typical image extensions if it looks tracking heavy
            # Actually, sometimes query params are needed for CDNs (like ?v=...). Let's just limit length.
            if len(full_url) > 300:
                continue
                
            # Basic extension check (optional, but good for filtering out tracking pixels)
            if any(parsed_img_url.path.lower().endswith(ext) for ext in valid_extensions) or not parsed_img_url.path:
                images.append(full_url)
            else:
                images.append(full_url) # keep it just in case, length limit already helps

        # Sanitize Links
        links = []
        for href in raw_links:
            if href.startswith(('javascript:', 'mailto:', 'tel:', 'data:')):
                continue
            
            full_url = urljoin(url, href)
            # Remove query params from links to reduce tracking token bloat
            parsed_link = urlparse(full_url)
            clean_link = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
            
            if len(clean_link) <= 300:
                links.append(clean_link)

        # 3. Check /about page if possible
        parsed_url = urlparse(url)
        if parsed_url.path == "" or parsed_url.path == "/":
            about_url = urljoin(url, "/about")
            try:
                about_resp = requests.get(about_url, headers=headers, timeout=10)
                if about_resp.status_code == 200:
                    about_text = trafilatura.extract(about_resp.text, config=config)
                    if about_text:
                        text += "\n\n--- ABOUT PAGE ---\n\n" + about_text
            except Exception:
                pass # Ignore about page errors
                
        # Remove duplicates while preserving order
        images = list(dict.fromkeys(images))[:20] # Hard limit to top 20
        links = list(dict.fromkeys(links))[:20]   # Hard limit to top 20
        
        return {
            "extractor": "trafilatura",
            "text": text,
            "images": images,
            "links": links,
            "metadata": metadata
        }
    except Exception as e:
        print(f"Generic extracting failed for {url}: {e}")
        return {"extractor": "trafilatura_failed", "text": "", "images": [], "links": [], "metadata": {}}

def extract_instagram_url(url: str) -> dict:
    """
    Dedicated extractor for Instagram URLs.
    Currently uses basic scraping but can be extended to use APIs.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        metadata = {}
        for meta in soup.find_all('meta'):
            if meta.get('property'):
                metadata[meta['property']] = meta.get('content')
            elif meta.get('name'):
                metadata[meta['name']] = meta.get('content')
                
        # The title contains the name and username
        if soup.title and soup.title.string:
            metadata['title'] = soup.title.string
                
        text = soup.get_text(separator='\n', strip=True)
        
        images = []
        # Add the og:image (profile picture) to the images list explicitly if it exists
        if metadata.get('og:image'):
            images.append(metadata.get('og:image'))
            
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and not src.startswith(('data:image/', 'data:application/')):
                images.append(urljoin(url, src))
                
        # Remove duplicates while preserving order
        images = list(dict.fromkeys(images))[:20]
        
        return {
            "extractor": "instagram",
            "text": text,
            "images": images,
            "links": [url],
            "metadata": metadata
        }
    except Exception as e:
        print(f"Instagram extracting failed for {url}: {e}")
        return {"extractor": "instagram_failed", "text": "", "images": [], "links": [url], "metadata": {}}

# --- Main Extractor Router ---
def extract_url(url: str) -> dict:
    """
    Routes the extracting task to the appropriate tool based on the URL.
    """
    if "instagram.com" in urlparse(url).netloc.lower():
        return extract_instagram_url(url)
    return extract_generic_url(url)
