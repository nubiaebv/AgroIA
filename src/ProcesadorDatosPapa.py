"""
Clase: ProcesadorDatosPapa
Clase para limpiar y transformar datos de producción de papa.
Procesa archivos Excel con datos de producción y área sembrada por cantón, año y mes.
Cambios: 1.Creacion de la clase.
        2. Cambios de nombre a los metodos
"""

import pandas as pd
import os
from typing import List, Optional
import logging


class ProcesadorDatosPapa:
    """
    Procesa datos de producción de papa desde archivos Excel al formato largo.
    """

    def __init__(self, archivo_excel: str):
        """
        Inicializa el procesador con la ruta del archivo Excel.

        Args:
            archivo_excel (str): Ruta completa al archivo Excel

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el archivo no es válido
        """
        if not os.path.exists(archivo_excel):
            raise FileNotFoundError(f"El archivo {archivo_excel} no existe")

        if not archivo_excel.lower().endswith(('.xls', '.xlsx')):
            raise ValueError(f"El archivo debe ser Excel (.xls o .xlsx), recibido: {archivo_excel}")

        self.archivo = archivo_excel
        self.nombres_interes = ['Turrialba', 'Oreamuno', 'El Guarco', 'Cartago', 'Alvarado']
        self.meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                      'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        self.df_largo = None
        self.logger = logging.getLogger(__name__)

    def procesar_formato_largo(self) -> pd.DataFrame:
        """
        Procesa el archivo Excel directamente al formato largo.

        Returns:
            pd.DataFrame: DataFrame con los datos en formato largo

        Raises:
            Exception: Si hay problemas al procesar el archivo
        """
        try:
            xls = pd.ExcelFile(self.archivo)
            hojas = xls.sheet_names
            self.logger.info(f"Procesando {len(hojas)} hojas del archivo Excel")

            if not hojas:
                raise ValueError("El archivo Excel no contiene hojas válidas")

            datos = []

            for hoja in hojas:
                try:
                    # Leer hoja con encabezado en fila 6 (index=5)
                    df = pd.read_excel(self.archivo, sheet_name=hoja, header=5)

                    if df.empty:
                        self.logger.warning(f"La hoja {hoja} está vacía, omitiendo...")
                        continue

                    # Nombre de la primera columna (cantones)
                    nombre_columna_a = df.columns[0]

                    # Filtrar filas por cantones de interés
                    df_filtrado = df[df[nombre_columna_a].isin(self.nombres_interes)].copy()

                    if df_filtrado.empty:
                        self.logger.warning(f"No se encontraron cantones de interés en la hoja {hoja}")
                        continue

                    # Armar lista de nuevos nombres
                    nuevos_nombres = ['canton']
                    for mes in self.meses:
                        nuevos_nombres.append(f'{mes}_produccion')
                        nuevos_nombres.append(f'{mes}_area')

                    # Verificar que hay suficientes columnas
                    if len(df_filtrado.columns) < len(nuevos_nombres):
                        self.logger.warning(f"La hoja {hoja} no tiene suficientes columnas, omitiendo...")
                        continue

                    # Cortar el DataFrame para que solo tenga la cantidad correcta de columnas
                    df_filtrado = df_filtrado.iloc[:, :len(nuevos_nombres)]
                    df_filtrado.columns = nuevos_nombres

                    # Transformar a formato largo
                    for _, fila in df_filtrado.iterrows():
                        for mes in self.meses:
                            try:
                                produccion = pd.to_numeric(fila[f'{mes}_produccion'], errors='coerce')
                                area = pd.to_numeric(fila[f'{mes}_area'], errors='coerce')

                                datos.append({
                                    'canton': str(fila['canton']).strip(),
                                    'mes': mes,
                                    'anio': int(hoja) if str(hoja).isdigit() else hoja,
                                    'produccion': produccion,
                                    'area': area
                                })
                            except (ValueError, KeyError) as e:
                                self.logger.warning(f"Error procesando datos de {hoja}, {mes}: {e}")
                                continue

                except Exception as e:
                    self.logger.error(f"Error procesando hoja {hoja}: {e}")
                    continue

            if not datos:
                raise ValueError("No se pudieron procesar datos de ninguna hoja")

            # Crear el DataFrame en formato largo
            self.df_largo = pd.DataFrame(datos)
            self.logger.info(f"Procesamiento completado: {len(self.df_largo)} registros")

            return self.df_largo

        except Exception as e:
            self.logger.error(f"Error al procesar archivo Excel: {e}")
            raise

    def exportar(self, ruta_csv: str = None) -> pd.DataFrame:
        """
        Ejecuta todo el proceso: procesar Excel a formato largo.

        Args:
            ruta_csv (str, optional): Ruta para guardar el archivo CSV (opcional)

        Returns:
            pd.DataFrame: DataFrame procesado
        """
        df = self.procesar_formato_largo()

        # Solo exportar si se especifica una ruta
        if ruta_csv:
            try:
                # Crear directorio si no existe
                os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)

                self.df_largo.to_csv(ruta_csv, index=False, encoding='utf-8')
                self.logger.info(f"Archivo CSV guardado en: {ruta_csv}")

            except Exception as e:
                self.logger.error(f"Error al exportar CSV: {e}")
                raise

        return df
