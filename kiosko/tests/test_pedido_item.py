import unittest
from app.models.pedido_item import PedidoItem

class TestPedidoItem(unittest.TestCase):

    def test_crear_item_sin_pedido(self):
        # debe fallar por FOREIGN KEY
        with self.assertRaises(Exception):
            item = PedidoItem(pedido_id=9999, producto_id=1, cantidad=1, precio_unit=10)
            item.crear()

if __name__ == "__main__":
    unittest.main()
