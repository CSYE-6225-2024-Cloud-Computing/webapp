from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from .. import schemas, database, models, hashing, validation
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from datetime import datetime
from fastapi.responses import JSONResponse

security = HTTPBasic()

# Create headers with "no-cache" directive
headers = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0"
}

router = APIRouter(
    prefix="/v1/user",
    tags=['authenticated']
)

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user or not hashing.Hash.verify(user.password, credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

# GET - Retrieve user information
@router.get('/self', status_code=status.HTTP_200_OK, response_model=schemas.showUser)
def get_user_info(user: schemas.User = Depends(verify_credentials)):
    return user

# PUT - Update user information
@router.put('/self', status_code=status.HTTP_204_NO_CONTENT)
async def update_user_info(request: Request, user: schemas.User = Depends(verify_credentials), db: Session = Depends(database.get_db)):
    allowed_fields = {'first_name', 'last_name', 'password'}
    fields_to_update = await request.json()

    # Check if the prefix matches
    if not request.url.path.startswith('/v1/user/self'):
        print("not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Endpoint not found"}, headers=headers)


    # Validate if the provided fields are allowed
    if not set(fields_to_update.keys()).issubset(allowed_fields):
        error_message = {"detail": "Only first_name, last_name, and password can be updated"}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message,headers=headers)
    
    if not validation.validateNames(fields_to_update["first_name"],fields_to_update["last_name"]):
        error_message = {"detail": "Name must contain only alphabetic characters"}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message, headers=headers)

    errors = validation.validatePassword(fields_to_update["password"])
    if len(errors)!=0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": errors}, headers=headers)

    # Update fields
    for field, value in fields_to_update.items():
        if field == 'password':
            setattr(user, field, hashing.Hash.bcrypt(value))
        else:
            setattr(user, field, value)

    # Commit changes to the database
    db.commit()
    db.refresh(user)
    

   # Return JSONResponse with headers and no content
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, headers=headers, content=None)





# @router.put('/self', status_code=status.HTTP_202_ACCEPTED,response_model=schemas.showUser)
# def update_user_info(request: Request, user: schemas.User = Depends(verify_credentials), db: Session = Depends(database.get_db)):
#     print("===================PUT TRIGGERED==============================")
#     allowed_fields = {'first_name', 'last_name', 'password'}
#     fields_to_update = request.dict(exclude_unset=True)  # Only include fields that are set in the request
    
#     # Custom validation to ensure all required fields are present
#     if not (request.first_name and request.last_name and request.password):
#         error_message = {"detail": "All fields (first_name, last_name, password) are required."}
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message)

#     # Check if there are any fields other than allowed_fields
  
#     if set(fields_to_update.keys()) != allowed_fields:
#         error_message = {"detail": "Only First_name, Last_name and password can be updated"}
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message)


#     # Update fields
#     for field, value in fields_to_update.items():
#         if field == 'password':
#             setattr(user, field, hashing.Hash.bcrypt(value))
#         else:
#             setattr(user, field, value)

#     # Update account_updated field
#     #user.account_updated = datetime.utcnow()

#     db.commit()
#     db.refresh(user)

#     return user










# from fastapi import APIRouter, Depends,HTTPException, status
# import schemas, database, models, JWTtoken
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from sqlalchemy.orm import Session
# from hashing import Hash
# import oauth2, hashing

# security = HTTPBasic()

# router = APIRouter(
#     prefix ="/v1/user",
#     tags=['authenticated']
# )

# #FUNCTION - HTTPBasicCredentials
# def verification(creds: HTTPBasicCredentials = Depends(security), db: Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.username == creds.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                              detail=f"Invalid username")
    
#     elif not Hash.verify(user.password, creds.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                              detail=f"Incorrect password")
    
#     else:
#         print("=================================================================================================")
#         print(f"User is authenticated")
#         print("=================================================================================================")
#         return user

    

# #CRED - READ USER
# @router.get('/self',status_code=status.HTTP_200_OK,response_model=schemas.showUser)
# def get_user(Verification =  Depends(verification), db: Session = Depends(database.get_db)):
#     if Verification:
#         return Verification
    
# #CRED - UPDATE
# @router.put('/self', status_code=status.HTTP_202_ACCEPTED)
# def update(request: schemas.updateUser , Verification =  Depends(verification), db: Session = Depends(database.get_db) ):
#     if Verification:
#         username = Verification.username
#         print("=================================================================================================")
#         print(f"username: {username}")
#         password = request.password
#         print(f"password: {password}")
#         user = db.query(models.User).filter(models.User.username == username).first()
#         print("=================================================================================================")
#         print(user)
#         print("=================================================================================================")
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#         hashpassword = hashing.Hash.bcrypt(request.password)
#         #Update user attributes
#         user.first_name = request.first_name
#         user.last_name = request.last_name
#         user.password = hashpassword
#         #user.update(request.dict())
#         db.commit()
#         db.refresh(user)

#         return user
    

# # #UPDATE
# # @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
# # def update(id, request: schemas.Blog, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
# #     blog = db.query(models.Blog).filter(models.Blog.id == id)
# #     if not blog.first():
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")
# #     blog.update(request.dict())
# #     db.commit()

# #     return 'updated'



 