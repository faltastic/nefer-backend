import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.ai_service import GeminiAIService

@pytest.mark.asyncio
async def test_analyze_profile_success(mocker):
    # Mock settings
    mocker.patch('src.services.ai_service.settings.GEMINI_API_KEY', 'fake_key')
    
    # Mock Gemini Client
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "name": "Test Artist",
        "profile_type": "Photographer",
        "short_description": "A test photographer.",
        "long_description": "A test photographer who loves testing.",
        "image_urls": ["url1", "url2", "url3"],
        "instagram_link": "https://instagram.com/test",
        "keywords": ["#test", "#photography"]
    })
    
    # Correctly mock the nested async call: client.aio.models.generate_content
    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)
    
    # Mock _get_gemini_client to return our mock_client
    service = GeminiAIService()
    mocker.patch.object(service, '_get_gemini_client', return_value=mock_client)
    
    extracted_data = {
        "text": "Some profile text",
        "images": ["url1", "url2", "url3", "url4"],
        "links": ["https://instagram.com/test"],
        "metadata": {"title": "Test Title"}
    }
    
    result = await service.analyze_profile(extracted_data)
    
    assert result["name"] == "Test Artist"
    assert result["profile_type"] == "Photographer"
    assert len(result["keywords"]) == 2
    mock_client.aio.models.generate_content.assert_called_once()

@pytest.mark.asyncio
async def test_analyze_profile_no_api_key(mocker):
    mocker.patch('src.services.ai_service.settings.GEMINI_API_KEY', '')
    service = GeminiAIService()
    
    with pytest.raises(ValueError, match="GEMINI_API_KEY is not configured"):
        await service.analyze_profile({"text": "test"})

@pytest.mark.asyncio
async def test_analyze_profile_failure(mocker):
    mocker.patch('src.services.ai_service.settings.GEMINI_API_KEY', 'fake_key')
    
    mock_client = MagicMock()
    mock_client.aio.models.generate_content = AsyncMock(side_effect=Exception("API Error"))
    
    service = GeminiAIService()
    mocker.patch.object(service, '_get_gemini_client', return_value=mock_client)
    
    with pytest.raises(RuntimeError, match="Gemini analysis failed"):
        await service.analyze_profile({"text": "test", "images": [], "links": []})

@pytest.mark.asyncio
async def test_analyze_profile_url_only(mocker):
    mocker.patch('src.services.ai_service.settings.GEMINI_API_KEY', 'fake_key')
    
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "name": "Test Artist",
        "profile_type": "Photographer",
        "short_description": "A test photographer.",
        "long_description": "A test photographer who loves testing.",
        "image_urls": ["url1"],
        "instagram_link": "https://instagram.com/test",
        "keywords": ["#test"]
    })
    
    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)
    
    service = GeminiAIService()
    mocker.patch.object(service, '_get_gemini_client', return_value=mock_client)
    
    result = await service.analyze_profile(url="https://instagram.com/test_artist")
    
    assert result["name"] == "Test Artist"
    mock_client.aio.models.generate_content.assert_called_once()
    
    # Check that "Either extracted_data or url must be provided" is raised
    with pytest.raises(ValueError, match="Either extracted_data or url must be provided"):
        await service.analyze_profile()
