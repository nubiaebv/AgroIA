"""
Clase: cnn

Objetivo: Clase para llamado de modelo entrenado

Cambios:

    1. Creacion de clase pmarin 13-07-2025
"""
import os

from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np
from typing import Dict, Any
# CNN training script
class cnn:
    def __init__(self, ruta_raiz):
        self.model =load_model(os.path.join(ruta_raiz,'models/modelo_CNN_Papas.h5'))
        # Diccionario invertido para obtener nombre por índice
        self.clases = {0: 'Potato_Early_blight', 1: 'Potato_Late_blight', 2: 'Potato_healthy'}

    def _get_diagnostico_info(self,resultado: str) -> Dict[str, Any]:
        """
        Obtiene información detallada del diagnóstico según el resultado

        Args:
            resultado (str): Clase predicha por el modelo

        Returns:
            Dict: Información estructurada del diagnóstico
        """
        diagnosticos = {
            "Potato_healthy": {
                "emoji_resultado": "✅ Sana",
                "color_metrica": "normal",
                "tipo_mensaje": "success",
                "icono_estado": "🌿",
                "mensaje_estado": "La papa está completamente sana",
                "recomendacion": "Mantener las prácticas actuales de cuidado",
                "severidad": "ninguna",
                "descripcion": "La planta no presenta signos de enfermedad y se encuentra en perfecto estado de salud.",
                "acciones_sugeridas": [
                    "Continuar con el riego regular",
                    "Mantener el programa de fertilización",
                    "Realizar inspecciones preventivas periódicas",
                    "Conservar las condiciones ambientales actuales"
                ]
            },
            "Potato_Early_blight": {
                "emoji_resultado": "⚠️ Tizón Temprano",
                "color_metrica": "normal",
                "tipo_mensaje": "warning",
                "icono_estado": "⚠️",
                "mensaje_estado": "Se detectó tizón temprano (Early Blight)",
                "recomendacion": "Aplicar fungicida preventivo y mejorar ventilación",
                "severidad": "media",
                "descripcion": "El tizón temprano es una enfermedad fúngica que puede causar manchas circulares en las hojas y reducir el rendimiento.",
                "acciones_sugeridas": [
                    "Aplicar fungicida preventivo (clorotalonil o mancozeb)",
                    "Mejorar la ventilación del cultivo",
                    "Remover hojas infectadas",
                    "Evitar riego por aspersión",
                    "Aumentar el espaciado entre plantas"
                ]
            },
            "Potato_Late_blight": {
                "emoji_resultado": "🚨 Tizón Tardío",
                "color_metrica": "normal",
                "tipo_mensaje": "error",
                "icono_estado": "🚨",
                "mensaje_estado": "Se detectó tizón tardío (Late Blight)",
                "recomendacion": "Tratamiento urgente con fungicida específico",
                "severidad": "alta",
                "descripcion": "El tizón tardío es una enfermedad muy destructiva que puede devastar cultivos enteros rápidamente.",
                "acciones_sugeridas": [
                    "Aplicar fungicida específico inmediatamente (metalaxil + mancozeb)",
                    "Aumentar frecuencia de aplicación",
                    "Remover y destruir plantas severamente infectadas",
                    "Mejorar drenaje del suelo",
                    "Monitorear condiciones de humedad",
                    "Considerar tratamiento de tubérculos"
                ]
            }
        }

        return diagnosticos.get(resultado, {
            "emoji_resultado": "❓ Desconocido",
            "color_metrica": "normal",
            "tipo_mensaje": "warning",
            "icono_estado": "❓",
            "mensaje_estado": f"Resultado no reconocido: {resultado}",
            "recomendacion": "Consultar con un especialista en patología vegetal",
            "severidad": "desconocida",
            "descripcion": "El resultado no corresponde a ninguna clase conocida del modelo.",
            "acciones_sugeridas": [
                "Revisar la calidad de la imagen",
                "Consultar con un especialista",
                "Realizar análisis adicionales"
            ]
        })

    def predeccir_imagen_api(self, imagen):
        # Convertir imagen PIL a numpy array
        if isinstance(imagen, Image.Image):
            imagen_array = np.array(imagen)
        else:
            imagen_array = imagen

        # Asegurar que la imagen tenga 3 canales (RGB)
        if len(imagen_array.shape) == 3 and imagen_array.shape[2] == 4:
            imagen_array = imagen_array[:, :, :3]
        elif len(imagen_array.shape) == 2:
            imagen_array = cv2.cvtColor(imagen_array, cv2.COLOR_GRAY2RGB)

        imagen_nueva = cv2.resize(imagen_array, (256, 256))
        nueva_imagen = image.img_to_array(imagen_nueva)
        nueva_imagen = np.expand_dims(nueva_imagen, axis=0)

        if nueva_imagen.max() > 1.0:
            nueva_imagen = nueva_imagen / 255.0

        prediccion_prob = self.model.predict(nueva_imagen)
        indice_clase = np.argmax(prediccion_prob, axis=1)[0]


        return self._get_diagnostico_info(self.clases[indice_clase])

    def predeccir_imagen(self, imagen):
        # Convertir imagen PIL a numpy array
        if isinstance(imagen, Image.Image):
            imagen_array = np.array(imagen)
        else:
            imagen_array = imagen

        # Asegurar que la imagen tenga 3 canales (RGB)
        if len(imagen_array.shape) == 3 and imagen_array.shape[2] == 4:
            imagen_array = imagen_array[:, :, :3]
        elif len(imagen_array.shape) == 2:
            imagen_array = cv2.cvtColor(imagen_array, cv2.COLOR_GRAY2RGB)

        imagen_nueva = cv2.resize(imagen_array, (256, 256))
        nueva_imagen = image.img_to_array(imagen_nueva)
        nueva_imagen = np.expand_dims(nueva_imagen, axis=0)

        if nueva_imagen.max() > 1.0:
            nueva_imagen = nueva_imagen / 255.0

        prediccion_prob = self.model.predict(nueva_imagen)
        indice_clase = np.argmax(prediccion_prob, axis=1)[0]

        return self.clases[indice_clase]






