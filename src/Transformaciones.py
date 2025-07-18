
class Transformaciones:

    def recomendacion_num(self, df):
        try:
            mapeo = {
                'riego': 1,
                'fertilizacion': 2,
                'poda_preventiva': 3
            }
            df['Recomendacion'] = df['Recomendacion'].map(mapeo)
            return df
        except KeyError as e:
            print(f"Error: Columna 'Recomendacion' no encontrada - {e}")
            raise
        except Exception as e:
            print(f"Error transformando recomendaciones: {e}")
            raise