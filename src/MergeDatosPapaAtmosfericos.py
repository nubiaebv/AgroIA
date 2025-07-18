"""
Clase: MergeDatosPapaAtmosfericos
Clase para fusionar datos de papa con datos atmosféricos.
Cambios: 1.Creacion de la clase @fabarca
        2.
"""

import pandas as pd
import os
import logging


class MergeDatosPapaAtmosfericos:
    """
    Fusiona datasets de papa y datos atmosféricos.
    """

    def __init__(self, ruta_clima: str, ruta_papa: str):
        """
        Inicializa el fusionador con las rutas de los archivos.

        Args:
            ruta_clima (str): Ruta del archivo de datos climáticos
            ruta_papa (str): Ruta del archivo de datos de papa

        Raises:
            FileNotFoundError: Si algún archivo no existe
        """
        if not os.path.exists(ruta_clima):
            raise FileNotFoundError(f"El archivo de datos climáticos {ruta_clima} no existe")

        if not os.path.exists(ruta_papa):
            raise FileNotFoundError(f"El archivo de datos de papa {ruta_papa} no existe")

        self.ruta_clima = ruta_clima
        self.ruta_papa = ruta_papa
        self.logger = logging.getLogger(__name__)

    def traducir_mes(self, mes: str) -> str:
        """
        Traduce nombres de meses del inglés al español.

        Args:
            mes (str): Nombre del mes en inglés

        Returns:
            str: Nombre del mes en español
        """
        mapa_meses = {
            "JAN": "enero", "FEB": "febrero", "MAR": "marzo", "APR": "abril",
            "MAY": "mayo", "JUN": "junio", "JUL": "julio", "AUG": "agosto",
            "SEP": "septiembre", "OCT": "octubre", "NOV": "noviembre", "DEC": "diciembre"
        }
        return mapa_meses.get(mes.upper(), mes.lower())

    def carga_validacion_datos(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Carga y valida los datasets.

        Returns:
            tuple: (df_clima, df_papa)

        Raises:
            ValueError: Si hay problemas con los datos
        """
        try:
            # Cargar datos
            df_clima = pd.read_csv(self.ruta_clima, encoding='utf-8')
            df_papa = pd.read_csv(self.ruta_papa, encoding='utf-8')

            # Validar que no estén vacíos
            if df_clima.empty:
                raise ValueError("El archivo de datos climáticos está vacío")
            if df_papa.empty:
                raise ValueError("El archivo de datos de papa está vacío")

            # Verificar columnas necesarias
            columnas_clima_necesarias = ["anio", "mes", "canton"]
            columnas_papa_necesarias = ["anio", "mes", "canton"]

            # Verificar si existe 'año' en lugar de 'anio'
            if 'año' in df_papa.columns:
                df_papa = df_papa.rename(columns={"año": "anio"})

            # Verificar columnas faltantes
            clima_faltantes = [col for col in columnas_clima_necesarias if col not in df_clima.columns]
            papa_faltantes = [col for col in columnas_papa_necesarias if col not in df_papa.columns]

            if clima_faltantes:
                raise ValueError(f"Columnas faltantes en datos climáticos: {clima_faltantes}")
            if papa_faltantes:
                raise ValueError(f"Columnas faltantes en datos de papa: {papa_faltantes}")

            self.logger.info(f"Datos cargados - Clima: {len(df_clima)} filas, Papa: {len(df_papa)} filas")

            return df_clima, df_papa

        except Exception as e:
            self.logger.error(f"Error cargando datos: {e}")
            raise

    def merge_datasets(self) -> pd.DataFrame:
        """
        Une los datasets de papa y clima.

        Returns:
            pd.DataFrame: Dataset fusionado

        Raises:
            ValueError: Si hay problemas en la fusión
        """
        try:
            df_clima, df_papa = self.carga_validacion_datos()

            # Procesar datos climáticos
            df_clima["mes"] = df_clima["mes"].apply(self.traducir_mes)
            df_clima["canton"] = df_clima["canton"].str.strip().str.upper()
            df_clima["anio"] = pd.to_numeric(df_clima["anio"], errors='coerce')

            # Procesar datos de papa
            df_papa["canton"] = df_papa["canton"].str.strip().str.upper()
            df_papa["anio"] = pd.to_numeric(df_papa["anio"], errors='coerce')

            # Eliminar filas con valores nulos en las columnas clave
            df_clima = df_clima.dropna(subset=["anio", "mes", "canton"])
            df_papa = df_papa.dropna(subset=["anio", "mes", "canton"])

            # Realizar el merge
            df_fusionado = pd.merge(df_papa, df_clima,
                                    on=["anio", "mes", "canton"],
                                    how="left")

            # Validar resultado
            if df_fusionado.empty:
                raise ValueError("La fusión resultó en un dataset vacío")

            # Estadísticas del merge
            filas_originales = len(df_papa)
            filas_fusionadas = len(df_fusionado)
            filas_con_clima = len(df_fusionado.dropna(subset=df_clima.columns.difference(["anio", "mes", "canton"])))

            self.logger.info(f"Fusión completada:")
            self.logger.info(f"  - Filas originales: {filas_originales}")
            self.logger.info(f"  - Filas fusionadas: {filas_fusionadas}")
            self.logger.info(f"  - Filas con datos climáticos: {filas_con_clima}")

            return df_fusionado

        except Exception as e:
            self.logger.error(f"Error en la fusión de datos: {e}")
            raise