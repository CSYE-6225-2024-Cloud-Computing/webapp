from pydantic import BaseModel, validator, EmailStr, constr, UUID4
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import JSONResponse
import re

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
