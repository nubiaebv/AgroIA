"""
Clase: Service_Ann

Objetivo: Clase para control de servicios de ANN

Cambios:

    1. Creacion de clase pmarin 05-07-2025
"""
from src.train.ann import ann
from src.utils.metrics import obtener_ruta_app


class Service_Ann:
    def __init__(self, fila):
        self._ann = ann(obtener_ruta_app("AgroIA"))
        self._fila = fila

    def prediccion(self):
        return self._ann.predecir_desde_fila(self._fila)