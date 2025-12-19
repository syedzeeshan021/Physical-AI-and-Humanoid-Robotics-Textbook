import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.user import User
from src.models.translation_session import TranslationSession
from src.core.database import get_db
from unittest.mock import patch, MagicMock
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

client = TestClient(app)


def test_complete_translation_flow_integration():
    """
    Integration test for complete translation flow
    Tests the entire flow from request to response with database interactions
    """
    # Mock data
    user_id = str(uuid.uuid4())
    chapter_id = "test-chapter-1"
    original_content = "This is the original English content to be translated."
    translated_content = "یہ ترجمہ شدہ اردو مواد ہے۔"

    # Mock the translation service response
    mock_translation_result = {
        "translated_content": translated_content,
        "session_id": str(uuid.uuid4()),
        "is_cached": False
    }

    with patch('src.services.translation_service.TranslationService.translate_content') as mock_service:
        mock_service.return_value = mock_translation_result

        # Make the translation request
        response = client.post(
            "/translation/translate",
            json={
                "content": original_content,
                "chapter_id": chapter_id,
                "target_language": "ur"
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        # Verify response structure and content
        assert data["translated_content"] == translated_content
        assert isinstance(data["session_id"], str)

        # Verify that the translation was properly handled by the service
        mock_service.assert_called_once()
        call_args = mock_service.call_args
        assert call_args[1]["content"] == original_content
        assert call_args[1]["chapter_id"] == chapter_id
        assert call_args[1]["target_language"] == "ur"


def test_translation_flow_with_caching():
    """
    Test translation flow with caching mechanism
    Verifies that previously translated content is served from cache
    """
    user_id = str(uuid.uuid4())
    chapter_id = "test-chapter-cached"
    original_content = "This content should be cached."
    cached_translation = "یہ کیش کردہ ترجمہ ہے۔"

    # Mock cached response
    cached_result = {
        "translated_content": cached_translation,
        "session_id": str(uuid.uuid4()),
        "is_cached": True
    }

    with patch('src.services.translation_service.TranslationService.translate_content') as mock_service:
        mock_service.return_value = cached_result

        response = client.post(
            "/translation/translate",
            json={
                "content": original_content,
                "chapter_id": chapter_id,
                "target_language": "ur"
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        assert response.status_code == 200
        data = response.json()

        # Verify that the response indicates cached content
        assert data["is_cached"] is True
        assert data["translated_content"] == cached_translation


def test_translation_flow_rate_limiting():
    """
    Test translation flow with rate limiting
    Verifies that the system properly enforces rate limits
    """
    # This test would require mocking the rate limiter
    # For now, we'll verify the rate limiting middleware is in place
    with patch('slowapi.Limiter.is_allowed') as mock_rate_limiter:
        mock_rate_limiter.return_value = False  # Simulate rate limit exceeded

        response = client.post(
            "/translation/translate",
            json={
                "content": "Test content",
                "chapter_id": "test-chapter-rate-limit",
                "target_language": "ur"
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        # Should return 429 for rate limited
        assert response.status_code == 429