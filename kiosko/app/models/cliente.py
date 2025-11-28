from app.db_connector import execute_query

class Cliente:
    def __init__(self, id=None, nombre="", telefono=None, fecha_registro=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono

    def crear(self):
        q = "INSERT INTO clientes (nombre, telefono) VALUES (%s, %s)"
        self.id = execute_query(q, (self.nombre, self.telefono), commit=True, return_id=True)
        return self.id
