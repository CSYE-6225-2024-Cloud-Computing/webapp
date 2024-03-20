import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Request, Response, HTTPException
from pythonjsonlogger import jsonlogger


# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create file handler
log_file_path = './webapp.log'  # File path from config.yaml
file_handler = logging.FileHandler(log_file_path)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s %(filename)s %(lineno)d')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Add custom log attribute
file_handler.addFilter(lambda record: setattr(record, 'log_name', 'my_logs_app'))




# Declare database engine
def create_database_engine():
    database_url = os.getenv('POSTGRES_DATABASE_URL', '')
    if database_url:
        try:
            engine = create_engine(database_url)
            # Test the connection
            engine.connect()
            print("\n=====================================================================")
            logger.info(f"POSTGRES DB Connected Successfuly")
            print("\n=====================================================================")

            return engine

        except Exception as e:
            #return Response(status_code=503)
            print("\n=====================================================================")
            logger.error("Error connecting to the PostgreSQL database:")
            print("\n=====================================================================")
            #raise e
    else:
        print("\n=====================================================================")
        logger.error(f"Cannot find Connection to Postgres Database")
        print("\n=====================================================================")
        sys.exit()

# Additional log for database connection setup completion
logger.info("Database connection setup completed successfully")

        # SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
        # try:
        #     engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
        #     print("\n=====================================================================")
        #     print(f"SQLITE DB Connected Successfuly")
        #     print("\n=====================================================================")
        #     return engine

        # except Exception as e:
        #     print("\n=====================================================================")
        #     print("Error connecting to the SQLITE database:")
        #     print("\n=====================================================================")



engine = create_database_engine()

#declare sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#declare mapping
Base = declarative_base()

def get_db():
    try:
        db = SessionLocal() #initializes a database session
        yield db
    finally:
        db.close()

# Create a function to clear the database
def clear_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# if os.getenv('POSTGRES_DATABASE_URL'):
#     engine = create_engine(os.getenv('POSTGRES_DATABASE_URL'))
# else:
#     SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#     engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

