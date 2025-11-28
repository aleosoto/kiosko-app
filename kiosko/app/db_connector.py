import mysql.connector
from mysql.connector import Error
from app.config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def execute_query(query, params=None, commit=False):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        if commit:
            conn.commit()
        try:
            return cur.fetchall()
        except:
            return []
    except Exception as e:
        # simple logging to console; replace with logging if needed
        print('DB Error:', e)
        raise
    finally:
        if conn:
            cur.close()
            conn.close()
