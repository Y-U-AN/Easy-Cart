import pymysql.cursors

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "472500",
    "db": "shop",
    "charset": 'utf8mb4',
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db_connection():
    connection = pymysql.connect(**DB_CONFIG)
    return connection
