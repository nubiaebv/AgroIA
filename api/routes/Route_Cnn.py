"""
Clase: Route_Cnn

Objetivo: Clase para control de router de CNN

Cambios:

    1. Creacion de clase pmarin 05-07-2025
    2. Implementación de control de excepciones robusto pmarin 06-07-2025
"""
import io

from PIL import Image
from fastapi import APIRouter, Query, HTTPException, status, UploadFile, File
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any
from api.services.Service_Cnn import Service_Cnn
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Route_Cnn:
    def __init__(self):
        try:
            self._router = APIRouter(
                prefix="/Modelo_CNN",
                tags=["Modelo_CNN"]
            )

            self._router.add_api_route(
                path="/consulta",
                endpoint=self.obtener_modelo,
                methods=["POST"],
                summary="Realizar prediccion CNN",
                description="Este endpoint permite realizar la prediccion del modelo CNN"
            )

            logger.info("Router CNN inicializado correctamente")

        except Exception as e:
            logger.error(f"Error al inicializar el router CNN: {str(e)}")
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

    def obtener_modelo(self, file: UploadFile = File(...)) -> Dict[str, Any]:
        """
        Procesa una imagen para detectar enfermedades en papas usando CNN

        Args:
            file: Archivo de imagen subido

        Returns:
            Dict con el resultado del diagnóstico
        """
        try:
            # Validar tipo de archivo
            if not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El archivo debe ser una imagen"
                )

            # Leer y procesar la imagen
            contents = file.file.read()
            imagen = Image.open(io.BytesIO(contents))

            # Convertir a RGB si es necesario
            if imagen.mode != 'RGB':
                imagen = imagen.convert('RGB')

            # Crear instancia del servicio y realizar predicción
            servicio_cnn = Service_Cnn(imagen)
            resultado_diagnostico = servicio_cnn.prediccion()

            # Registro de operación exitosa
            logger.info(f"Diagnóstico exitoso para imagen: {file.filename}")

            # Respuesta exitosa con información detallada del diagnóstico
            return {
                "mensaje": "Diagnóstico completado exitosamente",
                "archivo": file.filename,
                "diagnostico": {
                    "resultado": resultado_diagnostico["emoji_resultado"],
                    "estado": resultado_diagnostico["mensaje_estado"],
                    "severidad": resultado_diagnostico["severidad"],
                    "descripcion": resultado_diagnostico["descripcion"],
                    "recomendacion": resultado_diagnostico["recomendacion"],
                    "acciones_sugeridas": resultado_diagnostico["acciones_sugeridas"]
                },
                "metadata": {
                    "tipo_mensaje": resultado_diagnostico["tipo_mensaje"],
                    "icono_estado": resultado_diagnostico["icono_estado"],
                    "color_metrica": resultado_diagnostico["color_metrica"]
                },
                "timestamp": None,  # Se podría agregar timestamp si es necesario
                "status": "success"
            }

        except HTTPException:
            # Re-lanzar HTTPExceptions para que FastAPI las maneje correctamente
            raise
        except ValueError as e:
            # Error de conversión de tipos o validación
            logger.error(f"Error de validación de datos: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de validación: {str(e)}"
            )
        except Exception as e:
            # Error genérico no previsto
            logger.error(f"Error inesperado en obtener_modelo: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor. Contacte al administrador."
            )
        finally:
            # Cerrar el archivo si está abierto
            if hasattr(file.file, 'close'):
                file.file.close()