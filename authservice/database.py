import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from databases import Database

import config

# Load .env
env_path = Path('.') / config.ENVIRONMENT
load_dotenv(dotenv_path=env_path, verbose=True)

# Get db URI from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# database = create_engine(SQLALCHEMY_DATABASE_URL)
SqlAlchemyEngine = create_engine(SQLALCHEMY_DATABASE_URL)

# SQLAlchemy session used in a single request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=SqlAlchemyEngine)

# Database session used in a single request
database = Database(SQLALCHEMY_DATABASE_URL)


def get_db():
    return database
