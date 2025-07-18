import pandas as pd
import os

class RecomendadorClimatico:
    def __init__(self, archivo_entrada, archivo_salida):
        self.archivo_entrada = archivo_entrada
        self.archivo_salida = archivo_salida
        self.df = None
        self.merged = None

    def cargar_datos(self):
        try:
            self.df = pd.read_csv(self.archivo_entrada)
        except FileNotFoundError:
            print(f"Error: El archivo {self.archivo_entrada} no existe")
            raise
        except pd.errors.EmptyDataError:
            print(f"Error: El archivo {self.archivo_entrada} está vacío")
            raise
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            raise

    def transformar_datos(self):
        try:
            # Separar por parámetro
            lluvia = self.df[self.df["PARAMETER"] == "PRECTOTCORR"]
            temp_max = self.df[self.df["PARAMETER"] == "T2M_MAX"]
            temp_min = self.df[self.df["PARAMETER"] == "T2M_MIN"]
            humedad = self.df[self.df["PARAMETER"] == "RH2M"]

            meses = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                     "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

            # Convertir a formato largo
            lluvia_long = lluvia.melt(id_vars=["YEAR"], value_vars=meses, var_name="MONTH", value_name="lluvia_mm")
            temp_max_long = temp_max.melt(id_vars=["YEAR"], value_vars=meses, var_name="MONTH", value_name="temp_max")
            temp_min_long = temp_min.melt(id_vars=["YEAR"], value_vars=meses, var_name="MONTH", value_name="temp_min")
            humedad_long = humedad.melt(id_vars=["YEAR"], value_vars=meses, var_name="MONTH", value_name="humedad")

            # pH del suelo
            try:
                ph_cols = [col for col in self.df.columns if "PH_SUELO" in col]
                ph_df = lluvia[["YEAR"] + ph_cols].copy()
                ph_long = ph_df.melt(id_vars=["YEAR"], var_name="MONTH", value_name="ph_suelo")
                ph_long["MONTH"] = ph_long["MONTH"].str.extract(r'(\w+)_PH_SUELO')
            except Exception as e:
                print(f"Error procesando pH del suelo: {e}")
                # Crear DataFrame con pH neutro por defecto
                ph_long = lluvia_long[["YEAR", "MONTH"]].copy()
                ph_long["ph_suelo"] = 7.0

            # Unir todos
            self.merged = lluvia_long.merge(temp_max_long, on=["YEAR", "MONTH"])
            self.merged = self.merged.merge(temp_min_long, on=["YEAR", "MONTH"])
            self.merged = self.merged.merge(humedad_long, on=["YEAR", "MONTH"])
            self.merged = self.merged.merge(ph_long, on=["YEAR", "MONTH"])

        except KeyError as e:
            print(f"Error: Columna faltante - {e}")
            raise
        except Exception as e:
            print(f"Error durante la transformación: {e}")
            raise

    def generar_recomendacion(self, row):
        try:
            # Prioridad: riego > fertilización > poda preventiva > ninguna
            if row["lluvia_mm"] < 8 and row["temp_max"] > 27:
                return "riego"
            elif row["ph_suelo"] < 6:
                return "fertilizacion"
            elif row["humedad"] > 87 and row["temp_max"] > 24:
                return "poda_preventiva"
            else:
                return "riego"
        except Exception as e:
            print(f"Error generando recomendación: {e}")
            return "ninguna"

    def aplicar_recomendaciones(self):
        try:
            self.merged["Recomendacion"] = self.merged.apply(self.generar_recomendacion, axis=1)
        except Exception as e:
            print(f"Error aplicando recomendaciones: {e}")
            raise

    def exportar_resultado(self):
        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(self.archivo_salida)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)

            columnas_finales = ["YEAR", "MONTH", "lluvia_mm", "temp_max", "temp_min", "humedad", "ph_suelo", "Recomendacion"]
            self.merged[columnas_finales].to_csv(self.archivo_salida, index=False)
        except PermissionError:
            print(f"Error: Sin permisos para escribir el archivo {self.archivo_salida}")
            raise
        except Exception as e:
            print(f"Error exportando resultado: {e}")
            raise

    def procesar(self):
        try:
            self.cargar_datos()
            self.transformar_datos()
            self.aplicar_recomendaciones()
            self.exportar_resultado()
            print(f"✅ Archivo generado: {self.archivo_salida}")
        except Exception as e:
            print(f"❌ Error en el procesamiento: {e}")
            raise


# Uso de la clase:
# recomendador = RecomendadorClimatico("df_con_ph.csv", "datos_con_recomendaciones_completo.csv")
# recomendador.procesar()