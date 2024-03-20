from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from .. import schemas, database, models, hashing, oauth2, validation
from typing import List
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
import json
from pydantic import ValidationError
import logging
from pythonjsonlogger import jsonlogger


# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create file handler
log_file_path = './webapp.log'  # File path from config.yaml
file_handler = logging.FileHandler(log_file_path)
formatter = jsonlogger.JsonFormatter('(asctime) (levelname) (message) (filename) (lineno)')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Add custom log attribute
file_handler.addFilter(lambda record: setattr(record, 'log_name', 'my_logs_app'))

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

        # Log the incoming request data
        logger.info("Received request to create user", extra={"request_data": data})


        # Check if the prefix matches
        if not request.url.path.startswith('/v1/user'):
            logger.warning("Endpoint not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Endpoint not found"}, headers=headers)

        # Check if all required parameters are present
        required_params = ["first_name", "last_name", "username", "password"]
        for param in required_params:
            if param not in data:
                error_message = {"detail": f"Parameter {param} is missing"}
                logger.error(error_message)
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message, headers=headers)
            
        # Check if there are any extra parameters in the request
        allowed_params = set(required_params)
        request_params = set(data.keys())
        if not request_params.issubset(allowed_params):
            extra_params = request_params - allowed_params
            error_message = {"detail": f"Extra parameters in request: {', '.join([f'{param}' for param in extra_params])} not allowed"}
            logger.error(error_message)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message)

        
        # Validate user data
        print("validate pleaseee")
        
        if not validation.validateEmail(data["username"]):
            error_message = {"detail": f"Invalid email format"}
            logger.error(error_message)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content=error_message,headers=headers)
        
        if not validation.validateNames(data["first_name"],data["last_name"]):
            error_message = {"detail": "Name must contain only alphabetic characters"}
            logger.error(error_message)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message, headers=headers)
        
        errors = validation.validatePassword(data["password"])
        if len(errors)!=0:
            logger.error(errors)
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

        logger.info("User created successfully")
        return new_user

    except Exception as e:
        # Log the error
        logger.error("An error occurred while processing the request", exc_info=True)
        # Log the error if needed
        #print("Error:", str(e))
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

  

