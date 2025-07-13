"""
Pipeline EDA Automatizado - Réplica exacta del Jupyter Notebook
Este script replica todo el flujo del notebook EDA_CNN.ipynb de manera automatizada.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')


class PipelineEDA:
    """
    Pipeline que replica exactamente el flujo del Jupyter Notebook EDA_CNN.ipynb
    """

    def __init__(self, directorio_proyecto="AgroIA", mostrar_graficos=False):
        """
        Inicializa el pipeline EDA.

        Args:
            directorio_proyecto: Nombre del directorio del proyecto
            mostrar_graficos: Si mostrar los gráficos (False para ejecución silenciosa)
        """
        self.directorio_proyecto = directorio_proyecto
        self.mostrar_graficos = mostrar_graficos
        self.analizador = None
        self.clases = None
        self.conteos_train = None
        self.conteos_test = None
        self.configurado = False

    def ejecutar_eda_completo(self):
        """
        Ejecuta todo el EDA siguiendo exactamente el flujo del notebook.
        Retorna el analizador configurado y listo para usar.
        """
        print("🚀 Iniciando Pipeline EDA Automatizado")
        print("=" * 50)

        # Paso 1: Importaciones y configuración inicial
        self._paso_1_importaciones()

        # Paso 2: Inicializar el analizador
        self._paso_2_inicializar_analizador()

        # Paso 3: Configurar rutas y explorar estructura
        self._paso_3_configurar_rutas()

        # Paso 4: Análisis cuantitativo del dataset
        self._paso_4_analisis_cuantitativo()

        # Paso 5: Análisis de dimensiones
        self._paso_5_analisis_dimensiones()

        # Paso 6: Generar reporte completo
        self._paso_6_generar_reporte()

        # Paso 7: Visualizaciones (opcional)
        if self.mostrar_graficos:
            self._paso_7_visualizaciones()

        # Paso 8: Mostrar imágenes de muestra (opcional)
        if self.mostrar_graficos:
            self._paso_8_mostrar_muestras()

        # Paso 9: Configuración del procesamiento
        self._paso_9_configurar_procesamiento()

        # Paso 10: Configurar generador con aumento de datos
        self._paso_10_configurar_generador()

        # Paso 11: Crear generadores de datos
        self._paso_11_crear_generadores()

        # Paso 12: Mostrar índices de clases
        self._paso_12_mostrar_indices()

        # Paso 13: Transformaciones de ejemplo (opcional)
        if self.mostrar_graficos:
            self._paso_13_transformaciones_ejemplo()

        # Paso 14: Resumen final
        self._paso_14_resumen_final()

        self.configurado = True
        print("\n✅ Pipeline EDA completado exitosamente")
        return self.analizador

    def _paso_1_importaciones(self):
        """Paso 1: Importaciones y configuración inicial"""
        print("📦 Paso 1: Importaciones y configuración inicial")

        # Configurar matplotlib
        plt.rcParams['figure.figsize'] = (10, 6)

        print("✅ Librerías importadas correctamente")

    def _paso_2_inicializar_analizador(self):
        """Paso 2: Inicializar el analizador"""
        print("🔧 Paso 2: Inicializar el analizador")

        # Importar clases necesarias
        from src.DataPrepEdaCnn import DataPrepEdaCnn as AnalizadorImagenes
        from src.utils.metrics import obtener_ruta_app

        # Configurar la ruta del proyecto
        directorio_proyecto = obtener_ruta_app(self.directorio_proyecto)

        # Crear instancia del analizador
        self.analizador = AnalizadorImagenes(directorio_proyecto)

        print(f"✅ Analizador inicializado con directorio: {directorio_proyecto}")

    def _paso_3_configurar_rutas(self):
        """Paso 3: Configurar rutas y explorar estructura"""
        print("📁 Paso 3: Configurar rutas y explorar estructura")

        # Configurar rutas de train y test
        self.analizador.configurar_rutas()

        print("📁 Contenido del directorio principal:")
        contenido_principal = self.analizador.listar_contenido()
        for item in contenido_principal:
            print(f"  - {item}")

        # Obtener clases disponibles
        print("\n🏷️ Clases disponibles en el dataset entrenamiento:")
        clases_train = self.analizador.obtener_clases_disponibles_entrenamiento()
        for i, clase in enumerate(clases_train, 1):
            print(f"  {i}. {clase}")

        print("\n🏷️ Clases disponibles en el dataset pruebas:")
        clases_test = self.analizador.obtener_clases_disponibles_pruebas()
        for i, clase in enumerate(clases_test, 1):
            print(f"  {i}. {clase}")

        self.clases = clases_train

    def _paso_4_analisis_cuantitativo(self):
        """Paso 4: Análisis cuantitativo del dataset"""
        print("\n📊 Paso 4: Análisis cuantitativo del dataset")

        # Contar imágenes por clase - entrenamiento
        self.conteos_train = self.analizador.contar_imagenes_por_clase("entrenamiento")

        print("📊 Distribución de imágenes entrenamiento por clase:")
        total_imagenes_train = 0
        for clase, cantidad in self.conteos_train.items():
            print(f"  {clase}: {cantidad:,} imágenes")
            total_imagenes_train += cantidad

        print(f"\n📈 Total de imágenes entrenamiento: {total_imagenes_train:,}")

        # Contar imágenes por clase - pruebas
        self.conteos_test = self.analizador.contar_imagenes_por_clase("pruebas")

        print("\n📊 Distribución de imágenes pruebas por clase:")
        total_imagenes_test = 0
        for clase, cantidad in self.conteos_test.items():
            print(f"  {clase}: {cantidad:,} imágenes")
            total_imagenes_test += cantidad

        print(f"\n📈 Total de imágenes pruebas: {total_imagenes_test:,}")

        # Crear gráficos si está habilitado
        if self.mostrar_graficos:
            self._crear_graficos_distribucion()

    def _crear_graficos_distribucion(self):
        """Crear gráficos de distribución"""
        # Gráfico entrenamiento
        plt.figure(figsize=(10, 6))
        clases_nombres = list(self.conteos_train.keys())
        cantidades = list(self.conteos_train.values())

        bars = plt.bar(clases_nombres, cantidades, color=['#2E8B57', '#FF6B6B', '#4ECDC4'])
        plt.title('Distribución de Imágenes por Clase - Entrenamiento', fontsize=16, fontweight='bold')
        plt.xlabel('Clases', fontsize=12)
        plt.ylabel('Número de Imágenes', fontsize=12)
        plt.xticks(rotation=45, ha='right')

        for bar, cantidad in zip(bars, cantidades):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                     f'{cantidad:,}', ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        plt.grid(axis='y', alpha=0.3)
        plt.show()

        # Gráfico pruebas
        plt.figure(figsize=(10, 6))
        cantidades_test = list(self.conteos_test.values())

        bars = plt.bar(clases_nombres, cantidades_test, color=['#2E8B57', '#FF6B6B', '#4ECDC4'])
        plt.title('Distribución de Imágenes por Clase - Pruebas', fontsize=16, fontweight='bold')
        plt.xlabel('Clases', fontsize=12)
        plt.ylabel('Número de Imágenes', fontsize=12)
        plt.xticks(rotation=45, ha='right')

        for bar, cantidad in zip(bars, cantidades_test):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                     f'{cantidad:,}', ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        plt.grid(axis='y', alpha=0.3)
        plt.show()

    def _paso_5_analisis_dimensiones(self):
        """Paso 5: Análisis de dimensiones"""
        print("\n📏 Paso 5: Análisis de dimensiones de las imágenes")

        # Analizar dimensiones entrenamiento
        estadisticas_dim_train = self.analizador.analizar_dimensiones_por_clase("entrenamiento")

        print("📏 Estadísticas de dimensiones por clase para entrenamiento:\n")
        for clase, stats in estadisticas_dim_train.items():
            print(f"🔍 {clase.upper()}:")
            print(f"  • Altura promedio: {stats['altura_promedio']:.1f} px")
            print(f"  • Ancho promedio: {stats['ancho_promedio']:.1f} px")
            print(f"  • Rango altura: {stats['altura_min']} - {stats['altura_max']} px")
            print(f"  • Rango ancho: {stats['ancho_min']} - {stats['ancho_max']} px")
            print(f"  • Total imágenes analizadas: {stats['total_imagenes']}")
            print()

        # Analizar dimensiones pruebas
        estadisticas_dim_test = self.analizador.analizar_dimensiones_por_clase("pruebas")

        print("📏 Estadísticas de dimensiones por clase para pruebas:\n")
        for clase, stats in estadisticas_dim_test.items():
            print(f"🔍 {clase.upper()}:")
            print(f"  • Altura promedio: {stats['altura_promedio']:.1f} px")
            print(f"  • Ancho promedio: {stats['ancho_promedio']:.1f} px")
            print(f"  • Rango altura: {stats['altura_min']} - {stats['altura_max']} px")
            print(f"  • Rango ancho: {stats['ancho_min']} - {stats['ancho_max']} px")
            print(f"  • Total imágenes analizadas: {stats['total_imagenes']}")
            print()

    def _paso_6_generar_reporte(self):
        """Paso 6: Generar reporte completo"""
        print("📋 Paso 6: Generar reporte completo del dataset")

        # Reporte entrenamiento
        reporte_df_train = self.analizador.generar_reporte_dataset("entrenamiento")

        print("📋 Reporte completo del dataset entrenamiento:")
        print(reporte_df_train.to_string(index=False))

        print("\n📊 Resumen estadístico entrenamiento:")
        print(f"  • Altura promedio general: {reporte_df_train['Altura_Promedio'].mean():.1f} px")
        print(f"  • Ancho promedio general: {reporte_df_train['Ancho_Promedio'].mean():.1f} px")
        print(f"  • Total de clases: {len(reporte_df_train)}")
        print(f"  • Total de imágenes: {reporte_df_train['Num_Imagenes'].sum():,}")

        # Reporte pruebas
        reporte_df_test = self.analizador.generar_reporte_dataset("pruebas")

        print("\n📋 Reporte completo del dataset pruebas:")
        print(reporte_df_test.to_string(index=False))

        print("\n📊 Resumen estadístico pruebas:")
        print(f"  • Altura promedio general: {reporte_df_test['Altura_Promedio'].mean():.1f} px")
        print(f"  • Ancho promedio general: {reporte_df_test['Ancho_Promedio'].mean():.1f} px")
        print(f"  • Total de clases: {len(reporte_df_test)}")
        print(f"  • Total de imágenes: {reporte_df_test['Num_Imagenes'].sum():,}")

    def _paso_7_visualizaciones(self):
        """Paso 7: Visualización de distribuciones de dimensiones"""
        print("\n📊 Paso 7: Visualización de distribuciones de dimensiones")

        # Graficar distribuciones para entrenamiento
        for clase in self.clases:
            ruta_clase = os.path.join(self.analizador.ruta_train, clase)
            titulo = f"Distribución de dimensiones entrenamiento - {clase.replace('_', ' ').title()}"
            self.analizador.graficar_dimensiones(ruta_clase, titulo)

        # Graficar distribuciones para pruebas
        for clase in self.clases:
            ruta_clase = os.path.join(self.analizador.ruta_test, clase)
            titulo = f"Distribución de dimensiones pruebas - {clase.replace('_', ' ').title()}"
            self.analizador.graficar_dimensiones(ruta_clase, titulo)

    def _paso_8_mostrar_muestras(self):
        """Paso 8: Mostrar imágenes de muestra"""
        print("\n🖼️ Paso 8: Mostrar imágenes de muestra")

        print("🖼️ Imágenes de muestra por clase para entrenamiento:")
        self.analizador.mostrar_imagenes_muestra(num_imagenes=4, tipo_movimiento="entrenamiento")

        print("🖼️ Imágenes de muestra por clase para pruebas:")
        self.analizador.mostrar_imagenes_muestra(4, "pruebas")

    def _paso_9_configurar_procesamiento(self):
        """Paso 9: Configuración del procesamiento de imágenes"""
        print("\n⚙️ Paso 9: Configuración del procesamiento de imágenes")

        # Configurar forma de imagen
        altura_objetivo = 256
        ancho_objetivo = 256
        self.analizador.configurar_forma_imagen(altura_objetivo, ancho_objetivo, 3)

        print(f"✅ Forma de imagen configurada: {self.analizador.forma_imagen}")

        # Configurar tamaño de lote
        self.analizador.configurar_tamano_lote(16)
        print(f"✅ Tamaño de lote configurado: {self.analizador.tamano_lote}")

    def _paso_10_configurar_generador(self):
        """Paso 10: Configurar generador con aumento de datos"""
        print("\n🔄 Paso 10: Configurar generador de imágenes con aumento de datos")

        # Configurar el generador con parámetros de aumento de datos
        self.analizador.configurar_generador_imagenes(
            rotacion_max=20,
            desplazamiento_ancho=0.10,
            desplazamiento_alto=0.10,
            distorsion=0.1,
            zoom_max=0.1,
            giro_horizontal=True
        )

        print("✅ Generador de imágenes configurado con aumento de datos")

    def _paso_11_crear_generadores(self):
        """Paso 11: Crear generadores de datos"""
        print("\n🎯 Paso 11: Crear generadores de datos para entrenamiento")

        # Crear generadores de datos
        self.analizador.crear_generadores_datos(modo_clase='categorical')

        print("✅ Generadores de datos creados")

        # Mostrar información de los generadores
        print(f"\n📊 Información del generador de entrenamiento:")
        print(f"  • Número de muestras: {self.analizador.generador_train.samples}")
        print(f"  • Número de clases: {self.analizador.generador_train.num_classes}")
        print(f"  • Tamaño de lote: {self.analizador.generador_train.batch_size}")

        print(f"\n📊 Información del generador de prueba:")
        print(f"  • Número de muestras: {self.analizador.generador_test.samples}")
        print(f"  • Número de clases: {self.analizador.generador_test.num_classes}")
        print(f"  • Tamaño de lote: {self.analizador.generador_test.batch_size}")

    def _paso_12_mostrar_indices(self):
        """Paso 12: Mostrar índices de clases"""
        print("\n🏷️ Paso 12: Mostrar índices de clases")

        # Índices para entrenamiento
        indices_clases_train = self.analizador.obtener_indices_clases("entrenamiento")

        print("🏷️ Índices de clases para el modelo entrenamiento:")
        for clase, indice in indices_clases_train.items():
            print(f"  {clase}: {indice}")

        # Índices para pruebas
        indices_clases_test = self.analizador.obtener_indices_clases("pruebas")

        print("\n🏷️ Índices de clases para el modelo pruebas:")
        for clase, indice in indices_clases_test.items():
            print(f"  {clase}: {indice}")

    def _paso_13_transformaciones_ejemplo(self):
        """Paso 13: Demostrar transformaciones de aumento de datos"""
        print("\n🔄 Paso 13: Demostrar transformaciones de aumento de datos")

        # Seleccionar una imagen de ejemplo
        clase_ejemplo = self.clases[0]
        ruta_clase_ejemplo = os.path.join(self.analizador.ruta_train, clase_ejemplo)
        imagenes_ejemplo = os.listdir(ruta_clase_ejemplo)
        imagen_ejemplo = os.path.join(ruta_clase_ejemplo, imagenes_ejemplo[0])

        print(f"🔄 Ejemplos de transformaciones aplicadas a: {clase_ejemplo}")
        self.analizador.mostrar_transformacion_ejemplo(imagen_ejemplo, num_transformaciones=5)

    def _paso_14_resumen_final(self):
        """Paso 14: Resumen final del análisis"""
        print("\n" + "=" * 60)
        print("           RESUMEN FINAL DEL ANÁLISIS")
        print("=" * 60)

        indices_clases = self.analizador.obtener_indices_clases("entrenamiento")

        print(f"\n🎯 Dataset analizado: Clasificación de enfermedades en papas")
        print(f"📁 Directorio: {self.analizador.directorio_base}")
        print(f"\n📊 Estadísticas generales:")
        print(f"  • Clases identificadas: {len(self.clases)}")
        print(f"  • Total de imágenes de entrenamiento: {self.analizador.generador_train.samples:,}")
        print(f"  • Total de imágenes de prueba: {self.analizador.generador_test.samples:,}")
        print(f"  • Forma de imagen configurada: {self.analizador.forma_imagen}")
        print(f"  • Tamaño de lote: {self.analizador.tamano_lote}")

        print(f"\n🏷️ Clases del dataset:")
        for i, (clase, indice) in enumerate(indices_clases.items(), 1):
            cantidad = self.conteos_train[clase]
            print(f"  {i}. {clase} (índice: {indice}) - {cantidad:,} imágenes")

        print(f"\n✅ Análisis completado exitosamente")
        print(f"✅ Generadores de datos listos para entrenamiento")
        print(f"✅ Dataset preparado para modelo de deep learning")
        print("=" * 60)

    def obtener_generadores(self):
        """Obtiene los generadores listos para usar"""
        if not self.configurado:
            raise ValueError("Pipeline no ejecutado. Ejecuta primero ejecutar_eda_completo()")

        return self.analizador.generador_train, self.analizador.generador_test

    def obtener_metadatos(self):
        """Obtiene metadatos del dataset"""
        if not self.configurado:
            raise ValueError("Pipeline no ejecutado. Ejecuta primero ejecutar_eda_completo()")

        return {
            'clases': self.clases,
            'conteos_train': self.conteos_train,
            'conteos_test': self.conteos_test,
            'forma_imagen': self.analizador.forma_imagen,
            'tamano_lote': self.analizador.tamano_lote,
            'num_clases': self.analizador.generador_train.num_classes,
            'indices_clases': self.analizador.obtener_indices_clases("entrenamiento")
        }


# Función de uso simple
def ejecutar_eda_automatico(directorio_proyecto="Modulo1_AgroIA", mostrar_graficos=False):
    """
    Ejecuta el EDA completo de manera automatizada.

    Args:
        directorio_proyecto: Nombre del directorio del proyecto
        mostrar_graficos: Si mostrar gráficos e imágenes

    Returns:
        tuple: (analizador, generador_train, generador_test, metadatos)
    """
    pipeline = PipelineEDA(directorio_proyecto, mostrar_graficos)
    analizador = pipeline.ejecutar_eda_completo()
    gen_train, gen_test = pipeline.obtener_generadores()
    metadatos = pipeline.obtener_metadatos()

    return analizador, gen_train, gen_test, metadatos
