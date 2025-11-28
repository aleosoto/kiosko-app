class Usuario:
    def __init__(self, id=None, nombre=''):
        self.id = id
        self.nombre = nombre

class Empleado(Usuario):
    def __init__(self, id=None, nombre='', puesto=''):
        super().__init__(id, nombre)
        self.puesto = puesto
