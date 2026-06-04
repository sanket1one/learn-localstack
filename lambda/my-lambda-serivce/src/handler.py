import json
import logging
from typing import Any, Dict, Tuple
from datetime import datetime, timezone

from .exceptions import DomainError, PersistenceError, ValidationError
from .models import UserCreate, User
from .db import put_user_item
# pyrefly: ignore [missing-import]
from pydantic import ValidationError as PydanticValidationError

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
    try:
        return UserCreate(**payload)
    except PydanticValidationError as e:
        raise ValidationError(e.errors()) from e

def _handle_create_user(payload: UserCreate) -> User:
    """
    Domain logic: in the next steps we'll call DynamoDB here.
    For now it just echoes the payload back with a flag.
    """
    created_at = datetime.now(timezone.utc)

    item = {
        "pk": f"USER#{payload.user_id}",
        "sk": "PROFILE",
        "user_id": payload.user_id,
        "name": payload.name,
        "email": payload.email,
        "created_at": created_at.isoformat(),
        "status": "CREATED"
    }

    put_user_item(item)


    return User(
        user_id=payload.user_id,
        name=payload.name,
        email=payload.email,
        created_at=created_at,
        status="CREATED",
    )
    

def _build_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
        AWS Lambda entry point.
        This is the only function AWS / LocalStack needs to know about.
    """

    logger.info("Received event: %s", json.dumps(event))

    try:
        payload_dict = _parse_event(event)
        user_create = _validate_payload(payload_dict)
        user = _handle_create_user(user_create)
        return _build_response(201, {"user": user.model_dump(mode='json')})
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
