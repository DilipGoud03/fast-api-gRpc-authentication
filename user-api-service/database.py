from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from decouple import config
import os


SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    config("DB_CONNECTION", default="mysql+mysqldb"),
    config("DB_USERNAME", default="root"),
    config("DB_PASSWORD", default="root"),
    config("DB_HOST", default="localhost"),
    config("DB_PORT", default="3306"),
    config("DB_DATABASE", default="python_with_angular"),
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    pool_pre_ping=True,
    isolation_level="READ COMMITTED",
)

SessionLocal = sessionmaker(bind=engine)
SessionLocal = scoped_session(SessionLocal)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
        engine.dispose()
