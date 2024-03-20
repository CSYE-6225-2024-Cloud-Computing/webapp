
from passlib.context import CryptContext
import logging
import sys
from pythonjsonlogger import jsonlogger
from . import validation


# Get the root logger instance
logger = logging.getLogger()
validation.configure_logging(logger)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        logger.info("Password hashed successfully")
        return pwd_cxt.hash(password)
    
    # def verify(hashed_password, plain_password):
    #     return pwd_cxt.verify(plain_password,hashed_password)

    def verify(hashed_password, plain_password):
        is_verified = pwd_cxt.verify(plain_password, hashed_password)
        if is_verified:
            logger.info("Password verification successful")
        else:
            logger.warning("Password verification failed")
        return is_verified
