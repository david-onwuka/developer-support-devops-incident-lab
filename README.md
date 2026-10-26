# Developer Support & DevOps Incident Lab

A practical support project using FastAPI, PostgreSQL, Docker, and pytest.

## Features
- REST API for retrieving support tickets.
- PostgreSQL database integration.
- Docker Compose setup.
- Automated API tests.
- Simulated database failures and recovery.
- Incident reports and diagnostic logging.

## Run the Project
docker compose up --build -d

## API Endpoints
- GET / — Service status
- GET /health — Health check
- GET /tickets — Retrieve support tickets

## Run Tests
source .venv/bin/activate
pytest -v

## Incident Reports
- Database unavailable
- Missing database table
- Database error logging
