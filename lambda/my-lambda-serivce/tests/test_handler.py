import json
import pytest
from src.handler import lamdba_handler

def test_lambda_handler_success():
    event = {
        "body": json.dumps({
            "user_id": "U123",
            "name": "Test user",
            "email": "test@example.com"
        })
    }
    result = lamdba_handler(event, None)
    assert result["statusCode"] == 201

    body = json.loads(result["body"])
    assert "user"  in body
    assert body["user"]["user_id"] == "U123"

@pytest.mark.parametrize(
    "payload_data, expected_error_detail",
    [
        (
            {"user_id": "U123", "name": "Test user"},
            "Missing fields: email"
        ),
        (
            {"user_id": "U123", "email": "test@example.com"},
            "Missing fields: name"
        ),
        (
            {"name": "Test user", "email": "test@example.com"},
            "Missing fields: user_id"
        ),
        (
            {},
            "Missing fields: user_id, name, email"
        )
    ]
)
def test_lambda_handler_validation_error(payload_data, expected_error_detail):
    event = {
        "body": json.dumps(payload_data)
    }
    result = lamdba_handler(event, None)
    assert result["statusCode"] == 400

    body = json.loads(result["body"])
    assert "error" in body
    assert body["error"] == "Validation error"
    assert expected_error_detail in body["details"]

    