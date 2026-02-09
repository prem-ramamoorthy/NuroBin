from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "nurobin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mysecretpassword")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
