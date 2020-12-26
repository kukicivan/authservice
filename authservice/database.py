import os
from pathlib import Path

import databases
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Reads the key-value pair from .env file
from sqlalchemy.orm import sessionmaker

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy session used in a single request
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
