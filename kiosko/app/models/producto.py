# app/models/producto.py
from app.db_connector import execute_query

class Producto:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=0.0, categoria=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria

    @staticmethod
    def crear(nombre, descripcion, precio, categoria):
        q = "INSERT INTO productos (nombre, descripcion, precio, categoria) VALUES (%s,%s,%s,%s)"
        execute_query(q, (nombre, descripcion, precio, categoria), commit=True)

    @staticmethod
    def listar_todos():
        q = "SELECT * FROM productos"
        return execute_query(q)

    @staticmethod
    def obtener_por_id(producto_id):
        q = "SELECT * FROM productos WHERE id=%s"
        res = execute_query(q, (producto_id,))
        return res[0] if res else None

    @staticmethod
    def actualizar(producto_id, nombre, descripcion, precio, categoria):
        q = "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, categoria=%s WHERE id=%s"
        execute_query(q, (nombre, descripcion, precio, categoria, producto_id), commit=True)

    @staticmethod
    def eliminar(producto_id):
        q = "DELETE FROM productos WHERE id=%s"
        execute_query(q, (producto_id,), commit=True)
