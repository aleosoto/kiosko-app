from app.db_connector import execute_query

class Pago:
    def __init__(self, id=None, pedido_id=None, monto=0.0, metodo="Efectivo", estado="Validado"):
        self.id = id
        self.pedido_id = pedido_id
        self.monto = float(monto)
        self.metodo = metodo
        self.estado = estado

    def crear(self):
        q = """
            INSERT INTO pagos (pedido_id, monto, metodo, estado)
            VALUES (%s, %s, %s, %s)
        """
        execute_query(q, (self.pedido_id, self.monto, self.metodo, self.estado), commit=True)

    @staticmethod
    def procesar_pago_simple(pedido_id, monto):
        pago = Pago(pedido_id=pedido_id, monto=monto, metodo="Efectivo", estado="Validado")
        pago.crear()
        return pago
