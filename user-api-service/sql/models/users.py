from sqlalchemy import Column, Integer, String
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(String(255), default=datetime.now(), nullable=False)
    updated_at = Column(String(255), nullable=False, onupdate=datetime.now())
