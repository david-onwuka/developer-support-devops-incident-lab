import os

from fastapi.testclient import TestClient

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://support_user:change_me_local@localhost:5545/support_lab",
)

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_tickets():
    response = client.get("/tickets")
    assert response.status_code == 200

    tickets = response.json()
    assert len(tickets) == 3
    assert tickets[0]["customer_name"] == "Ada Okafor"
