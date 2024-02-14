from fastapi.testclient import TestClient
from ..main import app
from .. import database
from passlib.context import CryptContext
import base64
import json

# Test client instance
client = TestClient(app)

# Test user credentials
USERNAME = "test_email@example.com"
PASSWORD = "Test@pass01"

def get_auth_headers(username: str, password: str) -> dict:
    """Generate basic authentication headers."""
    concatenated_value = f"{username}:{password}"
    headers = {'Authorization': f"Basic {base64.b64encode(concatenated_value.encode('utf-8')).decode('utf-8')}"}
    return headers

###running-pr-02###
########################################################CLEAR DATABASE BEFORE STARTING INTEGRATION TESTING##############################################################
database.clear_database()
########################################################################################################################################################################

########################################################################################################################################################################
#Test 1 - Create an account, and using the GET call, validate account exists.
########################################################################################################################################################################

# Test to create a user successfully
def test_create_user():
    """Test creating a user and validate the response."""

    user_data = {
        "first_name": "testFirstName",
        "last_name": "testLastName",
        "username": USERNAME,
        "password": PASSWORD
    }
    response = client.post("/v1/user/", json=user_data)

    assert response.status_code == 201
    assert response.json()["first_name"] == "testFirstName"
    assert response.json()["last_name"] == "testLastName"
    assert response.json()["username"] == USERNAME


# Test to read user data successfully to validate existence of account
def test_read_main():
    """Test reading user data and validate the response."""
    response = client.get("/v1/user/self", headers=get_auth_headers(USERNAME, PASSWORD))

    assert response.status_code == 200
    assert response.json()["first_name"] == "testFirstName"
    assert response.json()["last_name"] == "testLastName"
    assert response.json()["username"] == USERNAME

########################################################################################################################################################################

# Test to handle failure in creating a user with invalid email format
def test_create_user_failure():
    """Test creating a user with invalid email format and validate the response."""

    invalid_user_data = {
        "first_name": "testFirstName",
        "last_name": "testLastName",
        "username": "invalid_email_example.com",  # Invalid email format
        "password": PASSWORD
    }
    response = client.post("/v1/user/", json=invalid_user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"



# Test to handle failure in reading user data with incorrect password
def test_read_main_failure():
    """Test reading user data with incorrect password and validate the response."""
    invalid_password = "IncorrectPassword"
    response = client.get("/v1/user/self", headers=get_auth_headers(USERNAME, invalid_password))

    assert response.status_code == 401

########################################################################################################################################################################
#Test 2 - Update the account and using the GET call, validate the account was updated.
########################################################################################################################################################################
        
# Test to update user first name successfully
def test_update_first_name():
    """Test updating user first name and validate the response."""

    update_data = {
        "first_name": "testRenameFirstName",
        "last_name": "testRenameLastName",
        "password": PASSWORD
    }
    response = client.put("/v1/user/self", headers=get_auth_headers(USERNAME, PASSWORD), json=update_data)

    assert response.status_code == 204

    # Send a GET request to validate that the account was updated
    updated_response = client.get("/v1/user/self", headers=get_auth_headers(USERNAME, PASSWORD))

    assert updated_response.status_code == 200
    assert updated_response.json()["first_name"] == "testRenameFirstName"
    assert updated_response.json()["last_name"] == "testRenameLastName"

# Test to update user password successfully
def test_update_password():
    """Test updating user password and validate the response."""

    update_data = {
        "first_name": "testRenameFirstName",
        "last_name": "testRenameLastName",
        "password": "TestRename@pass01"
    }
    response = client.put("/v1/user/self", headers=get_auth_headers(USERNAME, PASSWORD), json=update_data)

    assert response.status_code == 204

# Test to read user data after updating password successfully
def test_update_read_pass():
    """Test reading user data after updating password and validate the response."""
    updated_password = "TestRename@pass01"
    response = client.get("/v1/user/self", headers=get_auth_headers(USERNAME, updated_password))

    assert response.status_code == 200
    assert response.json()["first_name"] == "testRenameFirstName"
    assert response.json()["last_name"] == "testRenameLastName"

# Test to handle failure in reading user data with incorrect password after updating
def test_update_read_failure():
    """Test reading user data with incorrect password after updating and validate the response."""
    invalid_password = "IncorrectPassword"
    response = client.get("/v1/user/self", headers=get_auth_headers(USERNAME, invalid_password))

    assert response.status_code == 401

########################################################################################################################################################################
    

