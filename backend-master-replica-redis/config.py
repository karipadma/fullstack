import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # DB
    DB_MASTER_HOST = os.getenv("DB_MASTER_HOST")
    DB_REPLICA_HOST = os.getenv("DB_REPLICA_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    # REDIS
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))