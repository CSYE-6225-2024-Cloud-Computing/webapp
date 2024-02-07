from fastapi.testclient import TestClient
from .main import app
from . import database
import requests
from passlib.context import CryptContext
client = TestClient(app)
import base64
import json

######################################################################################################################################
#REFRESH DATABASE
database.clear_database()
######################################################################################################################################
def test_create_user():
    # Define test data
    user_data = {
        "first_name": "testFirstName",
        "last_name": "testLastName",
        "username": "test_email@example.com",
        "password": "Test@pass01"
    }

    # Send a POST request to create a new user
    response = client.post("/v1/user/", json=user_data)

    # Check if the response status code is 201 Created
    assert response.status_code == 201

    # Check if the response contains the expected user data
    assert response.json()["first_name"] == "testFirstName"
    assert response.json()["last_name"] == "testLastName"
    assert response.json()["username"] == "test_email@example.com"

def test_create_user_failure():
    # Define test data with invalid email address (missing '@' symbol)
    invalid_user_data = {
        "first_name": "testFirstName",
        "last_name": "testLastName",
        "username": "invalid_email_example.com",  # Invalid email format
        "password": "Test@pass01"
    }

    # Send a POST request to create a new user with invalid data
    response = client.post("/v1/user/", json=invalid_user_data)

    # Check if the response status code is 400 Bad Request
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"

######################################################################################################################################

def test_read_main():

    # Assuming you have the plaintext password
    username = "test_email@example.com"
    password = "Test@pass01"
    concatenated_value = f"{username}:{password}"
    payload = {}
    headers = {
            'Authorization': f"Basic {base64.b64encode(bytes(concatenated_value, 'utf-8')).decode('utf-8') }"
            }
    print(f"---headers----- {headers}")
    response = client.get("/v1/user/self", headers=headers)
    # response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 200
    print(f"----response body ---- {response.json()}")


def test_read_main_failure():
    # Assuming you have the plaintext password
    username = "test_email@example.com"
    # Use an incorrect password here
    password = "IncorrectPassword"
    concatenated_value = f"{username}:{password}"
    payload = {}
    headers = {
        'Authorization': f"Basic {base64.b64encode(bytes(concatenated_value, 'utf-8')).decode('utf-8')}"
    }
    response = client.get("/v1/user/self", headers=headers)
    # Assert that the response status code is 401 Unauthorized
    assert response.status_code == 401

######################################################################################################################################

def test_update_first_name():

    # Assuming you have the plaintext password
    username = "test_email@example.com"
    password = "Test@pass01"
    concatenated_value = f"{username}:{password}"
    payload = json.dumps({
        "first_name": "testRenameFirstName",
        "last_name": "testLastName",
        "password": "Test@pass01"
        })
    headers = {
            'Authorization': f"Basic {base64.b64encode(bytes(concatenated_value, 'utf-8')).decode('utf-8') }"
            }
    print(f"---headers----- {headers}")
    response = client.put("/v1/user/self", headers=headers, data=payload)
    # response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 204
    print(f"----response body ---- {response.json()}")


def test_update_password():
    # Assuming you have the plaintext password
    username = "test_email@example.com"
    password = "Test@pass01"
    concatenated_value = f"{username}:{password}"
    payload = json.dumps({
        "first_name": "testRenameFirstName",
        "last_name": "testLastName",
        "password": "TestRename@pass01"
        })
    headers = {
            'Authorization': f"Basic {base64.b64encode(bytes(concatenated_value, 'utf-8')).decode('utf-8') }"
            }
    print(f"---headers----- {headers}")
    response = client.put("/v1/user/self", headers=headers, data=payload)
    # response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 204
    print(f"----response body ---- {response.json()}")

def test_update_read_pass():

    # Assuming you have the plaintext password
    username = "test_email@example.com"
    password = "TestRename@pass01"
    concatenated_value = f"{username}:{password}"
    payload = {}
    headers = {
            'Authorization': f"Basic {base64.b64encode(bytes(concatenated_value, 'utf-8')).decode('utf-8') }"
            }
    print(f"---headers----- {headers}")
    response = client.get("/v1/user/self", headers=headers)
    # response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 200
    print(f"----response body ---- {response.json()}")

def test_update_read_failure():
    # Assuming you have the plaintext password
    username = "test_email@example.com"
    # Use an incorrect password here
    password = "IncorrectPassword"
    concatenated_value = f"{username}:{password}"
    payload = {}
    headers = {
        'Authorization': f"Basic {base64.b64encode(bytes(concatenated_value, 'utf-8')).decode('utf-8')}"
    }
    response = client.get("/v1/user/self", headers=headers)
    # Assert that the response status code is 401 Unauthorized
    assert response.status_code == 401


######################################################################################################################################








