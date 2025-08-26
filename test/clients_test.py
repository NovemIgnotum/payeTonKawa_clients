import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.routes.clients import get_db

client = TestClient(app)

class MockClient:
    name = "Test Client"
    email = "test@example.com"
    phone = "0612345678"
    created_at = "2024-08-03T10:00:00+00:00"
    updated_at = "2024-08-03T10:00:00+00:00"
    id = 1

def override_get_db_create():
    db = MagicMock()
    db.query().filter().first.return_value = None
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.side_effect = lambda obj: setattr(obj, "id", 1)
    db.refresh.return_value = None
    yield db

def override_get_db_exists():
    db = MagicMock()
    db.query().filter().first.return_value = MockClient()
    yield db

def override_get_db_get():
    db = MagicMock()
    db.query().filter().first.return_value = MockClient()
    yield db

def override_get_db_list():
    db = MagicMock()
    db.query().all.return_value = [MockClient(), MockClient()]
    yield db

def override_get_db_update():
    db = MagicMock()
    db.query().filter().first.return_value = MockClient()
    db.commit.return_value = None
    db.refresh.return_value = None
    yield db

def override_get_db_delete():
    db = MagicMock()
    db.query().filter().first.return_value = MockClient()
    db.delete.return_value = None
    db.commit.return_value = None
    yield db

# Test POST /clients (success)
def test_create_client_success():
    app.dependency_overrides[get_db] = override_get_db_create
    payload = {
        "name": "Test Client",
        "email": "test@example.com",
        "phone": "0612345678"
    }
    response = client.post("/api/clients", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Client created successfully."
    assert data["client"]["name"] == "Test Client"

# Test POST /clients (already exists)
def test_create_client_already_exists():
    app.dependency_overrides[get_db] = override_get_db_exists
    payload = {
        "name": "Test Client",
        "email": "test@example.com",
        "phone": "0612345678"
    }
    response = client.post("/api/clients", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "Client with this email already exists."

# Test GET /clients/{client_id}
def test_get_client_success():
    app.dependency_overrides[get_db] = override_get_db_get
    response = client.get("/api/clients/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Client retrieved successfully."
    assert data["client"]["id"] == 1

# Test GET /clients/{client_id} not found
def test_get_client_not_found():
    def override():
        db = MagicMock()
        db.query().filter().first.return_value = None
        yield db
    app.dependency_overrides[get_db] = override
    response = client.get("/api/clients/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Client not found"

# Test GET /clients (list)
def test_get_clients_list():
    app.dependency_overrides[get_db] = override_get_db_list
    response = client.get("/api/clients")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "All clients retrieved successfully."
    assert isinstance(data["clients"], list)
    assert len(data["clients"]) == 2

# Test PUT /clients/{client_id}
def test_update_client_success():
    app.dependency_overrides[get_db] = override_get_db_update
    payload = {
        "phone": "0707070707"
    }
    response = client.put("/api/clients/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Client updated successfully."
    assert data["client"]["id"] == 1

# Test PUT /clients/{client_id} not found
def test_update_client_not_found():
    def override():
        db = MagicMock()
        db.query().filter().first.return_value = None
        yield db
    app.dependency_overrides[get_db] = override
    payload = {
        "phone": "0707070707"
    }
    response = client.put("/api/clients/999", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Client not found"

# Test DELETE /clients/{client_id}
def test_delete_client_success():
    app.dependency_overrides[get_db] = override_get_db_delete
    response = client.delete("/api/clients/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Client deleted successfully."
    assert data["client"]["id"] == 1

# Test DELETE /clients/{client_id} not found
def test_delete_client_not_found():
    def override():
        db = MagicMock()
        db.query().filter().first.return_value = None
        yield db
    app.dependency_overrides[get_db] = override
    response = client.delete("/api/clients/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Client not found"
