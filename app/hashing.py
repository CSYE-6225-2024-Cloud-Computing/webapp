
from passlib.context import CryptContext
import logging
from pythonjsonlogger import jsonlogger

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create JSON handler with log file path
log_file_path = '/var/log/webapp.log'  # Specify the log file path here
logHandler = logging.FileHandler(log_file_path)
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

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
