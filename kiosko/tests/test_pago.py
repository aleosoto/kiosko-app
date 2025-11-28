import unittest
from app.models.pago import Pago

class TestPago(unittest.TestCase):

    def test_pago_invalido(self):
        # un pedido inexistente debe generar error
        try:
            Pago.procesar_pago_simple(9999, 50)
            resultado = False
        except:
            resultado = True

        self.assertTrue(resultado)

if __name__ == "__main__":
    unittest.main()
