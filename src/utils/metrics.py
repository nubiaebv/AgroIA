# Custom metrics functions
# Custom metrics functions
"""
Clase: mnetrics

Objetivo: Py con funciones para utilidades a nivel de codigo

Cambios:

    1. Creacion de la funcion obtener_ruta_app con el fin de mapear la ruta raiz del proyecto
    pmarin 30-06-2025
"""
import os


def obtener_ruta_app(nombre_objetivo="AgroIA"):
    """
      Busca la ruta hasta la carpeta con nombre `nombre_objetivo`, subiendo desde la ruta actual.

      Retorna:
          str | None: Ruta completa si se encuentra, None si no.
      """
    try:
        ruta_actual = os.path.dirname(__file__)
    except NameError:
        # Para entornos donde __file__ no existe, como Jupyter
        ruta_actual = os.getcwd()
    except Exception as e:
        print(f"[ERROR] No se pudo determinar la ruta base: {e}")
        return None

    try:
        while True:
            if os.path.basename(ruta_actual) == nombre_objetivo:
                return ruta_actual

            ruta_padre = os.path.dirname(ruta_actual)

            if ruta_padre == ruta_actual:  # Llegamos a la raíz del sistema
                print(f"[INFO] No se encontró la carpeta '{nombre_objetivo}'.")
                return None

            ruta_actual = ruta_padre
    except Exception as e:
        print(f"[ERROR] Ocurrió un error al buscar la carpeta '{nombre_objetivo}': {e}")
        return None