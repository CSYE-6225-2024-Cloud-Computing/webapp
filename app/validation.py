from pydantic import BaseModel, validator, EmailStr, constr, UUID4
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import JSONResponse
import re
import logging
import sys

headers = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0"
}


def validateNames(first_name, last_name):
    if first_name.isalpha() and last_name.isalpha():
        return True
    else:
        JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Name must contain only alphabetic characters"}, headers=headers)
        return False

def validateEmail(username):
    # Regular expression pattern for validating email format
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(email_pattern, username):
        return True
    else:
        return False
    

    from fastapi import status

def validatePassword(password):
    errors = []

    if len(password) < 8 or len(password) > 32:
        errors.append("Password must be between 8 and 32 characters long")
        
    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one uppercase character")
        
    if not any(char.isdigit() for char in password):
        errors.append("Password must contain at least one digit")

    if errors:
        return errors
    else:
        return []

def configure_logging(logger):
    # Set the logging level to INFO
    logger.setLevel(logging.INFO)

    # Define the log message format in JSON format
    formatter = logging.Formatter('{"timestamp": "%(asctime)s","severity": "%(levelname)s",  "message": "%(message)s"}')

    # Configure a StreamHandler to output logs to the console (stdout)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    # Configure a FileHandler to output logs to a file named 'webapp.log'
    file_handler = logging.FileHandler('/var/log/webapp.log')
    # file_handler = logging.FileHandler('./webapp.log')

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)