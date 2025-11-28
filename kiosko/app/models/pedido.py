from app.db_connector import execute_query
from app.models.pedido_item import PedidoItem

class Pedido:

    @staticmethod
    def crear_pedido(cliente_id):
        q = "INSERT INTO pedidos (cliente_id) VALUES (%s)"
        return execute_query(q, (cliente_id,), commit=True, return_id=True)

    @staticmethod
    def crear_desde_carrito(cliente_id, items):
        # crea el pedido y obtiene ID real
        id_pedido = Pedido.crear_pedido(cliente_id)

        total = 0
        for p in items:
            cantidad = p.get("cantidad", 1)
            precio = float(p["precio"])
            total += precio * cantidad

            item = PedidoItem(
                pedido_id=id_pedido,
                producto_id=p["id"],
                cantidad=cantidad,
                precio_unit=precio
            )
            item.crear()

        Pedido.actualizar_total(id_pedido, total)

        return {"id": id_pedido, "total": total}

    @staticmethod
    def actualizar_total(pedido_id, total):
        q = "UPDATE pedidos SET total=%s WHERE id=%s"
        execute_query(q, (total, pedido_id), commit=True)

    @staticmethod
    def listar_todos():
        return execute_query("SELECT * FROM pedidos")
