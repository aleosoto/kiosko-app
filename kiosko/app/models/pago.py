# app/models/pago.py
from app.db_connector import execute_query

class Pago:
    def __init__(self, id=None, pedido_id=None, monto=0.0,
                 metodo="Efectivo", estado="Validado", fecha=None):
        self.id = id
        self.pedido_id = pedido_id
        self.monto = monto
        self.metodo = metodo
        self.estado = estado
        self.fecha = fecha

    # --- CREATE ---
    @staticmethod
    def procesar_pago(pedido_id, monto, metodo="Efectivo"):
        q = """
        INSERT INTO pagos (pedido_id, monto, metodo, estado)
        VALUES (%s, %s, %s, 'Validado')
        """
        execute_query(q, (pedido_id, monto, metodo), commit=True)

        # actualizar pedido como listo para preparación
        from app.models.pedido import Pedido
        Pedido.cambiar_estado(pedido_id, "En preparación")

    # --- SIMPLE PAYMENT FROM GUI ---
    @staticmethod
    def procesar_pago_simple(pedido_id, monto):
        Pago.procesar_pago(pedido_id, monto, metodo="Efectivo")

    # --- READ ---
    @staticmethod
    def listar_por_pedido(pedido_id):
        q = "SELECT * FROM pagos WHERE pedido_id=%s"
        return execute_query(q, (pedido_id,))

    @staticmethod
    def obtener_por_id(id_pago):
        q = "SELECT * FROM pagos WHERE id=%s"
        res = execute_query(q, (id_pago,))
        return res[0] if res else None
