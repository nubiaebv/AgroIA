"""
Clase: Api

Objetivo: Archivo que ejecuta el Api en segundo plano

Cambios:
    1. Creacion de clase pmarin 05-07-2025
    2. Implementación de control de excepciones 06-07-2025
"""

import logging
from fastapi import FastAPI, HTTPException
from routes.Route_Ann import Route_Ann
from routes.Route_Cnn import Route_Cnn
from routes.Route_Rnn import Route_Rnn

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    # Crear instancia de FastAPI
    app = FastAPI(
        title="API de Modelos ANN",
        description="API que gestiona consultas al modelos de redes neuronales",
        version="1.0.0"
    )
    logger.info("Aplicación FastAPI creada exitosamente")

    # Incluir el router de ANN
    try:
        ann_router = Route_Ann()
        # Validar que el router tiene el método get_router
        if not hasattr(ann_router, 'get_router'):
            raise AttributeError("Route_Ann no tiene método get_router")
        router = ann_router.get_router()
        app.include_router(router)
        logger.info("Router ANN incluido exitosamente")
    except ImportError as e:
        logger.error(f"Error al importar Route_Ann: {e}")
        logger.warning("La aplicación continuará sin el router ANN")


        # Agregar ruta de fallback
        @app.get("/ann/status")
        async def ann_status():
            return {
                "status": "unavailable",
                "message": "El módulo ANN no está disponible"
            }
    except AttributeError as e:
        logger.error(f"Error en Route_Ann: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error de configuración en Route_Ann"
        )
    except Exception as e:
        logger.error(f"Error inesperado al incluir router: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al configurar el router ANN"
        )

    # Incluir el router de CNN
    try:
        cnn_router = Route_Cnn()
        # Validar que el router tiene el método get_router
        if not hasattr(cnn_router, 'get_router'):
            raise AttributeError("Route_Cnn no tiene método get_router")
        router = cnn_router.get_router()
        app.include_router(router)
        logger.info("Router CNN incluido exitosamente")
    except ImportError as e:
        logger.error(f"Error al importar Route_Cnn: {e}")
        logger.warning("La aplicación continuará sin el router CNN")


        # Agregar ruta de fallback
        @app.get("/cnn/status")
        async def ann_status():
            return {
                "status": "unavailable",
                "message": "El módulo CNN no está disponible"
            }
    except AttributeError as e:
        logger.error(f"Error en Route_Cnn: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error de configuración en Route_Cnn"
        )
    except Exception as e:
        logger.error(f"Error inesperado al incluir router: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al configurar el router CNN"
        )

    # Incluir el router de RNN
    try:
        rnn_router = Route_Rnn()
        # Validar que el router tiene el método get_router
        if not hasattr(rnn_router, 'get_router'):
            raise AttributeError("Route_Rnn no tiene método get_router")
        router = rnn_router.get_router()
        app.include_router(router)
        logger.info("Router CNN incluido exitosamente")
    except ImportError as e:
        logger.error(f"Error al importar Route_Rnn: {e}")
        logger.warning("La aplicación continuará sin el router RNN")


        # Agregar ruta de fallback
        @app.get("/rnn/status")
        async def ann_status():
            return {
                "status": "unavailable",
                "message": "El módulo RNN no está disponible"
            }
    except AttributeError as e:
        logger.error(f"Error en Route_Rnn: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error de configuración en Route_Rnn"
        )
    except Exception as e:
        logger.error(f"Error inesperado al incluir router: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al configurar el router RNN"
        )
except Exception as e:
    logger.critical(f"Error crítico al crear la aplicación: {e}")
    raise