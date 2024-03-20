from fastapi import FastAPI, Response, Request
import logging
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv
load_dotenv()

from . import models
import os
from .database import engine
from .routers import user, authenticated, healthz


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

#testing-01
models.Base.metadata.create_all(engine)
logger.info("Database created successfully")
#print("Database created successfully")

app = FastAPI()

print("============================== ROUTER: user.py================================")
logger.info("Including user router")
app.include_router(user.router)


print("============================== ROUTER: authenticated.py================================")
app.include_router(authenticated.router)


print("============================== ROUTER: healthz.py================================")
logger.info("Including healthz router")
app.include_router(healthz.router)



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)








