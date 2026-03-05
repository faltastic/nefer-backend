import pytest
from unittest.mock import MagicMock, patch
from src.services.extractor import extract_url, extract_generic_url

def test_extract_url_routes_to_generic():
    with patch('src.services.extractor.extract_generic_url') as mock_generic:
        mock_generic.return_value = {"extractor": "trafilatura", "text": "test"}
        result = extract_url("https://example.com")
        assert result["extractor"] == "trafilatura"
        mock_generic.assert_called_once_with("https://example.com")

def test_extract_url_raises_for_instagram():
    with pytest.raises(ValueError, match="Instagram URLs should be processed directly by the AI service."):
        extract_url("https://www.instagram.com/testuser/")

def test_extract_generic_url_success(mocker):
    # Mock requests.get for main url and about page
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><h1>Test Page</h1><img src='img1.jpg'><a href='/link1'>Link</a></body></html>"
    
    mock_about_response = MagicMock()
    mock_about_response.status_code = 200
    mock_about_response.text = "<html><body>About content</body></html>"
    
    def mock_get(url, *args, **kwargs):
        if url == "https://example.com/about":
            return mock_about_response
        return mock_response
        
    mocker.patch('requests.get', side_effect=mock_get)
    
    # Mock trafilatura
    mocker.patch('trafilatura.extract', side_effect=lambda html, **kwargs: "Test Page text" if "Test Page" in html else "About text")
    mock_metadata = MagicMock()
    mock_metadata.as_dict.return_value = {"title": "Test Title"}
    mocker.patch('trafilatura.extract_metadata', return_value=mock_metadata)
    
    result = extract_generic_url("https://example.com")
    
    assert result["extractor"] == "trafilatura"
    assert "Test Page text" in result["text"]
    assert "About text" in result["text"]
    assert result["images"] == ["https://example.com/img1.jpg"]
    assert result["links"] == ["https://example.com/link1"]
    assert result["metadata"]["title"] == "Test Title"
