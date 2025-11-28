from app.db_connector import execute_query
from app.models.pedido_item import PedidoItem

class Pedido:
    def __init__(self, id=None, cliente_id=None, fecha=None,
                 total=0.0, estado="Pendiente"):
        self.id = id
        self.cliente_id = cliente_id
        self.fecha = fecha
        self.total = total
        self.estado = estado
        self.items = []

    # --- CREATE BASE ---
    @staticmethod
    def crear_pedido(cliente_id):
        q = "INSERT INTO pedidos (cliente_id) VALUES (%s)"
        execute_query(q, (cliente_id,), commit=True)
        res = execute_query("SELECT LAST_INSERT_ID() as id")
        return res[0]["id"]

    # --- CREATE FROM CART ---
    @staticmethod
    def crear_desde_carrito(cliente_id, items):
        """
        items = lista de productos:
        [
            {'id':1, 'precio':40},
            {'id':3, 'precio':20},
            ...
        ]
        """
        id_pedido = Pedido.crear_pedido(cliente_id)

        total = 0

        for p in items:
            item = PedidoItem(
                pedido_id=id_pedido,
                producto_id=p["id"],
                cantidad=p.get("cantidad", 1),
                precio_unit=p["precio"]
            )
            total += float(p["precio"]) * item.cantidad
            item.crear()

        Pedido.actualizar_total(id_pedido, total)

        return {"id": id_pedido, "total": total}

    # --- UPDATE TOTAL ---
    @staticmethod
    def actualizar_total(pedido_id, total):
        q = "UPDATE pedidos SET total=%s WHERE id=%s"
        execute_query(q, (total, pedido_id), commit=True)

    # --- UPDATE STATUS ---
    @staticmethod
    def cambiar_estado(pedido_id, nuevo_estado):
        q = "UPDATE pedidos SET estado=%s WHERE id=%s"
        execute_query(q, (nuevo_estado, pedido_id), commit=True)

    # --- READ ---
    @staticmethod
    def obtener_por_id(pedido_id):
        q = "SELECT * FROM pedidos WHERE id=%s"
        res = execute_query(q, (pedido_id,))
        return res[0] if res else None

    @staticmethod
    def listar_todos():
        q = "SELECT * FROM pedidos"
        return execute_query(q)

    # --- DELETE ---
    @staticmethod
    def eliminar(pedido_id):
        q = "DELETE FROM pedidos WHERE id=%s"
        execute_query(q, (pedido_id,), commit=True)
