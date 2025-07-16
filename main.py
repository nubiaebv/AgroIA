"""
Clase: main

Objetivo: Clase principal donde llama al menu principal

Cambios:
    1. Creacion de la clase y cascarazon visual pmarin 06-07-2025
    2. Implementación de control de excepciones robusto 06-07-2025
"""
import os
import sys
import threading
import logging
from pathlib import Path

import streamlit as st
import uvicorn

from src.utils.metrics import obtener_ruta_app

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Agrega el path del proyecto raíz para que se pueda importar src.*
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from app.Home import Home
    logger.info("Módulo Home importado exitosamente")
except ImportError as e:
    logger.error(f"Error al importar Home: {e}")
    st.error("Error crítico: No se pudo importar el módulo Home")
    sys.exit(1)

def crear_config_streamlit(max_mb=2000):
    """
    Crea la configuración de Streamlit con manejo de excepciones
    """
    try:
        # Determinar ruta según sistema operativo
        if os.name == "nt":
            ruta_config = os.path.expandvars(r"%USERPROFILE%\.streamlit\config.toml")
        else:
            ruta_config = os.path.expanduser("~/.streamlit/config.toml")

        # Crear directorio si no existe
        directorio_config = os.path.dirname(ruta_config)
        Path(directorio_config).mkdir(parents=True, exist_ok=True)

        contenido = f"""
[server]
maxUploadSize = {max_mb}
"""

        with open(ruta_config, "w", encoding='utf-8') as f:
            f.write(contenido.strip())

        logger.info(f"Archivo config.toml creado/actualizado en: {ruta_config}")
        return True

    except PermissionError:
        logger.error(f"Sin permisos para crear archivo en: {ruta_config}")
        st.warning("No se pudo crear la configuración de Streamlit por permisos insuficientes")
        return False
    except OSError as e:
        logger.error(f"Error del sistema al crear config: {e}")
        st.error(f"Error del sistema: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al crear config: {e}")
        st.error(f"Error inesperado al configurar Streamlit: {e}")
        return False

def iniciar_api():
    """
    Inicia la API con manejo de excepciones
    """
    try:
        # Verificar que el directorio api existe
        api_path = os.path.join(os.path.dirname(__file__), "api")
        if not os.path.exists(api_path):
            raise FileNotFoundError(f"El directorio API no existe: {api_path}")

        # Agregar el directorio 'api' al sys.path
        sys.path.append(api_path)

        # Verificar que Api.py existe
        api_file = os.path.join(api_path, "Api.py")
        if not os.path.exists(api_file):
            raise FileNotFoundError(f"El archivo Api.py no existe: {api_file}")

        logger.info("Iniciando servidor API...")
        uvicorn.run("Api:app", host="127.0.0.1", port=8000, log_level="info")

    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado: {e}")
        st.error(f"Error: {e}")
    except ImportError as e:
        logger.error(f"Error al importar módulo API: {e}")
        st.error("Error al cargar la API. Verifica que Api.py esté configurado correctamente")
    except OSError as e:
        if "Address already in use" in str(e):
            logger.warning("Puerto 8000 ya está en uso")
            st.warning("La API ya está ejecutándose en el puerto 8000")
        else:
            logger.error(f"Error de red al iniciar API: {e}")
            st.error(f"Error de red: {e}")
    except Exception as e:
        logger.error(f"Error inesperado al iniciar API: {e}")
        st.error(f"Error inesperado en la API: {e}")

@st.cache_resource
def lanzar_api():
    """
    Lanza la API en un hilo separado con manejo de excepciones
    """
    try:
        hilo = threading.Thread(target=iniciar_api, daemon=True)
        hilo.start()
        logger.info("Hilo de API lanzado exitosamente")
        return True
    except Exception as e:
        logger.error(f"Error al lanzar hilo de API: {e}")
        st.error(f"No se pudo iniciar la API: {e}")
        return False

def main():
    """
    Función principal con manejo completo de excepciones
    """
    try:
        # Crear configuración de Streamlit
        if "config_creado" not in st.session_state:
            config_exitoso = crear_config_streamlit()
            st.session_state["config_creado"] = config_exitoso

            if not config_exitoso:
                st.warning("La aplicación continuará pero con configuración predeterminada")

        # Verificar que el directorio existe
        directorio_actual = obtener_ruta_app("AgroIA")
        if not os.path.exists(directorio_actual):
            raise FileNotFoundError(f"Directorio no encontrado: {directorio_actual}")

        # Inicializar menú
        try:
            menu = Home(directorio_actual)
            logger.info("Menú Home inicializado exitosamente")
        except Exception as e:
            logger.error(f"Error al inicializar Home: {e}")
            st.error("Error al inicializar el menú principal")
            return

        # Lanzar API
        try:
            api_exitosa = lanzar_api()
            if not api_exitosa:
                st.warning("La API no se pudo iniciar correctamente")
        except Exception as e:
            logger.error(f"Error al lanzar API: {e}")
            st.warning("Continuando sin API")

        # Ejecutar menú principal
        try:
            menu.home()
            logger.info("Aplicación ejecutándose correctamente")
        except AttributeError as e:
            logger.error(f"Error en método home(): {e}")
            st.error("Error en el método home del menú")
        except Exception as e:
            logger.error(f"Error inesperado en menu.home(): {e}")
            st.error("Error inesperado en el menú principal")

    except KeyboardInterrupt:
        logger.info("Aplicación interrumpida por el usuario")
        st.info("Aplicación detenida por el usuario")
    except SystemExit:
        logger.info("Aplicación terminada")
    except Exception as e:
        logger.critical(f"Error crítico en main(): {e}")
        st.error(f"Error crítico: {e}")
        st.info("Reinicia la aplicación para continuar")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"Error fatal al ejecutar main: {e}")
        print(f"Error fatal: {e}")
        sys.exit(1)