"""
Clase: Service_Rnn

Objetivo: Clase para control de servicios de RNN

Cambios:

    1. Creacion de clase pmarin 05-07-2025
"""
from src.train.rnn import rnn
from src.utils.metrics import obtener_ruta_app

class Service_Rnn:
    def __init__(self):
        self._rnn = rnn(obtener_ruta_app("AgroIA"))
    def prediccion(self, df):
        return self._rnn.obtener_prediccion_api(df)