import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200 or (
        response.status_code == 400 and "already signed up" in response.json().get("detail", "")
    )
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200 or (
        response.status_code == 400 and "not registered" in response.json().get("detail", "")
    )

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister?email=foo@bar.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
