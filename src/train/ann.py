import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import os


class ann:
    def __init__(self, ruta_raiz):
        try:
            self.model = load_model(os.path.join(ruta_raiz, 'models/modelo_pred_cultivopapa.h5'))
            # Inicializar el escalador
            self.escalador = MinMaxScaler()
            self.is_fitted = False
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No se encontró el archivo del modelo en la ruta: {os.path.join(ruta_raiz, 'models/modelo_pred_cultivopapa.h5')}")
        except Exception as e:
            raise Exception(f"Error al cargar el modelo: {str(e)}")

    def generar_prediccion(self, df_pred):
        """
        Genera predicciones para los datos de entrada

        Args:
            df_pred (pd.DataFrame): DataFrame con los datos para predecir
                                   Debe contener las columnas: ['lluvia_mm', 'temp_max', 'temp_min', 'humedad', 'ph_suelo']

        Returns:
            pd.DataFrame: DataFrame original con columnas adicionales de predicción
        """
        try:
            # Validar que el DataFrame tenga las columnas necesarias
            columnas_necesarias = ['lluvia_mm', 'temp_max', 'temp_min', 'humedad', 'ph_suelo']
            columnas_faltantes = [col for col in columnas_necesarias if col not in df_pred.columns]

            if columnas_faltantes:
                raise ValueError(f"Faltan las siguientes columnas: {columnas_faltantes}")

            # Validar que el DataFrame no esté vacío
            if df_pred.empty:
                raise ValueError("El DataFrame no puede estar vacío")

            # Crear una copia del DataFrame para no modificar el original
            df_resultado = df_pred.copy()

            # Preparar los datos para la predicción
            X_pred = df_pred[columnas_necesarias].copy()

            # Verificar valores nulos
            if X_pred.isnull().any().any():
                raise ValueError("Los datos contienen valores nulos")

            # Normalizar los datos
            try:
                if not self.is_fitted:
                    # Si es la primera vez, ajustar y transformar
                    X_pred_scaled = self.escalador.fit_transform(X_pred)
                    self.is_fitted = True
                else:
                    # Si ya está ajustado, solo transformar
                    X_pred_scaled = self.escalador.transform(X_pred)
            except Exception as e:
                raise Exception(f"Error al escalar los datos: {str(e)}")

            # Realizar predicción
            try:
                predicciones_raw = self.model.predict(X_pred_scaled)
                resultado_indices = np.argmax(predicciones_raw, axis=-1)
            except Exception as e:
                raise Exception(f"Error al generar predicciones: {str(e)}")

            # Obtener las probabilidades máximas para cada predicción
            try:
                probabilidades = np.max(predicciones_raw, axis=-1)

                # Mapear índices a recomendaciones
                mapeo_recomendaciones = {
                    0: 'riego',
                    1: 'fertilizacion',
                    2: 'poda_preventiva'
                }

                # Agregar las predicciones al DataFrame resultado
                df_resultado['indice'] = resultado_indices
                df_resultado['probabilidad_porcentaje'] = probabilidades
                df_resultado['prediccion'] = [mapeo_recomendaciones.get(idx, 'desconocido') for idx in
                                              resultado_indices]

                return df_resultado
            except Exception as e:
                raise Exception(f"Error al procesar las predicciones: {str(e)}")

        except ValueError as e:
            raise ValueError(f"Error de validación en generar_prediccion: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado en generar_prediccion: {str(e)}")

    def recomendacion_num(self, df):
        """
        Convierte las recomendaciones de texto a números

        Args:
            df (pd.DataFrame): DataFrame con columna 'Recomendacion'

        Returns:
            pd.DataFrame: DataFrame con recomendaciones convertidas a números
        """
        try:
            mapeo = {
                'riego': 1,
                'fertilizacion': 2,
                'poda_preventiva': 3
            }
            df_resultado = df.copy()
            df_resultado['Recomendacion'] = df_resultado['Recomendacion'].map(mapeo)
            return df_resultado
        except KeyError as e:
            print(f"Error: Columna 'Recomendacion' no encontrada - {e}")
            raise
        except Exception as e:
            print(f"Error transformando recomendaciones: {e}")
            raise

    def predecir_desde_fila(self, fila_datos):
        """
        Método específico para predecir desde un diccionario de datos (ideal para Streamlit)

        Args:
            fila_datos (dict): Diccionario con los datos de entrada

        Returns:
            dict: Diccionario con la predicción y información adicional
        """
        try:
            # Validar entrada
            if not isinstance(fila_datos, dict):
                raise ValueError("fila_datos debe ser un diccionario")

            if not fila_datos:
                raise ValueError("El diccionario de datos no puede estar vacío")

            # Convertir el diccionario a DataFrame
            try:
                df_entrada = pd.DataFrame([fila_datos])
            except Exception as e:
                raise Exception(f"Error al convertir fila_datos a DataFrame: {str(e)}")

            # Generar predicción
            resultado = self.generar_prediccion(df_entrada)

            # Extraer información relevante
            try:
                prediccion_info = {
                    'indice': resultado['indice'].iloc[0],
                    'probabilidad_porcentaje': round(resultado['probabilidad_porcentaje'].iloc[0] * 100, 2),
                    'prediccion': resultado['prediccion'].iloc[0]

                }

                return prediccion_info
            except KeyError as e:
                raise KeyError(f"Error al acceder a la columna de predicción: {str(e)}")
            except Exception as e:
                raise Exception(f"Error al procesar la información de predicción: {str(e)}")

        except ValueError as e:
            raise ValueError(f"Error de validación en predecir_desde_fila: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado en predecir_desde_fila: {str(e)}")