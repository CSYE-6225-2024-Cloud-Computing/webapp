from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from .. import schemas, database, models, hashing, oauth2, validation
from typing import List
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
import json
from pydantic import ValidationError


headers = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0"
}



router = APIRouter(
    prefix ="/v1/user",
    tags = ['user']
)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

#CRED - CREATE USER
#request: schemas.userCreate ,db: Session = Depends(database.get_db)
@router.post('/',status_code=status.HTTP_201_CREATED, response_description="User created",response_model=schemas.showUser)
async def create_user(request:Request,db: Session = Depends(database.get_db)):
    try:
        # Parse the request body
        data = await request.json()

        # Check if the prefix matches
        if not request.url.path.startswith('/v1/user'):
            print("not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Endpoint not found"}, headers=headers)

        # Check if all required parameters are present
        required_params = ["first_name", "last_name", "username", "password"]
        for param in required_params:
            if param not in data:
                error_message = {"detail": f"Parameter {param} is missing"}
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message, headers=headers)
        
        # Validate user data
        print("validate pleaseee")
        
        if not validation.validateEmail(data["username"]):
            error_message = {"detail": f"Invalid email format"}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content=error_message,headers=headers)
        
        if not validation.validateNames(data["first_name"],data["last_name"]):
            error_message = {"detail": "Name must contain only alphabetic characters"}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message, headers=headers)
        
        errors = validation.validatePassword(data["password"])
        print(errors)
        if len(errors)!=0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": errors}, headers=headers)

        # Check if the username already exists
        print("checking existing user")    
        existing_user = db.query(models.User).filter(models.User.username == data["username"]).first()
        if existing_user:
            print("entered existing user")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Email address already exists"},headers=headers)

        # Create a new user
        new_user = models.User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            password=hashing.Hash.bcrypt(data["password"]))

        # Add new user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except Exception as e:
        # Log the error if needed
        print("Error:", str(e))
        # Raise a generic 400 Bad Request error
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Bad Request"},headers=headers)



    # try:
    #     print("---inside CREATE USER=========")
    #     #user_data = request.dict()
    #     print(request.json())
    #     print("---inside CREATE USER=========")
    #     #schemas.userCreate(**user_data)

    # except schemas.ValidationError as e:
    #     # Construct a detailed error message for logging purposes
    #     error_details = [{'type': error.type, 'loc': error.loc, 'msg': error.msg, 'input': error.input} for error in e.errors()]
    #     # Log the error details if needed
    #     print("Validation errors:", error_details)
    #     # Return a 400 Bad Request with the error details
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


    # existing_user = db.query(models.User).filter(models.User.username == request.username).first()
    # if existing_user:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f"email address already exists")

    # #hashedPassword = pwd_cxt.hash(request.password)
    # new_user = models.User(
    #     first_name=request.first_name,
    #     last_name=request.last_name,
    #     username=request.username,
    #     password=hashing.Hash.bcrypt(request.password))
    
    # #add new user
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)

    # return new_user

  

