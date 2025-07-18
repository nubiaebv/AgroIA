
#%%
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


#%%


class MetodosEDARNN:
    def __init__(self, df: pd.DataFrame, base_path_func=None, proyecto=None):
        self.df = df.copy()
        self.base_path_func = base_path_func
        self.proyecto = proyecto
        self.scaler = MinMaxScaler()
        self.meses_es_en = {

            'enero': 'January', 'febrero': 'February', 'marzo': 'March',
            'abril': 'April', 'mayo': 'May', 'junio': 'June',
            'julio': 'July', 'agosto': 'August', 'septiembre': 'September',
            'octubre': 'October', 'noviembre': 'November', 'diciembre': 'December'
        }


    def transformar_fechas(self):

            self.df['mes_en'] = self.df['mes'].str.lower().map(self.meses_es_en)
            self.df['fecha'] = pd.to_datetime(
                self.df['mes_en'] + ' ' + self.df['anio'].astype(str), format='%B %Y'
            )
            self.df.drop(columns=['mes', 'anio', 'mes_en'], inplace=True)

    def preparar_categorica(self, columna: str):
        try:
            self.df[f'{columna}_id'] = self.df[columna].astype('category').cat.codes
            num_categorias = self.df[f'{columna}_id'].nunique()
            self.df.drop(columns=[columna], inplace=True)
            return num_categorias
        except Exception as e:
            raise

    def normalizar_columnas(self, columnas: list):
        try:
            self.df[columnas] = self.scaler.fit_transform(self.df[columnas])
        except Exception as e:
            raise

    def validar_cobertura(self, fecha_inicio: str = '2005-01-01', fecha_fin: str = '2025-05-01') -> pd.DataFrame:
        try:
            fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='MS')
            cantones = self.df['canton'].unique()
            combinaciones = pd.MultiIndex.from_product([cantones, fechas], names=['canton', 'fecha']).to_frame(index=False)
            self.df['fecha'] = self.df['fecha'].dt.to_period('M').dt.to_timestamp()
            df_existente = self.df[['canton', 'fecha']].drop_duplicates()
            faltantes = combinaciones.merge(df_existente, on=['canton', 'fecha'], how='left', indicator=True)
            faltantes = faltantes[faltantes['_merge'] == 'left_only'].drop(columns=['_merge'])

            return faltantes
        except Exception as e:
            raise

    def graficar_densidad(self, columna: str, color: str = '#1F4E79'):
        try:
            plt.figure(figsize=(10, 3))
            sns.kdeplot(self.df[columna], fill=True, color=color, alpha=0.6)
            plt.title(f'Distribución de la variable {columna.capitalize()}', fontsize=16)
            plt.xlabel(columna, fontsize=12)
            plt.ylabel('Densidad', fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            raise

    def guardar_csv(self, subcarpetas: list, nombre_archivo: str) -> str:
        if self.base_path_func is None or self.proyecto is None:
            raise ValueError("base_path_func y proyecto deben estar definidos para guardar CSV.")
        try:
            base_path = self.base_path_func(self.proyecto)
            ruta_completa = os.path.join(base_path, *subcarpetas)
            os.makedirs(ruta_completa, exist_ok=True)
            file_path = os.path.join(ruta_completa, nombre_archivo)
            self.df.to_csv(file_path, index=False)
            return file_path
        except Exception as e:
            raise

    def obtener_df(self) -> pd.DataFrame:
        return self.df
