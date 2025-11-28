import unittest
from app.models.cliente import Cliente

class TestCliente(unittest.TestCase):

    def test_crear_cliente(self):
        cliente = Cliente(nombre="Prueba Unittest", telefono="123456")
        nuevo_id = cliente.crear()
        self.assertIsNotNone(nuevo_id)   # verifica que sí lo creó
        self.assertGreater(nuevo_id, 0)

    def test_cliente_inexistente(self):
        cliente = Cliente.obtener_por_id(-1)
        self.assertIsNone(cliente)

if __name__ == "__main__":
    unittest.main()
