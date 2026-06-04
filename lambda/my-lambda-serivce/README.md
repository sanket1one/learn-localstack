# my-lambda-service

A small, production-leaning Python AWS Lambda service skeleton.

## Structure

```text
my-lambda-service/
  src/
    __init__.py
    handler.py      # Lambda entrypoint
    exceptions.py   # Domain exceptions
  tests/
    __init__.py
    test_handler.py # Unit tests for handler
  requirements.txt
  README.md
```

## Local testing

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest
```

## Lambda handler

Configure AWS / LocalStack to use:

- Runtime: python3.11
- Handler: `src.handler.lambda_handler`