from dotenv import load_dotenv
import os

from passlib.context import CryptContext

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_NAME = os.getenv("DB_NAME", "my_db")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
