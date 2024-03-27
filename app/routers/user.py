from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from .. import schemas, database, models, hashing, oauth2, validation
from typing import List
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
import json
from pydantic import ValidationError
import logging, sys
from pythonjsonlogger import jsonlogger
from datetime import datetime, timedelta
from google.cloud import pubsub_v1
import os

# Get the root logger instance
logger = logging.getLogger()
# validation.configure_logging(logger)



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

        ## Add pubsub message
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(
                                            os.getenv('GCP_PROJECT_ID', ''), 
                                            os.getenv('PUBSUB_TOPIC_NAME', 'verify_email')
                                        )
        message_bytes = new_user.encode("utf-8")
        future = publisher.publish(topic_path, data=message_bytes)
        return new_user

    except Exception as e:
        # Log the error
        logger.error("An error occurred while processing the request", exc_info=True)
        # Log the error if needed
        #print("Error:", str(e))
        # Raise a generic 400 Bad Request error
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Bad Request"},headers=headers)



@router.get('/verify_email', status_code=status.HTTP_200_OK, response_description="User verification", response_model=schemas.showUser)
async def verify_email(token_id: str, request: Request, db: Session = Depends(database.get_db)):
    try:
        # Assuming you have a User model with a field 'account_created' representing the account creation timestamp
        logs = db.query(models.Logs).filter(models.Logs.token_id == token_id).first()

        if not logs:
            error_message = "Token ID not found"
            logger.error(error_message)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)

        # Calculate the time difference between current time and account creation time
        if datetime.now() <= logs.expires_timestamp:
            user = db.query(models.User).filter(models.User.username == logs.username).first()
            user.is_verified = True
            db.commit()

            success_message = f"Email verification successful for user {user.username}"
            logger.info(success_message)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": success_message})

        
            # If the verification is successful, return the user details
            #return user

        else:
            error_message = "Account creation time exceeded 2 minutes"
            logger.error(error_message)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

    except Exception as e:
        error_message = f"An error occurred during email verification: {e}"
        logger.error(error_message)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": error_message})



# @router.get('/verify_email', status_code=status.HTTP_201_CREATED, response_description="User created", response_model=schemas.showUser)
# async def verify_email(token_id: str, request: Request, db: Session = Depends(database.get_db)):
#     # Assuming you have a User model with a field 'account_created' representing the account creation timestamp
#     logs = db.query(models.Logs).filter(models.Logs.token_id == token_id).first()
    
#     if not logs:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
#     # Calculate the time difference between current time and account creation time
#     if (datetime.now <= logs.expires_timestamp):
#         user = db.query(models.User).filter(models.User.username == logs.username).first()
#         user.is_verified == True
#         db.commit()

#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account creation time exceeded 2 minutes")

#     return user
    

# @router.get('/resend_email', status_code=status.HTTP_201_CREATED, response_description="User created", response_model=schemas.showUser)
# async def resend_email(user_email: str, request: Request, db: Session = Depends(database.get_db)):
#     # Assuming you have a User model with a field 'account_created' representing the account creation timestamp
#     user = db.query(models.User).filter(models.User.username == user_email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
#     # Update the account_created field with the current timestamp
#     user.account_created = datetime.now()
#     db.commit()
    
#     # If the update is successful, return the user details
#     return user

    