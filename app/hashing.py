
from passlib.context import CryptContext
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
