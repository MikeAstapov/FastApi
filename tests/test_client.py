import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from JWT_auth import app, get_current_active_user

# Create a test client using FastAPI's TestClient
from jwt_models import User

client = TestClient(app)


def test_login_for_access_token():
    # Define the test input data
    form_data = {
        "username": "michael",
        "password": "secret"
    }

    # Send a POST request to the /token endpoint with the test data
    response = client.post("/token", data=form_data)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains the access_token and token_type keys
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_get_current_active_user():
    user1 = User(username='michael', disabled=False)
    user2 = User(username='jane', disabled=True)


    # Test when current user is not disabled
    result1 = get_current_active_user(current_user=user1)
    assert result1 == user1

    # Test when current user is disabled
    with pytest.raises(HTTPException) as exc_info:
        get_current_active_user(current_user=user2)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Inactive user'