import streamlit as st
import time
from PIL import Image

from src.train.cnn import cnn
from src.utils.metrics import obtener_ruta_app


class Modulo1Web:
    def __init__(self):
        self.archivo_cargado = None
        self.analisis_realizado = False

    def render(self):
        try:
            st.title("🖼️ Carga de Imágenes")

            # Carga de archivo de imagen
            col1, col2 = st.columns([1, 2])
            with col1:
                st.info("Formatos soportados: PNG, JPG, JPEG")
            with col2:
                archivo = st.file_uploader(
                    "Sube tu imagen (.png, .jpg, .jpeg)",
                    type=["png", "jpg", "jpeg"],
                    key="uploader"
                )

            # Si se subió un archivo
            if archivo is not None:
                nombre = archivo.name
                prev_name = st.session_state.get('file_name')
                # Si es un archivo nuevo o cambia:
                if prev_name != nombre:
                    try:
                        # Leer la imagen
                        imagen = Image.open(archivo)

                        # Validar que la imagen sea válida
                        try:
                            imagen.verify()
                            archivo.seek(0)  # Resetear el pointer después de verify
                            imagen = Image.open(archivo)  # Reabrir después de verify
                        except Exception as e:
                            st.error(f"❌ El archivo no es una imagen válida: {e}")
                            return

                        # Verificar tamaño de la imagen
                        if imagen.width > 5000 or imagen.height > 5000:
                            st.warning(
                                f"⚠️ Imagen muy grande ({imagen.width}x{imagen.height}). Puede ser lenta de procesar.")

                        # Guardar en session_state
                        st.session_state.imagen_cargada = imagen
                        st.session_state.file_name = nombre
                        st.session_state.analisis_generado = False
                        # Limpiar resultado anterior cuando se carga nueva imagen
                        if 'resultado_prediccion' in st.session_state:
                            del st.session_state.resultado_prediccion

                        st.success(f"✅ Imagen '{nombre}' cargada exitosamente.")
                    except FileNotFoundError:
                        st.error("❌ Error: No se pudo encontrar el archivo.")
                    except PermissionError:
                        st.error("❌ Error: No se tienen permisos para leer el archivo.")
                    except OSError as e:
                        st.error(f"❌ Error del sistema al leer el archivo: {e}")
                    except Exception as e:
                        st.error(f"❌ Error inesperado al cargar la imagen: {e}")

                # Siempre asignar la imagen a self para mostrar
                try:
                    self.archivo_cargado = st.session_state.get('imagen_cargada')
                except Exception as e:
                    st.error(f"❌ Error al recuperar la imagen del estado: {e}")

            # Mostrar la imagen si existe imagen cargada
            if 'imagen_cargada' in st.session_state:
                try:
                    st.subheader("Vista previa de la imagen")

                    # Mostrar información de la imagen
                    imagen = st.session_state.imagen_cargada
                    col_info1, col_info2, col_info3 = st.columns(3)

                    try:
                        with col_info1:
                            st.metric("Ancho", f"{imagen.width} px")
                        with col_info2:
                            st.metric("Alto", f"{imagen.height} px")
                        with col_info3:
                            st.metric("Modo", imagen.mode)
                    except AttributeError:
                        st.warning("⚠️ No se pudo obtener información de la imagen.")
                    except Exception as e:
                        st.error(f"❌ Error al mostrar información de la imagen: {e}")

                    # Mostrar la imagen centrada
                    try:
                        st.image(
                            st.session_state.imagen_cargada,
                            caption=f"Imagen: {st.session_state.get('file_name', 'Sin nombre')}",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"❌ Error al mostrar la imagen: {e}")

                    # Botón para análisis
                    col3, col4, col5 = st.columns([3, 2, 3])
                    with col4:
                        if st.button("📊 Generar análisis"):
                            try:
                                progreso = st.progress(0, text="Iniciando análisis...")

                                # Progreso inicial
                                progreso.progress(20, text="Cargando modelo...")
                                clasificador = cnn(obtener_ruta_app("AgroIA"))

                                progreso.progress(40, text="Modelo cargado, procesando imagen...")

                                # Hacer la predicción
                                clase_predicha = clasificador.predeccir_imagen(st.session_state.imagen_cargada)

                                progreso.progress(80, text="Análisis casi completo...")

                                # Pequeña pausa para efecto visual
                                time.sleep(0.5)
                                progreso.progress(100, text="¡Análisis completado!")

                                # Guardar en session_state ANTES de mostrar
                                st.session_state.resultado_prediccion = clase_predicha
                                st.session_state.analisis_generado = True

                                # Eliminar la barra de progreso
                                progreso.empty()

                            except Exception as e:
                                st.error(f"❌ Error durante el análisis: {e}")
                                # Opcional: mostrar más detalles del error
                                if st.checkbox("Mostrar detalles del error"):
                                    st.exception(e)

                    # MOSTRAR RESULTADOS - Esta parte debe estar FUERA del if del botón
                    # para que se muestre siempre que exista un resultado
                    if 'resultado_prediccion' in st.session_state:
                        self._mostrar_resultados()

                except KeyError:
                    st.error("❌ Error: No se encontró la imagen en el estado de la sesión.")
                except Exception as e:
                    st.error(f"❌ Error inesperado al procesar la imagen: {e}")

            else:
                st.info("Por favor sube una imagen en formato PNG, JPG o JPEG.")

        except Exception as e:
            st.error(f"Ocurrió un error en la pantalla de imágenes: {e}")

    def _mostrar_resultados(self):
        """Método separado para mostrar los resultados de la predicción"""
        try:
            resultado = st.session_state.resultado_prediccion

            st.subheader("🔍 Resultados del análisis")

            # Expander principal con los resultados
            with st.expander("Ver resultados de la predicción", expanded=True):
                col1, col2 = st.columns([1, 2])

                with col1:
                    # Determinar el emoji y texto según el resultado
                    if resultado == "Potato_healthy":
                        emoji_resultado = "✅ Sana"
                        color_metrica = "normal"
                    elif resultado == "Potato_Early_blight":
                        emoji_resultado = "⚠️ Tizón Temprano"
                        color_metrica = "normal"
                    elif resultado == "Potato_Late_blight":
                        emoji_resultado = "🚨 Tizón Tardío"
                        color_metrica = "normal"
                    else:
                        emoji_resultado = "❓ Desconocido"
                        color_metrica = "normal"

                    st.metric("Diagnóstico", emoji_resultado)

                with col2:
                    st.write("**Estado de la planta:**")

                    # Mostrar información detallada según el resultado
                    if resultado == "Potato_healthy":
                        st.success("🌿 La papa está completamente sana")
                        st.info("**Recomendación:** Mantener las prácticas actuales de cuidado")
                    elif resultado == "Potato_Early_blight":
                        st.warning("⚠️ Se detectó tizón temprano (Early Blight)")
                        st.info(
                            "**Recomendación:** Aplicar fungicida preventivo y mejorar ventilación")
                    elif resultado == "Potato_Late_blight":
                        st.error("🚨 Se detectó tizón tardío (Late Blight)")
                        st.info(
                            "**Recomendación:** Tratamiento urgente con fungicida específico")
                    else:
                        st.warning(f"Resultado no reconocido: {resultado}")

        except Exception as e:
            st.error(f"❌ Error al mostrar resultados: {e}")