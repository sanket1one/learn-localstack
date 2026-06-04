import json
import logging
from typing import Any, Dict, Tuple

from .exceptions import DomainError, PersistenceError, ValidationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _parse_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts the payload from an API Gateway style event or direct invocation.
    """
    if "body" in event:
        body = event["body"]
        if isinstance(body, str):
            try:
                return json.loads(body)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON in body: {e}") from e
        elif isinstance(body, dict):
            return body
        else:
            raise ValidationError("Unsupported body. type")


    if isinstance(event, dict):
        return event
    raise ValidationError("Unsupported body type")


def _validate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic validation for a 'create user'-style payload.
    Extend this with pydantic if you want stricter typing.
    """
    required_fields = ["user_id", "name", "email"]
    missing = [f for f in required_fields if f not in payload]
    if missing:
        raise ValidationError(f"Missing fields: {', '.join(missing)}")
    return payload

def _handle_create_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Domain logic: in the next steps we'll call DynamoDB here.
    For now it just echoes the payload back with a flag.
    """
    try:

        user = {
            "user_id": payload["user_id"],
            "name": payload["name"],
            "email": payload["email"],
            "status": "CREATED"
        }

        return user
    except Exception as e:
        raise PersistenceError(f"Error saving user {payload.get('user_id')}: {e}") from e

def _build_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }

def lamdba_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
        AWS Lambda entry point.
        This is the only function AWS / LocalStack needs to know about.
    """

    logger.info("Received event: %s", json.dumps(event))

    try:
        payload = _parse_event(event)
        payload = _validate_payload(payload)
        user = _handle_create_user(payload)
        return _build_response(201, {"user": user})
    except ValidationError as e:
        logger.warning("Validation error: %s", e)
        return _build_response(400, {"error": "Validation error", "details": str(e)})
    except PersistenceError as e:
        logger.error("Persistence error: %s", e)
        return _build_response(500, {"error": "Persistence error", "details": str(e)})
    except DomainError as e:
        logger.error("Domain error: %s", e)
        return _build_response(500, {"error": "Domain error", "details": str(e)})
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return _build_response(500, {"error": "Unexpected error", "details": str(e)})
