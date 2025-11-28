import unittest
from app.models.producto import Producto
from app.models.cliente import Cliente
from app.db_connector import execute_query

class TestModels(unittest.TestCase):
    def test_producto_crud(self):
        Producto.crear('UTProducto', 'desc', 9.5, 'Test')
        prods = [p for p in Producto.listar_todos() if p['nombre']=='UTProducto']
        self.assertTrue(len(prods) >= 1)
        pid = prods[0]['id']
        Producto.actualizar(pid, 'UTProducto2', 'desc2', 10.0, 'Test')
        p = Producto.obtener_por_id(pid)
        self.assertEqual(p['nombre'], 'UTProducto2')
        Producto.eliminar(pid)
        self.assertIsNone(Producto.obtener_por_id(pid))

    def test_cliente_crud(self):
        c = Cliente(nombre='UTCliente', telefono='111')
        c.crear()
        res = execute_query('SELECT * FROM clientes WHERE nombre=%s', ('UTCliente',))
        self.assertTrue(len(res) >= 1)
        # cleanup
        execute_query('DELETE FROM clientes WHERE nombre=%s', ('UTCliente',), commit=True)

if __name__ == '__main__':
    unittest.main()
