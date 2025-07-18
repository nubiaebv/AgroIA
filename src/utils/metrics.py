"""
Clase: metrics

Objetivo: Py con funciones para utilidades a nivel de codigo

Cambios:
    1. Creacion de la funcion obtener_ruta_app con el fin de mapear la ruta raiz del proyecto
    pmarin 30-06-2025
    2. Corrección para Azure App Service y manejo robusto de rutas
    pmarin 18-07-2025
"""
import os
import logging

# Configurar logger para esta clase
logger = logging.getLogger(__name__)


def es_azure_app_service():
    """
    Detecta si la aplicación está ejecutándose en Azure App Service
    """
    return os.getenv('WEBSITE_SITE_NAME') is not None


def obtener_ruta_azure():
    """
    Obtiene la ruta raíz específica para Azure App Service
    """
    try:
        # Rutas comunes en Azure App Service
        rutas_azure = [
            '/home/site/wwwroot',  # Ruta estándar de Azure
            '/tmp/8ddc5a12a87247f',  # Tu ruta actual específica
            os.getcwd(),  # Directorio actual de trabajo
        ]

        for ruta in rutas_azure:
            if os.path.exists(ruta):
                # Verificar que contenga los archivos principales
                archivos_principales = ['main.py', 'src', 'app']
                archivos_encontrados = [f for f in archivos_principales if os.path.exists(os.path.join(ruta, f))]

                if len(archivos_encontrados) >= 2:  # Al menos 2 archivos principales
                    logger.info(f"Usando ruta de Azure App Service: {ruta}")
                    return ruta

        # Fallback: usar directorio actual si tiene la estructura correcta
        directorio_actual = os.getcwd()
        if os.path.exists(os.path.join(directorio_actual, 'main.py')):
            logger.info(f"Usando directorio actual con main.py: {directorio_actual}")
            return directorio_actual

    except Exception as e:
        logger.error(f"Error al obtener ruta de Azure: {e}")

    return None


def obtener_ruta_local(nombre_objetivo="AgroIA"):
    """
    Busca la ruta hasta la carpeta con nombre `nombre_objetivo` en entorno local
    """
    try:
        ruta_actual = os.path.dirname(__file__)
    except NameError:
        # Para entornos donde __file__ no existe, como Jupyter
        ruta_actual = os.getcwd()
    except Exception as e:
        logger.error(f"No se pudo determinar la ruta base: {e}")
        return None

    try:
        iteraciones = 0
        max_iteraciones = 10  # Prevenir bucles infinitos

        while iteraciones < max_iteraciones:
            if os.path.basename(ruta_actual) == nombre_objetivo:
                logger.info(f"Carpeta '{nombre_objetivo}' encontrada en: {ruta_actual}")
                return ruta_actual

            ruta_padre = os.path.dirname(ruta_actual)

            if ruta_padre == ruta_actual:  # Llegamos a la raíz del sistema
                logger.warning(f"No se encontró la carpeta '{nombre_objetivo}' - llegamos a la raíz")
                break

            ruta_actual = ruta_padre
            iteraciones += 1

        logger.warning(f"No se encontró la carpeta '{nombre_objetivo}' después de {max_iteraciones} iteraciones")
        return None

    except Exception as e:
        logger.error(f"Error al buscar la carpeta '{nombre_objetivo}': {e}")
        return None


def obtener_ruta_app(nombre_objetivo="AgroIA"):
    """
    Versión simplificada y robusta para Azure App Service y entornos locales

    Args:
        nombre_objetivo (str): Nombre de la carpeta objetivo a buscar (solo para entornos locales)

    Returns:
        str: Ruta completa válida (nunca None)
    """
    try:
        directorio_actual = os.getcwd()
        logger.info(f"Directorio actual: {directorio_actual}")

        # Verificar que el directorio actual contenga los archivos principales
        archivos_principales = ['main.py', 'src', 'app']
        archivos_encontrados = []

        for archivo in archivos_principales:
            ruta_archivo = os.path.join(directorio_actual, archivo)
            if os.path.exists(ruta_archivo):
                archivos_encontrados.append(archivo)

        logger.info(f"Archivos principales encontrados: {archivos_encontrados}")

        # Si encontramos al menos 2 archivos principales, usar directorio actual
        if len(archivos_encontrados) >= 2:
            logger.info(
                f"Usando directorio actual (tiene {len(archivos_encontrados)} archivos principales): {directorio_actual}")
            return directorio_actual

        # Si estamos en Azure App Service, usar directorio actual aunque no tenga todos los archivos
        if es_azure_app_service():
            logger.info(f"En Azure App Service, usando directorio actual: {directorio_actual}")
            return directorio_actual

        # Para entornos locales, intentar buscar la carpeta objetivo
        ruta_local = obtener_ruta_local(nombre_objetivo)
        if ruta_local:
            logger.info(f"Encontrada carpeta objetivo en entorno local: {ruta_local}")
            return ruta_local

        # Fallback: usar directorio actual siempre
        logger.info(f"Usando directorio actual como fallback: {directorio_actual}")
        return directorio_actual

    except Exception as e:
        logger.error(f"Error en obtener_ruta_app: {e}")
        # Último recurso: directorio de trabajo actual
        try:
            fallback = os.getcwd()
            logger.info(f"Usando último recurso: {fallback}")
            return fallback
        except:
            logger.error("No se pudo obtener ni siquiera el directorio actual")
            return "."


def validar_ruta_app(ruta):
    """
    Valida que la ruta sea válida y accesible

    Args:
        ruta (str): Ruta a validar

    Returns:
        bool: True si la ruta es válida, False en caso contrario
    """
    try:
        if not ruta:
            return False

        if not isinstance(ruta, (str, bytes, os.PathLike)):
            return False

        if not os.path.exists(ruta):
            logger.warning(f"La ruta no existe: {ruta}")
            return False

        if not os.path.isdir(ruta):
            logger.warning(f"La ruta no es un directorio: {ruta}")
            return False

        # Verificar que sea accesible
        try:
            os.listdir(ruta)
            return True
        except PermissionError:
            logger.warning(f"Sin permisos para acceder a la ruta: {ruta}")
            return False

    except Exception as e:
        logger.error(f"Error al validar ruta: {e}")
        return False


def obtener_informacion_entorno():
    """
    Obtiene información del entorno para debugging
    """
    info = {
        'es_azure': es_azure_app_service(),
        'directorio_actual': os.getcwd(),
        'directorio_archivo': os.path.dirname(__file__) if '__file__' in globals() else 'N/A',
        'estructura_directorio': [],
        'variables_azure': {
            'WEBSITE_SITE_NAME': os.getenv('WEBSITE_SITE_NAME'),
            'WEBSITE_CONTENTSHARE': os.getenv('WEBSITE_CONTENTSHARE'),
            'PYTHONPATH': os.getenv('PYTHONPATH'),
        }
    }

    # Listar archivos en el directorio actual
    try:
        archivos = os.listdir(os.getcwd())
        info['estructura_directorio'] = archivos[:10]  # Primeros 10 archivos
    except Exception as e:
        info['estructura_directorio'] = f"Error al listar: {e}"

    logger.info(f"Información del entorno: {info}")
    return info