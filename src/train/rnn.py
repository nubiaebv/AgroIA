"""
Clase: rnn_produccion

Objetivo: Clase para cargar modelo RNN entrenado y realizar predicciones a partir de archivo CSV o Excel.

Cambios:
    1. Creación de clase basada en ejemplo CNN - Fiorella, 14-07-2025
"""
# src/train/rnn.py
import os

import joblib
import numpy as np
import pandas as pd
import pickle

from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from keras.losses import MeanSquaredError
from dateutil.relativedelta import relativedelta

class rnn:
    """
    Clase para cargar modelo LSTM multivariado y realizar predicciones multistep
    de producción agrícola a partir de DataFrames.

    Cambios:
        Basada en estructura ejemplo CNN y código de predicción multistep con rolling window.
        Fiorella, 15-07-2025
    """

    def __init__(self, ruta_raiz):
        self.model = load_model(os.path.join(ruta_raiz, 'models/modelo_forecast.keras'))
        self.scaler  = joblib.load(os.path.join(ruta_raiz,'models/scaler.pkl'))
        # Diccionario invertido para obtener nombre por índice

    def obtener_prediccion(self,df: pd.DataFrame):
        # Obtener solo la fecha más reciente
        fecha_mas_reciente = pd.to_datetime(df['fecha'].max())

        # Sumar un mes a la fecha más reciente
        nueva_fecha = fecha_mas_reciente + pd.DateOffset(months=1)
        df_aux = df.copy()

        df = df[['lluvia', 'humedad', 'temperatura', 'produccion']]

        full_scaler_prediccion = MinMaxScaler()
        scaled_full_data_prediccion = full_scaler_prediccion.fit_transform(df)

        forecast = []

        periodos = 12  # Indicamos el número de periodos en base a la longitud del forecast deseada (12 meses)

        primer_batch = scaled_full_data_prediccion[-12:]
        batch_actual = primer_batch.reshape((1, 12, 4))

        for i in range(periodos):
            pred_actual = self.model.predict(batch_actual)[0]
            forecast.append(pred_actual)

            # Actualizar batch_actual de forma más simple
            batch_actual = np.roll(batch_actual, -1, axis=1)
            batch_actual[0, -1, :] = pred_actual

        forecast = np.array(forecast)

        # Extraer parámetros de la primera variable del scaler original
        min_val = self.scaler.min_[0]
        scale_val = self.scaler.scale_[0]

        # Aplicar inverse transform manualmente
        forecast_original = (forecast / scale_val) + min_val

        forecast_index_prueba = pd.date_range(start=nueva_fecha, periods=12, freq='MS')  #MS = Monthly Start
        forecast_df_prueba = pd.DataFrame(data=forecast_original, index=forecast_index_prueba,
                                          columns=['Forecast'])

        fig = self._crear_graficos_dinamicos(df_aux,forecast_df_prueba)
        return fig

    def _crear_graficos_dinamicos(self, df, forecast_df_prueba):
        """Gráficos mejorados y dinámicos"""

        # Configurar estilo moderno
        plt.style.use('seaborn-v0_8-whitegrid')

        # Crear figura más grande y atractiva
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12),
                                                     facecolor='white')

        # Colores modernos
        color_produccion = '#2E86AB'  # Azul moderno
        color_forecast = '#A23B72'  # Rosa/magenta

        # 1. Gráfico de Producción con área rellena
        ax1.fill_between(range(len(df)), df['produccion'], alpha=0.3, color=color_produccion)
        ax1.plot(df['produccion'], linewidth=3, color=color_produccion,
                 marker='o', markersize=8, markerfacecolor='white',
                 markeredgecolor=color_produccion, markeredgewidth=2)
        ax1.set_title('📈 Producción Histórica', fontsize=16, fontweight='bold', pad=20)
        ax1.set_xlabel('Período', fontweight='bold')
        ax1.set_ylabel('Producción (toneladas)', fontweight='bold')
        ax1.grid(True, alpha=0.3, linestyle='--')

        # Añadir estadísticas
        media = df['produccion'].mean()
        ax1.axhline(y=media, color='red', linestyle='--', alpha=0.7, linewidth=2)
        ax1.text(0.02, 0.98, f'📊 Promedio: {media:.1f}', transform=ax1.transAxes,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # 2. Gráfico de Forecast mejorado
        x_forecast = range(len(forecast_df_prueba))
        y_forecast = forecast_df_prueba['Forecast'].values

        ax2.fill_between(x_forecast, y_forecast, alpha=0.4, color=color_forecast)
        ax2.plot(x_forecast, y_forecast, linewidth=3, color=color_forecast,
                 marker='s', markersize=8, markerfacecolor='white',
                 markeredgecolor=color_forecast, markeredgewidth=2)

        ax2.set_title('🔮 Predicción Futura', fontsize=16, fontweight='bold', pad=20)
        ax2.set_xlabel('Meses Futuros', fontweight='bold')
        ax2.set_ylabel('Producción Predicha (toneladas)', fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--')

        # Etiquetas de meses
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        ax2.set_xticks(range(len(forecast_df_prueba)))
        ax2.set_xticklabels(meses[:len(forecast_df_prueba)], rotation=45)

        # 3. Gráfico con tendencia
        ax3.fill_between(range(len(df)), df['produccion'], alpha=0.3, color=color_produccion)
        ax3.plot(df['produccion'], linewidth=3, color=color_produccion,
                 marker='o', markersize=8, markerfacecolor='white',
                 markeredgecolor=color_produccion, markeredgewidth=2)
        ax3.set_title('📊 Producción Histórica (Copia)', fontsize=16, fontweight='bold', pad=20)
        ax3.set_xlabel('Período', fontweight='bold')
        ax3.set_ylabel('Producción (toneladas)', fontweight='bold')
        ax3.grid(True, alpha=0.3, linestyle='--')

        # 4. Gráfico combinado mejorado
        # Datos históricos
        x_hist = range(len(df))
        ax4.fill_between(x_hist, df['produccion'], alpha=0.3, color=color_produccion, label='Histórico')
        ax4.plot(x_hist, df['produccion'], linewidth=3, color=color_produccion,
                 marker='o', markersize=8, markerfacecolor='white',
                 markeredgecolor=color_produccion, markeredgewidth=2)

        # Datos de predicción
        x_pred = range(len(df), len(df) + len(forecast_df_prueba))
        ax4.fill_between(x_pred, y_forecast, alpha=0.4, color=color_forecast, label='Predicción')
        ax4.plot(x_pred, y_forecast, linewidth=3, color=color_forecast,
                 marker='s', markersize=8, markerfacecolor='white',
                 markeredgecolor=color_forecast, markeredgewidth=2)

        # Línea de conexión
        ax4.plot([len(df) - 1, len(df)], [df['produccion'].iloc[-1], y_forecast[0]],
                 color='gray', linestyle=':', linewidth=2, alpha=0.7)

        ax4.set_title('🔄 Histórico vs Predicción', fontsize=16, fontweight='bold', pad=20)
        ax4.set_xlabel('Período Total', fontweight='bold')
        ax4.set_ylabel('Producción (toneladas)', fontweight='bold')
        ax4.grid(True, alpha=0.3, linestyle='--')
        ax4.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)

        # Línea vertical para separar histórico de predicción
        ax4.axvline(x=len(df) - 0.5, color='red', linestyle='--', alpha=0.5, linewidth=2)
        ax4.text(len(df) - 0.5, ax4.get_ylim()[1] * 0.9, 'Inicio Predicción',
                 rotation=90, verticalalignment='top', horizontalalignment='right',
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

        # Mejorar aspecto general
        for ax in [ax1, ax2, ax3, ax4]:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_linewidth(0.5)
            ax.spines['bottom'].set_linewidth(0.5)

        fig.suptitle('🚀 Dashboard de Predicción de Producción de Papa',
                     fontsize=20, fontweight='bold', y=0.98)

        plt.tight_layout()
        return fig

    def obtener_prediccion_api(self,df: pd.DataFrame):
        # Obtener solo la fecha más reciente
        fecha_mas_reciente = pd.to_datetime(df['fecha'].max())

        # Sumar un mes a la fecha más reciente
        nueva_fecha = fecha_mas_reciente + pd.DateOffset(months=1)
        df_aux = df.copy()

        df = df[['lluvia', 'humedad', 'temperatura', 'produccion']]

        full_scaler_prediccion = MinMaxScaler()
        scaled_full_data_prediccion = full_scaler_prediccion.fit_transform(df)

        forecast = []

        periodos = 12  # Indicamos el número de periodos en base a la longitud del forecast deseada (12 meses)

        primer_batch = scaled_full_data_prediccion[-12:]
        batch_actual = primer_batch.reshape((1, 12, 4))

        for i in range(periodos):
            pred_actual = self.model.predict(batch_actual)[0]
            forecast.append(pred_actual)

            # Actualizar batch_actual de forma más simple
            batch_actual = np.roll(batch_actual, -1, axis=1)
            batch_actual[0, -1, :] = pred_actual

        forecast = np.array(forecast)

        # Extraer parámetros de la primera variable del scaler original
        min_val = self.scaler.min_[0]
        scale_val = self.scaler.scale_[0]

        # Aplicar inverse transform manualmente
        forecast_original = (forecast / scale_val) + min_val

        forecast_index_prueba = pd.date_range(start=nueva_fecha, periods=12, freq='MS')  #MS = Monthly Start
        forecast_df_prueba = pd.DataFrame(data=forecast_original, index=forecast_index_prueba,
                                          columns=['Forecast'])


        return forecast_df_prueba

