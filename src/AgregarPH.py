import pandas as pd
import numpy as np


# Cargar datos
class CargaData:
    def __init__(self, file_path):
        try:
            self.df = pd.read_csv(file_path).copy()
        except FileNotFoundError:
            print(f"Error: El archivo {file_path} no existe")
            raise
        except pd.errors.EmptyDataError:
            print(f"Error: El archivo {file_path} está vacío")
            raise
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            raise

    def obtener_data(self):
        try:
            return self.df
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            raise


# Agregar ph del suelo por mes
class AgregarPH:
    def __init__(self, df):
        try:
            self.df = df
        except Exception as e:
            print(f"Error al inicializar AgregarPH: {e}")
            raise

    def generar_ph_mensual(self):
        try:
            # Generar un valor aleatorio de pH entre 3 y 9 por cada mes
            for month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']:
                self.df.loc[:, month + '_PH_SUELO'] = np.round(np.random.uniform(3, 9, size=len(self.df)), 2)
            return self.df
        except Exception as e:
            print(f"Error generando pH mensual: {e}")
            raise