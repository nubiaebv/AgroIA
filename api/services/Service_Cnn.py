"""
Clase: Service_Cnn

Objetivo: Clase para control de servicios de CNN

Cambios:

    1. Creacion de clase pmarin 05-07-2025
"""
from src.train.cnn import cnn
from src.utils.metrics import obtener_ruta_app
class Service_Cnn:
    def __init__(self, imagen):
        self.imagen = imagen
        self._cnn = cnn(obtener_ruta_app("AgroIA"))

    def prediccion(self):
        return self._cnn.predeccir_imagen_api(self.imagen)