"""
Pipeline centralizado para el procesamiento completo de datos.
"""

import pandas as pd
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime

from src.ProcesadorDatosPapa import ProcesadorDatosPapa
from src.ProcesadorDatosAtmosfericos import ProcesadorDatosAtmosfericos
from src.MergeDatosPapaAtmosfericos import MergeDatosPapaAtmosfericos


class PipelineProcesamiento:
    """
    Pipeline centralizado para procesar datos de papa y clima.
    """

    def __init__(self,
                 ruta_excel_papa: str,
                 carpeta_datos_atmosfericos: str,
                 log_level: str = "INFO"):
        """
        Inicializa el pipeline con las rutas necesarias.

        Args:
            ruta_excel_papa (str): Ruta del archivo Excel con datos de papa
            carpeta_datos_atmosfericos (str): Carpeta con archivos CSV de datos atmosféricos
            log_level (str): Nivel de logging (DEBUG, INFO, WARNING, ERROR)
        """
        self.ruta_excel_papa = ruta_excel_papa
        self.carpeta_datos_atmosfericos = carpeta_datos_atmosfericos

        # Configurar logging
        self._configurar_logging(log_level)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Pipeline inicializado correctamente")

    def _configurar_logging(self, log_level: str) -> None:
        """
        Configura el sistema de logging.

        Args:
            log_level (str): Nivel de logging
        """
        # Crear carpeta logs si no existe
        os.makedirs("logs", exist_ok=True)

        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(f'logs/pipeline_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
            ]
        )

    def _validar_archivos_entrada(self) -> None:
        """
        Valida que existan los archivos y carpetas de entrada.

        Raises:
            FileNotFoundError: Si faltan archivos o carpetas
        """
        if not os.path.exists(self.ruta_excel_papa):
            raise FileNotFoundError(f"Archivo Excel no encontrado: {self.ruta_excel_papa}")

        if not os.path.exists(self.carpeta_datos_atmosfericos):
            raise FileNotFoundError(f"Carpeta de datos atmosféricos no encontrada: {self.carpeta_datos_atmosfericos}")

        if not os.path.isdir(self.carpeta_datos_atmosfericos):
            raise NotADirectoryError(f"La ruta no es una carpeta válida: {self.carpeta_datos_atmosfericos}")

        # Verificar que hay archivos CSV en la carpeta
        archivos_csv = [f for f in os.listdir(self.carpeta_datos_atmosfericos) if f.endswith('.csv')]
        if not archivos_csv:
            raise FileNotFoundError(f"No se encontraron archivos CSV en: {self.carpeta_datos_atmosfericos}")

        self.logger.info("Validación de archivos de entrada completada")

    def procesar_datos_papa(self) -> pd.DataFrame:
        """
        Procesa los datos de papa.

        Returns:
            pd.DataFrame: DataFrame procesado
        """
        try:
            self.logger.info("Iniciando procesamiento de datos de papa")

            procesador_papa = ProcesadorDatosPapa(self.ruta_excel_papa)
            df_papa = procesador_papa.procesar_formato_largo()

            self.logger.info("Procesamiento de datos de papa completado")
            return df_papa

        except Exception as e:
            self.logger.error(f"Error procesando datos de papa: {e}")
            raise

    def procesar_datos_atmosfericos(self) -> pd.DataFrame:
        """
        Procesa los datos atmosféricos.

        Returns:
            pd.DataFrame: DataFrame procesado
        """
        try:
            self.logger.info("Iniciando procesamiento de datos atmosféricos")

            procesador_atmosferico = ProcesadorDatosAtmosfericos(
                self.carpeta_datos_atmosfericos)

            df_clima = procesador_atmosferico.csvs_consolidados()

            self.logger.info("Procesamiento de datos atmosféricos completado")
            return df_clima

        except Exception as e:
            self.logger.error(f"Error procesando datos atmosféricos: {e}")
            raise

    def fusionar_datos(self, df_papa: pd.DataFrame, df_clima: pd.DataFrame) -> pd.DataFrame:
        """
        Fusiona los datos de papa y clima.

        Args:
            df_papa (pd.DataFrame): DataFrame de datos de papa
            df_clima (pd.DataFrame): DataFrame de datos climáticos

        Returns:
            pd.DataFrame: DataFrame fusionado
        """
        try:
            self.logger.info("Iniciando fusión de datos")

            # Crear archivos temporales para el merge
            import tempfile

            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_clima:
                df_clima.to_csv(tmp_clima.name, index=False, encoding='utf-8')
                ruta_tmp_clima = tmp_clima.name

            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_papa:
                df_papa.to_csv(tmp_papa.name, index=False, encoding='utf-8')
                ruta_tmp_papa = tmp_papa.name

            # Realizar la fusión
            fusionador = MergeDatosPapaAtmosfericos(ruta_tmp_clima, ruta_tmp_papa)
            df_fusionado = fusionador.merge_datasets()

            # Limpiar archivos temporales
            os.unlink(ruta_tmp_clima)
            os.unlink(ruta_tmp_papa)

            self.logger.info("Fusión completada")
            return df_fusionado

        except Exception as e:
            self.logger.error(f"Error fusionando datos: {e}")
            raise


    def ejecutar_pipeline_completo(self) -> pd.DataFrame:
        """
        Ejecuta todo el pipeline de procesamiento.

        Returns:
            tuple: (ruta_archivo_final, reporte_calidad)

        Raises:
            Exception: Si hay errores en cualquier paso del pipeline
        """
        try:
            inicio = datetime.now()
            self.logger.info("=== INICIANDO PIPELINE COMPLETO ===")

            # Validar archivos de entrada
            self._validar_archivos_entrada()

            # Procesar datos de papa
            df_papa = self.procesar_datos_papa()

            # Procesar datos atmosféricos
            df_clima = self.procesar_datos_atmosfericos()

            # Fusionar datos
            df_final = self.fusionar_datos(df_papa, df_clima)

            # Calcular tiempo total
            tiempo_total = datetime.now() - inicio

            self.logger.info(f"=== PIPELINE COMPLETADO EXITOSAMENTE ===")
            self.logger.info(f"Tiempo total: {tiempo_total}")

            return df_final

        except Exception as e:
            self.logger.error(f"Error en pipeline completo: {e}")
            raise
