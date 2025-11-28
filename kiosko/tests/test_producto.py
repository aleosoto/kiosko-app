import unittest
from app.models.producto import Producto

class TestProducto(unittest.TestCase):

    def test_listar_productos(self):
        lista = Producto.listar_todos()
        self.assertIsInstance(lista, list)

    def test_producto_inexistente(self):
        p = Producto.obtener_por_id(-1)
        self.assertIsNone(p)

if __name__ == "__main__":
    unittest.main()
