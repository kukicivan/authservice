import os
from pathlib import Path

import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from dotenv import load_dotenv

# Reads the key-value pair from .env file
# and adds them to environment variable
from sqlalchemy.orm import sessionmaker

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

# Prints environment that is loaded
print("INFO:     " + os.getenv("INFO") + " loaded")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

database = databases.Database(SQLALCHEMY_DATABASE_URL)

Base: DeclarativeMeta = declarative_base()

# Create Dependency used in crud routes
# New SQLAlchemy SessionLocal that will be used in a single
# request, and then closed once the request is finished
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
