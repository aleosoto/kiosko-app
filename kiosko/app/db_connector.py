# app/db_connector.py
import mysql.connector
from mysql.connector import Error
from app.config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def execute_query(query, params=None, commit=False):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        if commit:
            conn.commit()
        try:
            return cur.fetchall()
        except:
            return []
    finally:
        cur.close()
        conn.close()
