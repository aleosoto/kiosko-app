# app/db_connector.py

import mysql.connector
from mysql.connector import Error
from app.config import config

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            port=config["port"]
        )
        return conn
    except Error as e:
        print(" ERROR DE CONEXIÓN:", e)
        return None


def execute_query(query, params=None, commit=False):
    conn = get_connection()
    if conn is None:
        print(" No se pudo conectar a la base de datos.")
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if commit:
            conn.commit()

        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()

        return []

    except Error as e:
        print(" DB Error:", e)
        return []

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
