from dotenv import load_dotenv
from fastapi import Path

# Reads the key-value pair from .env file
# and adds them to environment variable
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)
