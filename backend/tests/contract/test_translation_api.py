import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.user import User
from src.core.database import get_db
from unittest.mock import patch
import uuid
from datetime import datetime

client = TestClient(app)

def test_translation_api_contract():
    """
    Contract test for POST /api/translate endpoint
    Validates the API contract defined in the specification
    """
    # Mock user data for testing
    user_id = str(uuid.uuid4())

    # Mock translation service response
    mock_translation_response = {
        "translated_content": "یہ اردو میں ترجمہ کردہ مواد ہے",
        "session_id": str(uuid.uuid4()),
        "is_cached": False
    }

    # Test the translation endpoint with mocked service
    with patch('src.services.translation_service.TranslationService.translate_content') as mock_service:
        mock_service.return_value = mock_translation_response

        response = client.post(
            "/translation/translate",
            json={
                "content": "This is the content to translate",
                "chapter_id": "test-chapter-1",
                "target_language": "ur"
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        # Assert the response structure matches the contract
        assert response.status_code == 200
        data = response.json()

        # Check that required fields are present in response
        assert "translated_content" in data
        assert "session_id" in data

        # Check that the response matches expected types
        assert isinstance(data["translated_content"], str)
        assert isinstance(data["session_id"], str)
        assert isinstance(data.get("is_cached", True), bool)


def test_translation_api_contract_missing_fields():
    """
    Test that API properly handles missing required fields
    """
    response = client.post(
        "/translation/translate",
        json={
            "content": "This is the content to translate"
            # Missing chapter_id which should be required
        },
        headers={"Authorization": "Bearer fake-jwt-token"}
    )

    # Should return 422 for validation error or 400 for bad request
    assert response.status_code in [400, 422]


def test_translation_api_contract_unauthorized():
    """
    Test that API properly handles unauthorized requests
    """
    response = client.post(
        "/translation/translate",
        json={
            "content": "This is the content to translate",
            "chapter_id": "test-chapter-1"
        }
        # No authorization header
    )

    # Should return 401 for unauthorized access
    assert response.status_code == 401