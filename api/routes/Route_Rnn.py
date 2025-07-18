"""
Clase: Route_Rnn

Objetivo: Clase para control de router de RNN

Cambios:

    1. Creacion de clase pmarin 05-07-2025
    2. Implementación de control de excepciones robusto pmarin 06-07-2025
"""
import io

import pandas as pd
from fastapi import APIRouter, HTTPException, status, UploadFile, File
import logging
from typing import Dict, Any
from api.services.Service_Rnn import Service_Rnn


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Route_Rnn:
    def __init__(self):
        try:
            self._router = APIRouter(
                prefix="/Modelo_RNN",
                tags=["Modelo_RNN"]
            )

            self._router.add_api_route(
                path="/consulta",
                endpoint=self.obtener_modelo,
                methods=["POST"],
                summary="Consulta de modelo RNN",
                description="Este endpoint permite consultar el modelo RNN"
            )

            logger.info("Router ANN inicializado correctamente")

        except Exception as e:
            logger.error(f"Error al inicializar el router RNN: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor al inicializar: {str(e)}"
            )

    def get_router(self):
        try:
            if not hasattr(self, '_router') or self._router is None:
                logger.error("Router no inicializado correctamente")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Router no disponible"
                )
            return self._router

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error al obtener el router: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno al obtener router: {str(e)}"
            )

    async def obtener_modelo(self, file: UploadFile = File(...)) -> Dict[str, Any]:
        try:
            # Validación de entrada
            if file is None:
                logger.warning("Archivo proporcionado es None")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El archivo no puede ser nulo"
                )

            if not file.filename:
                logger.warning("Nombre de archivo vacío")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El archivo debe tener un nombre válido"
                )

            # Validar extensión
            if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
                logger.warning(f"Formato no soportado: {file.filename}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Solo se permiten archivos CSV o Excel (.csv, .xlsx, .xls)"
                )

            # Validar tamaño (ejemplo: 10MB máximo)
            if file.size and file.size > 10 * 1024 * 1024:
                logger.warning(f"Archivo muy grande: {file.filename} ({file.size} bytes)")
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="El archivo es demasiado grande (máximo 10MB)"
                )

            # Leer y procesar archivo
            contents = await file.read()

            if file.filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
            else:
                df = pd.read_excel(io.BytesIO(contents))

            # Validar que no esté vacío
            if df.empty:
                logger.warning(f"Archivo vacío: {file.filename}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El archivo está vacío"
                )

            services_rnn= Service_Rnn()


            df_prediccion = services_rnn.prediccion(df)

            # Registro de operación exitosa
            logger.info(f"Archivo procesado exitosamente: {file.filename} - "
                        f"Filas: {len(df)}, Columnas: {len(df.columns)}")

            # Respuesta exitosa
            # Respuesta exitosa CON DATAFRAME COMO JSON
            return {
                "mensaje": "Archivo procesado exitosamente",
                "filename": file.filename,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "prediction": df_prediccion.to_dict('index'),  # ← AQUÍ está el DataFrame como JSON
                "timestamp": None,
                "status": "success"
            }

        except HTTPException:
            # Re-lanzar HTTPExceptions para que FastAPI las maneje correctamente
            raise
        except UnicodeDecodeError as e:
            # Error de encoding
            logger.error(f"Error de encoding en archivo {file.filename}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error de codificación del archivo. Verifique que sea UTF-8"
            )
        except pd.errors.EmptyDataError as e:
            # Error de archivo vacío o corrupto
            logger.error(f"Archivo corrupto: {file.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo está corrupto o vacío"
            )
        except Exception as e:
            # Error genérico no previsto
            logger.error(f"Error inesperado procesando archivo {file.filename}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor. Contacte al administrador."
            )