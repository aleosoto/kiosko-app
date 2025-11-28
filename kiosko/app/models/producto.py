from app.db_connector import execute_query

class Producto:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=0.0, categoria=None):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion
        self.precio=precio
        self.categoria=categoria

    @staticmethod
    def listar_todos():
        return execute_query("SELECT * FROM productos")

    @staticmethod
    def obtener_por_id(producto_id):
        res=execute_query("SELECT * FROM productos WHERE id=%s",(producto_id,))
        return res[0] if res else None
