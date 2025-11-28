import mysql.connector
from mysql.connector import Error
from app.config import DB_CONFIG

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"]
        )
        return conn
    except Error as e:
        print("ERROR DE CONEXIÓN:", e)
        return None

def execute_query(query, params=None, commit=False, return_id=False):
    conn = get_connection()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return None if return_id else []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if commit:
            conn.commit()

        # devolver ID correcto
        if return_id:
            return cursor.lastrowid

        # devolver SELECT
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()

        return []

    except Error as e:
        print("DB Error:", e)
        return None if return_id else []

    finally:
        cursor.close()
        conn.close()
