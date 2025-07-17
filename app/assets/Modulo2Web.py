import streamlit as st
import pandas as pd
from src.train.rnn import rnn
from src.utils.metrics import obtener_ruta_app

class Modulo2Web:
    def __init__(self):
        self.modelo_rnn = rnn(obtener_ruta_app("AgroIA"))

    def render(self):
        global df
        st.set_page_config(page_title="Predicción de Producción", layout="centered")
        st.title("Predicción de Producción de Papa")
        archivo = st.file_uploader("Sube un archivo .csv o .xlsx", type=["csv", "xlsx"])

        if archivo:
            try:
                if archivo.name.endswith(".csv"):
                    df = pd.read_csv(archivo)
                else:
                    df = pd.read_excel(archivo)

                st.write("Vista previa del archivo:")
                st.dataframe(df)

            except Exception as e:
                st.error(f" Error: {e}")
        # Botón para generar recomendación
        if st.button('Obtener Recomendación'):
            try:
                fig = self.modelo_rnn.obtener_prediccion(df)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error: {str(e)}")