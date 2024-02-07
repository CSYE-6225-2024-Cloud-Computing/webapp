from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from pydantic import BaseModel, validator, EmailStr, constr
from .database import Base
from typing import Optional
from datetime import datetime, timedelta
import uuid
from sqlalchemy.dialects.postgresql import UUID
# Define User model
class User(Base):
    __tablename__ = 'user'

    # id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    account_created = Column(DateTime, default=datetime.now)
    account_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)