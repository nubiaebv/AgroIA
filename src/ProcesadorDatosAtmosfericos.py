"""
Clase: Clase para limpiar y transformar datos atmosféricos.
Procesa múltiples archivos CSV con datos climatológicos por cantón.
Cambios: 1. Creacion de la clase @fabarca
        2. Optimizacion de codigo para eliminar la creacion de csv como parametro de salida y cambios de nombres
        a los metodos.
"""

import pandas as pd
import os
from typing import List, Optional
import logging


class ProcesadorDatosAtmosfericos:
    """
    Procesa datos atmosféricos desde múltiples archivos CSV.
    """

    def __init__(self, carpeta: str):
        """
        Inicializa el procesador con las rutas de carpetas.

        Args:
            carpeta (str): Carpeta con archivos CSV de datos atmosféricos
            carpeta_salida (str): Carpeta donde guardar resultados

        Raises:
            NotADirectoryError: Si la carpeta no existe
        """
        if not os.path.exists(carpeta):
            raise NotADirectoryError(f"La carpeta {carpeta} no existe")

        if not os.path.isdir(carpeta):
            raise NotADirectoryError(f"{carpeta} no es una carpeta válida")

        self.carpeta = carpeta
        self.logger = logging.getLogger(__name__)

    def leer_archivo(self, ruta: str, canton: str) -> Optional[pd.DataFrame]:
        """
        Lee y procesa un archivo CSV individual.

        Args:
            ruta (str): Ruta del archivo CSV
            canton (str): Nombre del cantón

        Returns:
            pd.DataFrame: DataFrame procesado o None si hay error
        """
        try:
            # Leer archivo buscando el encabezado correcto
            with open(ruta, 'r', encoding='utf-8') as f:
                lineas = f.readlines()

            # Encontrar dónde empieza la tabla de datos
            indice_inicio = None
            for i, linea in enumerate(lineas):
                if linea.strip().startswith("PARAMETER,YEAR"):
                    indice_inicio = i
                    break

            if indice_inicio is None:
                self.logger.warning(f"No se encontró encabezado válido en {ruta}")
                return None

            # Leer desde ese punto como CSV
            df = pd.read_csv(ruta, skiprows=indice_inicio)

            if df.empty:
                self.logger.warning(f"El archivo {ruta} está vacío después del procesamiento")
                return None

            # Verificar columnas necesarias
            columnas_necesarias = ["PARAMETER", "YEAR", "JAN", "FEB", "MAR", "APR",
                                 "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

            columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
            if columnas_faltantes:
                self.logger.warning(f"Columnas faltantes en {ruta}: {columnas_faltantes}")
                return None

            # Reorganizar a formato largo
            df_largo = df.melt(id_vars=["PARAMETER", "YEAR"],
                             value_vars=["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                                       "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
                             var_name="mes", value_name="valor")

            # Convertir valores a numérico
            df_largo["valor"] = pd.to_numeric(df_largo["valor"], errors='coerce')

            # Pivotear para tener una fila por año, mes y todas las variables
            df_pivoteado = df_largo.pivot_table(index=["YEAR", "mes"],
                                              columns="PARAMETER",
                                              values="valor",
                                              aggfunc='mean').reset_index()

            # Agregar nombre del cantón y renombrar columnas
            df_pivoteado["canton"] = canton.strip().upper()
            df_pivoteado = df_pivoteado.rename(columns={"YEAR": "anio"})

            return df_pivoteado

        except Exception as e:
            self.logger.error(f"Error procesando archivo {ruta}: {e}")
            return None

    def csvs_consolidados(self) -> pd.DataFrame:
        """
        Procesa todos los archivos CSV en la carpeta.

        Returns:
            pd.DataFrame: DataFrame consolidado

        Raises:
            ValueError: Si no se pueden procesar archivos
        """
        try:
            archivos = [f for f in os.listdir(self.carpeta) if f.endswith(".csv")]

            if not archivos:
                raise ValueError(f"No se encontraron archivos CSV en {self.carpeta}")

            self.logger.info(f"Procesando {len(archivos)} archivos CSV")

            df_final = []
            csvs_consolidados = 0

            for archivo in archivos:
                ruta = os.path.join(self.carpeta, archivo)
                canton = os.path.splitext(archivo)[0]

                df_canton = self.leer_archivo(ruta, canton)
                if df_canton is not None:
                    df_final.append(df_canton)
                    csvs_consolidados += 1

            if not df_final:
                raise ValueError("No se pudo procesar ningún archivo CSV válido")

            self.logger.info(f"Se procesaron exitosamente {csvs_consolidados} de {len(archivos)} archivos")

            # Consolidar todos los DataFrames
            df_consolidado = pd.concat(df_final, ignore_index=True)



            return df_consolidado

        except Exception as e:
            self.logger.error(f"Error al procesar archivos: {e}")
            raise

