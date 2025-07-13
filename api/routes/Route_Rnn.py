"""
Clase: Route_Rnn

Objetivo: Clase para control de router de RNN

Cambios:

    1. Creacion de clase pmarin 05-07-2025
    2. Implementación de control de excepciones robusto pmarin 06-07-2025
"""
from fastapi import APIRouter, Query, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any

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
                methods=["GET"],
                summary="Consulta de modelo RNN",
                description="Este endpoint permite consultar el modelo RNN con un ID."
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

    def obtener_modelo(self, id: int = Query(..., description="ID del modelo a consultar")) -> Dict[str, Any]:
        try:
            # Validación de entrada
            if id is None:
                logger.warning("ID proporcionado es None")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El ID no puede ser nulo"
                )

            if id <= 0:
                logger.warning(f"ID inválido proporcionado: {id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El ID debe ser un número positivo mayor a 0"
                )

            if id > 999999:  # Límite razonable para IDs
                logger.warning(f"ID fuera de rango: {id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El ID está fuera del rango permitido (1-999999)"
                )

            # Simulación de validación de existencia del modelo
            # En una implementación real, aquí consultarías la base de datos
            if id == 404:  # Ejemplo de ID no encontrado
                logger.warning(f"Modelo con ID {id} no encontrado")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Modelo con ID {id} no encontrado"
                )

            # Registro de operación exitosa
            logger.info(f"Consulta exitosa para modelo ID: {id}")

            # Respuesta exitosa
            return {
                "mensaje": "Consulta de modelo exitoso",
                "id": id,
                "timestamp": None,  # Se podría agregar timestamp si es necesario
                "status": "success"
            }

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
        except Exception as e:
            # Error genérico no previsto
            logger.error(f"Error inesperado en obtener_modelo: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor. Contacte al administrador."
            )