import psycopg2
from utils.config import DB_URL

def connect_db():
    conn = psycopg2.connect(DB_URL)
    if conn is None:
        print("Conexión no establecida.")
    else:
        print("Conexión establecida.")
    return conn

def close_db(conn):
    conn.close()
    print("Conexión cerrada.")
    