import unittest
from app.models.pedido import Pedido
from app.models.cliente import Cliente

class TestPedido(unittest.TestCase):

    def test_crear_pedido(self):
        cliente = Cliente(nombre="TestPedido")
        cliente_id = cliente.crear()

        pedido = Pedido.crear_desde_carrito(
            cliente_id,
            [{"id": 1, "precio": 10, "cantidad": 2}]
        )

        self.assertIsNotNone(pedido['id'])
        self.assertGreater(pedido['total'], 0)

if __name__ == "__main__":
    unittest.main()
