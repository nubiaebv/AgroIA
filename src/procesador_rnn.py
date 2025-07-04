
"""Clase: ProcesadorDatosPapa: Clase para limpiar los datos de la fuente original, el resultado es
    un dataset largo con los datos de produccion de papa en toneladas y area sembrada por cantón, año y mes.
	Cambios:    1. Creacion de la clase by Fiorella y Gilary 	2-07-2025"""
import pandas as pd


class ProcesadorDatosPapa:
    def __init__(self, archivo_excel):
        """
        Inicializa el procesador con la ruta del archivo Excel.

        Args:
            archivo_excel (str): Ruta completa al archivo Excel
        """
        self.archivo = archivo_excel
        self.nombres_interes = ['Turrialba', 'Oreamuno', 'El Guarco', 'Cartago', 'Alvarado']
        self.meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                      'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        self.df_largo = None

    def procesar_a_formato_largo(self):
        """
        Procesa el archivo Excel directamente al formato largo.
        """
        xls = pd.ExcelFile(self.archivo)
        hojas = xls.sheet_names

        datos = []

        for hoja in hojas:
            # Leer hoja con encabezado en fila 6 (index=5)
            df = pd.read_excel(self.archivo, sheet_name=hoja, header=5)

            # Nombre de la primera columna (cantones)
            nombre_columna_a = df.columns[0]

            # Filtrar filas por cantones de interés
            df_filtrado = df[df[nombre_columna_a].isin(self.nombres_interes)].copy()

            # Armar lista de nuevos nombres:
            # La primera columna es 'canton'
            nuevos_nombres = ['canton']
            for mes in self.meses:
                nuevos_nombres.append(f'{mes}_produccion')
                nuevos_nombres.append(f'{mes}_area')

            # Cortar el DataFrame para que solo tenga la cantidad correcta de columnas (1 + 12*2 = 25)
            df_filtrado = df_filtrado.iloc[:, :len(nuevos_nombres)]

            # Asignar nuevos nombres a columnas
            df_filtrado.columns = nuevos_nombres

            # Transformar directamente a formato largo para esta hoja
            for _, fila in df_filtrado.iterrows():
                for mes in self.meses:
                    datos.append({
                        'canton': fila['canton'],
                        'mes': mes,
                        'anio': hoja,
                        'produccion': fila[f'{mes}_produccion'],
                        'area': fila[f'{mes}_area']
                    })

        # Crear el DataFrame en formato largo
        self.df_largo = pd.DataFrame(datos)

    def exportar_csv(self, ruta_csv):
        """
        Exporta los datos en formato largo a un archivo CSV.

        Args:
            ruta_csv (str): Ruta donde guardar el archivo CSV
        """
        if self.df_largo is None:
            raise ValueError("Primero debe procesar los datos usando procesar_a_formato_largo()")

        self.df_largo.to_csv(ruta_csv, index=False)
        print(f"Archivo CSV guardado en: {ruta_csv}")


    def procesar_y_exportar(self, ruta_csv):
        """
        Ejecuta todo el proceso: procesar Excel a formato largo y exportar.

        Args:
            ruta_csv (str): Ruta para guardar el archivo CSV
        """
        self.procesar_a_formato_largo()
        self.exportar_csv(ruta_csv)


