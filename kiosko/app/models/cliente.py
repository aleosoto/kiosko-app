# app/models/cliente.py
from app.db_connector import execute_query

class Cliente:
    def __init__(self, id=None, nombre="", telefono=None, fecha_registro=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.fecha_registro = fecha_registro

    # --- CREATE ---
    def crear(self):
        q = """
        INSERT INTO clientes (nombre, telefono)
        VALUES (%s, %s)
        """
        execute_query(q, (self.nombre, self.telefono), commit=True)

    # --- READ ---
    @staticmethod
    def obtener_por_id(cliente_id):
        q = "SELECT * FROM clientes WHERE id = %s"
        res = execute_query(q, (cliente_id,))
        return res[0] if res else None

    @staticmethod
    def listar_todos():
        q = "SELECT * FROM clientes"
        return execute_query(q)

    # --- UPDATE ---
    @staticmethod
    def actualizar(cliente_id, nombre, telefono):
        q = """
        UPDATE clientes 
        SET nombre=%s, telefono=%s
        WHERE id=%s
        """
        execute_query(q, (nombre, telefono, cliente_id), commit=True)

    # --- DELETE ---
    @staticmethod
    def eliminar(cliente_id):
        q = "DELETE FROM clientes WHERE id=%s"
        execute_query(q, (cliente_id,), commit=True)
