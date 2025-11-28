from app.db_connector import execute_query

class PedidoItem:
    def __init__(self, id=None, pedido_id=None, producto_id=None, cantidad=1, precio_unit=0.0):
        self.id = id
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unit = precio_unit

    def crear(self):
        q = """
            INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio_unit)
            VALUES (%s, %s, %s, %s)
        """
        execute_query(q,
                      (self.pedido_id, self.producto_id, self.cantidad, self.precio_unit),
                      commit=True,
                      return_id=True)
