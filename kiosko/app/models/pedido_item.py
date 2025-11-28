from app.db_connector import execute_query

class PedidoItem:
    def __init__(self, id=None, pedido_id=None, producto_id=None,
                 cantidad=1, precio_unit=0.0):
        self.id = id
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unit = precio_unit

    # --- CREATE ---
    def crear(self):
        q = """
        INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio_unit)
        VALUES (%s, %s, %s, %s)
        """
        execute_query(q,
                      (self.pedido_id, self.producto_id,
                       self.cantidad, self.precio_unit),
                      commit=True)

    # --- READ ---
    @staticmethod
    def listar_por_pedido(pedido_id):
        q = "SELECT * FROM pedido_items WHERE pedido_id=%s"
        return execute_query(q, (pedido_id,))

    # --- DELETE ---
    @staticmethod
    def eliminar(id_item):
        q = "DELETE FROM pedido_items WHERE id=%s"
        execute_query(q, (id_item,), commit=True)
