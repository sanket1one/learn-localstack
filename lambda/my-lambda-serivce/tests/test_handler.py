import json
import pytest
from src.handler import lambda_handler

def test_lambda_handler_success(monkeypatch):
    # Monkeypatch DB layer to avoid hitting real DynamoDB in unit tests.
    from src import db

    def fake_put_user_item(item):
        return None

    monkeypatch.setattr(db, "put_user_item", fake_put_user_item)

    event = {
        "body": json.dumps({
            "user_id": "U123",
            "name": "Test User",
            "email": "test@example.com",
        })
    }

    result = lambda_handler(event, None)
    assert result["statusCode"] == 201

    body = json.loads(result["body"])
    assert "user" in body
    assert body["user"]["user_id"] == "U123"
    assert body["user"]["status"] == "CREATED"
    assert "created_at" in body["user"]


@pytest.mark.parametrize(
    "payload_data, expected_status",
    [
        # Missing fields
        ({"user_id": "U123", "name": "Test User"}, 400),
        ({"user_id": "U123", "email": "test@example.com"}, 400),
        ({"name": "Test User", "email": "test@example.com"}, 400),
        # Empty string values (violating min_length=1)
        ({"user_id": "", "name": "Test User", "email": "test@example.com"}, 400),
        ({"user_id": "U123", "name": "", "email": "test@example.com"}, 400),
        # Invalid email format
        ({"user_id": "U123", "name": "Test User", "email": "invalid-email"}, 400),
    ]
)
def test_lambda_handler_validation_errors(payload_data, expected_status):
    event = {
        "body": json.dumps(payload_data)
    }

    result = lambda_handler(event, None)
    assert result["statusCode"] == expected_status
    
    body = json.loads(result["body"])
    assert body["error"] == "Validation error"
    assert "details" in body


def test_lambda_handler_invalid_json():
    event = {
        "body": "{invalid-json"
    }

    result = lambda_handler(event, None)
    assert result["statusCode"] == 400
    
    body = json.loads(result["body"])
    assert body["error"] == "Validation error"
    assert "Invalid JSON" in body["details"]