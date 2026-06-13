import pymysql
from config import Config

# ---------------- MASTER DB ----------------
def get_master_conn():
    return pymysql.connect(
        host=Config.DB_MASTER_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# ---------------- REPLICA DB ----------------
def get_replica_conn():
    return pymysql.connect(
        host=Config.DB_REPLICA_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )