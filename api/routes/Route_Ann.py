"""
Clase: Route_Ann
Objetivo: Clase para control de router de ANN
Cambios:
    1. Creacion de clase pmarin 05-07-2025
    2. Implementación de control de excepciones robusto pmarin 06-07-2025
"""
from fastapi import APIRouter, Query, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any

from api.services.Service_Ann import Service_Ann

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Route_Ann:

    def __init__(self):
        try:
            self._router = APIRouter(
                prefix="/Modelo_ANN",
                tags=["Modelo_ANN"]
            )

            self._router.add_api_route(
                path="/consulta",
                endpoint=self.obtener_modelo,
                methods=["GET"],
                summary="Consulta de modelo ANN",
                description="Este endpoint permite consultar el modelo ANN"
            )

            logger.info("Router ANN inicializado correctamente")

        except Exception as e:
            logger.error(f"Error al inicializar el router ANN: {str(e)}")
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

    def obtener_modelo(self, precipitacion,  temperatura_max, temperatura_min,
                       humedad_aire, ph_suelo) -> Dict[str, Any]:
        """
        Obtiene predicción del modelo ANN usando Service_Ann
        Sigue el mismo patrón que la ejecución manual
        """
        try:
            # Validaciones básicas
            if any(param is None for param in [precipitacion, temperatura_max, temperatura_min, humedad_aire, ph_suelo]):
                logger.warning("Parámetros nulos proporcionados")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Todos los parámetros son requeridos"
                )

            # Crear fila de datos igual que en el código manual
            fila = {
                "lluvia_mm": precipitacion,
                "temp_max": temperatura_max,
                "temp_min": temperatura_min,
                "humedad": humedad_aire,
                "ph_suelo": ph_suelo
            }

            # Generar predicción igual que en el código manual
            service_ann = Service_Ann(fila)
            prediccion_info = service_ann.prediccion()

            # Registro de operación exitosa
            logger.info(f"Predicción exitosa: {prediccion_info['prediccion']}")

            # Respuesta exitosa
            respuesta = {
                "mensaje": "Predicción generada exitosamente",
                "datos_entrada": fila,
                "prediccion": prediccion_info,
                "status": "success"
            }

            # Convertir tipos numpy a tipos nativos de Python antes de retornar
            return self.convertir_numpy_a_python(respuesta)

        except HTTPException:
            # Re-lanzar HTTPExceptions para que FastAPI las maneje correctamente
            raise
        except ValueError as e:
            # Error de conversión de tipos
            logger.error(f"Error de validación de datos: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de validación: {str(e)}"
            )
        except FileNotFoundError as e:
            # Error si no se encuentra el modelo
            logger.error(f"Modelo no encontrado: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modelo de predicción no encontrado. Contacte al administrador."
            )
        except Exception as e:
            # Error genérico no previsto
            logger.error(f"Error inesperado en obtener_modelo: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor. Contacte al administrador."
            )

    def convertir_numpy_a_python(self, obj):
        """
        Convierte tipos numpy a tipos nativos de Python para serialización JSON
        """
        import numpy as np

        if isinstance(obj, dict):
            return {key: self.convertir_numpy_a_python(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.convertir_numpy_a_python(item) for item in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
