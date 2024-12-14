# webapp
<hr>

* This repository contains code for building and deploying a FastAPI-based backend web application

* It further  provides important information on prerequisites for building and deploying the application locally, as well as instructions for building and deploying the web application.

<hr>

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Build and Deploy Instructions](#build-and-deploy-instructions)

<hr>

## Prerequisites
## testing -pr
Before you begin building and deploying the FastAPI web application locally, ensure you have the following prerequisites:

- **Python Environment**: Python 3.x installed on your local machine.
- **FastAPI, SQLAlchemy, and Postgres**: Install FastAPI, SQLAlchemy, and necessary dependencies using pip:
- **PostgreSQL Database**: Install and set up a PostgreSQL database locally.
- **BCrypt**: Install the bcrypt library via pip:
- **note**: requirements.txt file contains all necessary dependencies
```bash
pip install -r requirements.txt
```
- **Basic Authentication Token**: Generate a basic authentication token for accessing authenticated endpoints.
- **Swagger Documentation**: Ensure annotations and comments are present in the code for generating Swagger documentation.
- **Unit and Integration Tests**: Implement unit and integration tests using libraries like pytest.
- **GitHub Actions**: Set up a GitHub Actions workflow for Continuous Integration.
- **Token-Based Authentication**: Implement Token-Based authentication for the web application.
- **Database Bootstrapping**: Implement logic for bootstrapping the database at application startup.
- **JSON Payloads**: Ensure all API request and response payloads are in JSON format.
- **Proper HTTP Status Codes**: Ensure API calls return appropriate HTTP status codes.
- **GitHub Branch Protection and Status Checks**: Configure GitHub branch protection and status checks for pull requests.

## Build and Deploy Instructions

To build and deploy the FastAPI web application locally, follow these instructions:

1. **Clone the Repository**: Clone the repository to your local machine:
```bash
git clone git@github.com:ShreyaJaiswal1604/webapp.git
```

2. **Set Up Environment Variables**: Set up environment variables for database connection and other configurations, if necessary.
```bash
python3 -m venv env

source env/bin/activate
```

3. **Run the Application**: Run the FastAPI application using uvicorn or your preferred ASGI server:
```bash
uvicorn main:app --reload
```

4. **Access the API**: Access the API endpoints in your browser or through tools like curl or Postman.

5. **Testing**: Run unit and integration tests to ensure the application functions correctly:


6. **Continuous Integration**: Ensure that your pull requests pass the GitHub Actions workflow before merging.

7. **Deployment**: Follow your deployment strategy to deploy the application to your production environment.

<hr>