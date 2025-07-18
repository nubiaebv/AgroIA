# AgroIA
Sistema integrado basado en CNN, RNN y ANN para:
1. Detectar enfermedades en hojas de cultivo.
2. Predecir rendimiento con series temporales climáticas.
3. Recomendar acciones agronómicas.


Desarrollado utilizando la herramienta PyCharm (logica) y Streamlit (UI)
Versión de Python 3.11
Para ejcutar la aplicación ejecutar el comando: streamlit run main.py

# Estructura del proyecto 

api --> Contiene lo necesario para utilizar los modelos mediante un API (localhost:8000/docs)
app --> Contiene los archivos con la UI de cada uno de los modulos descritos al inicio de este documento
data --> Contiene los datos "crudos" (raw) y los datos ya procesados (processed) que fueron utilizados para la creación de cada uno de los modelos
models --> Contiene los archivos en .h5, con los 3 diferentes modelos
notebooks --> Contiene los archivos con el EDA que se realizo en cada modulo 
src --> Contiene todas las clases utilizadas para el desarrollo de los modelos y en la carpeta "train" se encuentran los archivos en donde se desarrollaron los modelos.
main.py

# Desarrolladores:

1 - Evelin Calderón Rojas
2 - Nubia Brenes Valerin
3 - Gilary Granados Calvo
4 - Fiorella Abarca Valverde
5 - Mariel Rodríguez Arguello
6 - Roberto Montoya Leiva
7 - Pablo Marín Castillo
8 - Alejandro Quesada Leiva