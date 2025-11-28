# app/models/user.py
class Usuario:
    def __init__(self, id=None, nombre=''):
        self.id = id
        self.nombre = nombre

class Cliente(Usuario):
    def __init__(self, id=None, nombre='', telefono=None):
        super().__init__(id, nombre)
        self.telefono = telefono

    def crear_en_bd(self):
        from app.db_connector import execute_query
        q = "INSERT INTO clientes (nombre, telefono) VALUES (%s,%s)"
        execute_query(q, (self.nombre, self.telefono), commit=True)
