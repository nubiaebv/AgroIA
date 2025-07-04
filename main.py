from src.procesador_rnn import ProcesadorDatosPapa

if __name__ == "__main__":
    # Crear instancia del procesador
    archivo = "data/raw/ESTIM_papa_2005-2025 (1).xls"
    procesador = ProcesadorDatosPapa(archivo)

    # Procesar directamente a formato largo y exportar
    procesador.procesar_y_exportar("data/processed/datos_transformados.csv")
