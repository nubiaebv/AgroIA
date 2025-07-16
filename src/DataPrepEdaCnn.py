"""
Clase: DataPrepEdaCnnn

Objetivo: Clase para el Eda de CNN

Cambios:
    1. Creacion de la clase
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.image import imread
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from typing import Tuple, List, Optional
import cv2


class DataPrepEdaCnn:
    """
    Clase optimizada para análisis exploratorio de datasets de imágenes.
    Diseñada específicamente para clasificación de enfermedades en plantas.
    """

    def __init__(self, directorio_base: str):
        """
        Inicializa el analizador con el directorio base del proyecto.

        Args:
            directorio_base (str): Ruta al directorio principal del proyecto
        """
        self.directorio_base = directorio_base
        self.ruta_train = None
        self.ruta_test = None
        self.forma_imagen = (256, 256, 3)
        self.tamano_lote = 16
        self.generador_imagenes = None
        self.generador_train = None
        self.generador_test = None

    def configurar_rutas(self, carpeta_train: str = "data/raw/CNN/train",
                         carpeta_test: str = "data/raw/CNN/test") -> None:
        """
        Configura las rutas de entrenamiento y prueba.

        Args:
            carpeta_train (str): Ruta relativa a la carpeta de entrenamiento
            carpeta_test (str): Ruta relativa a la carpeta de prueba
        """
        self.ruta_train = os.path.join(self.directorio_base, carpeta_train)
        self.ruta_test = os.path.join(self.directorio_base, carpeta_test)

    def listar_contenido(self, ruta: str = None) -> List[str]:
        """
        Lista el contenido de un directorio.

        Args:
            ruta (str, optional): Ruta específica. Si es None, usa directorio_base

        Returns:
            List[str]: Lista de archivos/carpetas en el directorio
        """
        if ruta is None:
            ruta = self.directorio_base
        return os.listdir(ruta)

    def obtener_clases_disponibles_entrenamiento(self) -> List[str]:
        """
        Obtiene las clases disponibles en el dataset de entrenamiento.

        Returns:
            List[str]: Lista de nombres de clases
        """
        if self.ruta_train is None:
            raise ValueError("Debe configurar las rutas primero usando configurar_rutas()")
        return self.listar_contenido(self.ruta_train)

    def obtener_clases_disponibles_pruebas(self) -> List[str]:
        """
        Obtiene las clases disponibles en el dataset de entrenamiento.

        Returns:
            List[str]: Lista de nombres de clases
        """
        if self.ruta_test is None:
            raise ValueError("Debe configurar las rutas primero usando configurar_rutas()")
        return self.listar_contenido(self.ruta_test)

    def contar_imagenes_por_clase(self, tipo_movimiento = "entrenamiento") -> dict:
        """
        Cuenta el número de imágenes en cada clase.

        Returns:
            dict: Diccionario con el conteo de imágenes por clase
        """
        if tipo_movimiento == "entrenamiento":
            clases = self.obtener_clases_disponibles_entrenamiento()
        else:
            clases = self.obtener_clases_disponibles_pruebas()

        conteos = {}

        for clase in clases:
            if tipo_movimiento == "entrenamiento":
                ruta_clase = os.path.join(self.ruta_train, clase)
            else:
                ruta_clase = os.path.join(self.ruta_test, clase)
            if os.path.isdir(ruta_clase):
                conteos[clase] = len(os.listdir(ruta_clase))

        return conteos

    def obtener_dimensiones_carpeta(self, ruta_carpeta: str) -> Tuple[List[int], List[int]]:
        """
        Obtiene las dimensiones de todas las imágenes en una carpeta.

        Args:
            ruta_carpeta (str): Ruta a la carpeta con imágenes

        Returns:
            Tuple[List[int], List[int]]: Listas con alturas y anchos
        """
        alturas = []
        anchos = []

        for archivo in os.listdir(ruta_carpeta):
            ruta_imagen = os.path.join(ruta_carpeta, archivo)
            try:
                imagen = imread(ruta_imagen)
                if imagen is not None and len(imagen.shape) >= 2:
                    altura, ancho = imagen.shape[:2]
                    alturas.append(altura)
                    anchos.append(ancho)
            except Exception:
                continue

        return alturas, anchos

    def analizar_dimensiones_por_clase(self, tipo_movimiento = "entrenamiento") -> dict:
        """
        Analiza las dimensiones de imágenes para cada clase.

        Returns:
            dict: Estadísticas de dimensiones por clase
        """
        if tipo_movimiento == "entrenamiento":
            clases = self.obtener_clases_disponibles_entrenamiento()
        else:
            clases = self.obtener_clases_disponibles_pruebas()
        estadisticas = {}

        for clase in clases:
            if tipo_movimiento == "entrenamiento":
                ruta_clase = os.path.join(self.ruta_train, clase)
            else:
                ruta_clase = os.path.join(self.ruta_test, clase)

            if os.path.isdir(ruta_clase):
                alturas, anchos = self.obtener_dimensiones_carpeta(ruta_clase)

                if alturas and anchos:
                    estadisticas[clase] = {
                        'altura_promedio': np.mean(alturas),
                        'ancho_promedio': np.mean(anchos),
                        'altura_mediana': np.median(alturas),
                        'ancho_mediana': np.median(anchos),
                        'altura_min': np.min(alturas),
                        'altura_max': np.max(alturas),
                        'ancho_min': np.min(anchos),
                        'ancho_max': np.max(anchos),
                        'total_imagenes': len(alturas)
                    }

        return estadisticas

    def graficar_dimensiones(self, ruta_carpeta: str, titulo: str = "Distribución de dimensiones") -> None:
        """
        Genera un gráfico de distribución de dimensiones para una carpeta.

        Args:
            ruta_carpeta (str): Ruta a la carpeta con imágenes
            titulo (str): Título del gráfico
        """
        alturas, anchos = self.obtener_dimensiones_carpeta(ruta_carpeta)

        if not alturas or not anchos:
            return

        plt.figure(figsize=(12, 5))

        # Gráfico de dispersión
        plt.subplot(1, 2, 1)
        plt.scatter(anchos, alturas, alpha=0.6, color='teal')
        plt.xlabel('Ancho (píxeles)')
        plt.ylabel('Altura (píxeles)')
        plt.title(f'{titulo} - Dispersión')
        plt.grid(True, alpha=0.3)

        # Histogramas
        plt.subplot(1, 2, 2)
        plt.hist(anchos, bins=30, alpha=0.7, label='Ancho', color='skyblue')
        plt.hist(alturas, bins=30, alpha=0.7, label='Altura', color='lightcoral')
        plt.xlabel('Píxeles')
        plt.ylabel('Frecuencia')
        plt.title(f'{titulo} - Histograma')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def mostrar_imagenes_muestra(self, num_imagenes: int = 3, tipo_movimiento: str = "entrenamiento") -> None:
        """
        Muestra imágenes de muestra de cada clase.

        Args:
            num_imagenes (int): Número de imágenes a mostrar por clase
            tipo_movimiento (str): tipo movimiento
        """
        if tipo_movimiento == "entrenamiento":
            clases = self.obtener_clases_disponibles_entrenamiento()
        else:
            clases = self.obtener_clases_disponibles_pruebas()

        fig, axes = plt.subplots(len(clases), num_imagenes,
                                 figsize=(num_imagenes * 4, len(clases) * 3))

        if len(clases) == 1:
            axes = [axes]

        for i, clase in enumerate(clases):
            if tipo_movimiento == "entrenamiento":
                ruta_clase = os.path.join(self.ruta_train, clase)
            else:
                ruta_clase = os.path.join(self.ruta_test, clase)
            imagenes = os.listdir(ruta_clase)[:num_imagenes]

            for j, imagen in enumerate(imagenes):
                ruta_imagen = os.path.join(ruta_clase, imagen)
                try:
                    img = imread(ruta_imagen)
                    if len(clases) == 1:
                        axes[j].imshow(img)
                        axes[j].set_title(f'{clase} - {j + 1}')
                        axes[j].axis('off')
                    else:
                        axes[i, j].imshow(img)
                        axes[i, j].set_title(f'{clase} - {j + 1}')
                        axes[i, j].axis('off')
                except Exception:
                    continue

        plt.tight_layout()
        plt.show()

    def configurar_generador_imagenes(self,
                                      rotacion_max: float = 20,
                                      desplazamiento_ancho: float = 0.10,
                                      desplazamiento_alto: float = 0.10,
                                      distorsion: float = 0.1,
                                      zoom_max: float = 0.1,
                                      giro_horizontal: bool = True) -> None:
        """
        Configura el generador de imágenes para aumento de datos.

        Args:
            rotacion_max (float): Rotación máxima en grados
            desplazamiento_ancho (float): Desplazamiento máximo en ancho
            desplazamiento_alto (float): Desplazamiento máximo en alto
            distorsion (float): Distorsión máxima
            zoom_max (float): Zoom máximo
            giro_horizontal (bool): Permitir giro horizontal
        """
        self.generador_imagenes = ImageDataGenerator(
            rotation_range=rotacion_max,
            width_shift_range=desplazamiento_ancho,
            height_shift_range=desplazamiento_alto,
            rescale=1 / 255,
            shear_range=distorsion,
            zoom_range=zoom_max,
            horizontal_flip=giro_horizontal,
            fill_mode='nearest'
        )

    def crear_generadores_datos(self, modo_clase: str = 'categorical') -> None:
        """
        Crea los generadores de datos para entrenamiento y prueba.

        Args:
            modo_clase (str): Modo de clasificación ('categorical' o 'binary')
        """
        if self.generador_imagenes is None:
            self.configurar_generador_imagenes()

        if self.ruta_train is None or self.ruta_test is None:
            raise ValueError("Debe configurar las rutas primero")

        self.generador_train = self.generador_imagenes.flow_from_directory(
            self.ruta_train,
            target_size=self.forma_imagen[:2],
            color_mode='rgb',
            batch_size=self.tamano_lote,
            class_mode=modo_clase
        )

        # Generador para test sin aumento de datos
        generador_test = ImageDataGenerator(rescale=1 / 255)

        self.generador_test = generador_test.flow_from_directory(
            self.ruta_test,
            target_size=self.forma_imagen[:2],
            color_mode='rgb',
            batch_size=self.tamano_lote,
            class_mode=modo_clase,
            shuffle=False
        )

    def obtener_indices_clases(self, tipo_movimiento = "entrenamiento") -> dict:
        """
        Obtiene los índices de las clases del generador de entrenamiento.

        Returns:
            dict: Diccionario con índices de clases
        """
        if tipo_movimiento == "entrenamiento":
            if self.generador_train is None:
                raise ValueError("Debe crear los generadores primero")
            return self.generador_train.class_indices
        else:
            if self.generador_test is None:
                raise ValueError("Debe crear los generadores primero")
            return self.generador_test.class_indices

    def configurar_forma_imagen(self, altura: int, ancho: int, canales: int = 3) -> None:
        """
        Configura la forma de las imágenes.

        Args:
            altura (int): Altura de las imágenes
            ancho (int): Ancho de las imágenes
            canales (int): Número de canales (3 para RGB)
        """
        self.forma_imagen = (altura, ancho, canales)

    def configurar_tamano_lote(self, tamano: int) -> None:
        """
        Configura el tamaño del lote para el procesamiento.

        Args:
            tamano (int): Tamaño del lote
        """
        self.tamano_lote = tamano

    def mostrar_transformacion_ejemplo(self, ruta_imagen: str, num_transformaciones: int = 4) -> None:
        """
        Muestra ejemplos de transformaciones aplicadas a una imagen.

        Args:
            ruta_imagen (str): Ruta a la imagen de ejemplo
            num_transformaciones (int): Número de transformaciones a mostrar
        """
        if self.generador_imagenes is None:
            self.configurar_generador_imagenes()

        try:
            imagen = imread(ruta_imagen)

            plt.figure(figsize=(15, 4))

            # Imagen original
            plt.subplot(1, num_transformaciones + 1, 1)
            plt.imshow(imagen)
            plt.title('Original')
            plt.axis('off')

            # Transformaciones
            for i in range(num_transformaciones):
                plt.subplot(1, num_transformaciones + 1, i + 2)
                imagen_transformada = self.generador_imagenes.random_transform(imagen)
                plt.imshow(imagen_transformada)
                plt.title(f'Transformación {i + 1}')
                plt.axis('off')

            plt.tight_layout()
            plt.show()

        except Exception as e:
            pass

    def generar_reporte_dataset(self, tipo_movimiento = "entrenamiento") -> pd.DataFrame:
        """
        Genera un reporte completo del dataset.

        Returns:
            pd.DataFrame: DataFrame con estadísticas del dataset
        """
        conteos = self.contar_imagenes_por_clase(tipo_movimiento)
        estadisticas = self.analizar_dimensiones_por_clase(tipo_movimiento)

        datos_reporte = []

        for clase in conteos.keys():
            if clase in estadisticas:
                datos_reporte.append({
                    'Clase': clase,
                    'Num_Imagenes': conteos[clase],
                    'Altura_Promedio': round(estadisticas[clase]['altura_promedio'], 1),
                    'Ancho_Promedio': round(estadisticas[clase]['ancho_promedio'], 1),
                    'Altura_Min': estadisticas[clase]['altura_min'],
                    'Altura_Max': estadisticas[clase]['altura_max'],
                    'Ancho_Min': estadisticas[clase]['ancho_min'],
                    'Ancho_Max': estadisticas[clase]['ancho_max']
                })

        return pd.DataFrame(datos_reporte)