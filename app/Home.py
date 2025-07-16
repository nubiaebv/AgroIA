"""
Clase: Home

Objetivo: Clase para pagina principal web

Cambios:
    1. Creacion de clase pmarin 05-07-2025
    2. Implementación de control de excepciones robusto 06-07-2025
"""
import os
import logging
import streamlit as st
from typing import Dict, Optional, Any
from app.assets.Modulo1Web import Modulo1Web
from app.assets.Modulo3Web import Modulo3Web


# Configurar logging específico para Home
logger = logging.getLogger(__name__)


class Home:
    def __init__(self, base_dir: str):
        """
        Inicializa la clase Home con manejo de excepciones

        Args:
            base_dir (str): Directorio base de la aplicación
        """
        try:
            # Validar que base_dir es válido
            if not base_dir:
                raise ValueError("El directorio base no puede estar vacío")

            if not os.path.exists(base_dir):
                logger.warning(f"El directorio base no existe: {base_dir}")
                # Crear directorio si no existe
                try:
                    os.makedirs(base_dir, exist_ok=True)
                    logger.info(f"Directorio base creado: {base_dir}")
                except OSError as e:
                    logger.error(f"No se pudo crear el directorio base: {e}")
                    raise

            self.__menu = {
                "Modelo ANN": Modulo3Web(),  # Representa el modulo ANN
                "Modelo CNN": Modulo1Web(),  # Representa el modulo CNN
                "Modelo RNN": None  # Representa el modulo RNN
            }
            self.__base_dir = base_dir

            # Inicializar session_state de manera segura
            self._inicializar_session_state()

            logger.info("Clase Home inicializada exitosamente")

        except ValueError as e:
            logger.error(f"Error de validación en __init__: {e}")
            st.error(f"Error de configuración: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado en __init__: {e}")
            st.error(f"Error al inicializar la aplicación: {e}")
            raise

    def _inicializar_session_state(self):
        """
        Inicializa el estado de la sesión de manera segura
        """
        try:
            # Verificar que session_state esté disponible
            if not hasattr(st, 'session_state'):
                raise AttributeError("session_state no está disponible")

            # Inicializar la página seleccionada si no existe
            if 'pagina_seleccionada' not in st.session_state:
                st.session_state.pagina_seleccionada = "Modelo ANN"
                logger.info("Estado de sesión inicializado con página predeterminada")

        except AttributeError as e:
            logger.error(f"Error al acceder a session_state: {e}")
            st.error("Error al inicializar el estado de la sesión")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al inicializar session_state: {e}")
            raise

    def _configurar_pagina(self):
        """
        Configura la página de Streamlit con manejo de excepciones
        """
        try:
            st.set_page_config(
                page_title="AgroIA",
                layout="wide",
                page_icon="📊"
            )
            logger.debug("Configuración de página aplicada exitosamente")

        except st.errors.StreamlitAPIException as e:
            # Esta excepción ocurre si set_page_config ya fue llamado
            logger.warning(f"Configuración de página ya establecida: {e}")
        except Exception as e:
            logger.error(f"Error al configurar página: {e}")
            st.warning("No se pudo configurar la página completamente")

    def _renderizar_sidebar_header(self):
        """
        Renderiza el header del sidebar con manejo de excepciones
        """
        try:
            st.sidebar.markdown("""
                <div style='text-align: center; margin-bottom: 30px;'>
                    <h2 style='color: #1f77b4; margin-bottom: 5px;'>Menú Principal</h2>
                    <hr style='margin: 10px 0; border: 1px solid #dee2e6;'>
                </div>
            """, unsafe_allow_html=True)

            logger.debug("Header del sidebar renderizado exitosamente")

        except Exception as e:
            logger.error(f"Error al renderizar header del sidebar: {e}")
            # Fallback: título simple
            st.sidebar.title("Menú Principal")

    def _aplicar_estilos_css(self):
        """
        Aplica los estilos CSS con manejo de excepciones
        """
        try:
            css_styles = """
                <style>
                .stButton button {
                    background-color: #f8f9fa;
                    color: #333333;
                    border: 2px solid #dee2e6;
                    border-radius: 10px;
                    padding: 12px 16px;
                    width: 100%;
                    text-align: left;
                    font-size: 14px;
                    font-weight: 400;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    transition: all 0.3s ease;
                    margin: 5px 0;
                }
                .stButton button:hover {
                    background-color: #e9ecef;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(31, 119, 180, 0.4);
                }
                .stButton button:focus {
                    background-color: #1f77b4 !important;
                    color: #ffffff !important;
                    border-color: #1f77b4 !important;
                    box-shadow: 0 4px 8px rgba(31, 119, 180, 0.3) !important;
                }
                .menu-button-active .stButton button {
                    background-color: #1f77b4 !important;
                    color: #ffffff !important;
                    border-color: #1f77b4 !important;
                    box-shadow: 0 4px 8px rgba(31, 119, 180, 0.3) !important;
                    font-weight: 600 !important;
                }
                .menu-description {
                    font-size: 11px;
                    color: #6c757d;
                    margin-top: -10px;
                    margin-bottom: 10px;
                    margin-left: 5px;
                    font-style: italic;
                }
                </style>
            """

            st.sidebar.markdown(css_styles, unsafe_allow_html=True)
            logger.debug("Estilos CSS aplicados exitosamente")

        except Exception as e:
            logger.error(f"Error al aplicar estilos CSS: {e}")
            st.warning("Los estilos visuales no se aplicaron correctamente")

    def _obtener_descripciones(self) -> Dict[str, str]:
        """
        Obtiene las descripciones de los módulos con manejo de excepciones

        Returns:
            Dict[str, str]: Diccionario con las descripciones
        """
        try:
            descripciones = {
                "Modelo ANN": "Gestión de datasets",
                "Modelo CNN": "Análisis exploratorio",
                "Modelo RNN": "Reducción dimensional"
            }

            # Validar que todas las opciones del menú tienen descripción
            for opcion in self.__menu.keys():
                if opcion not in descripciones:
                    logger.warning(f"Descripción faltante para: {opcion}")
                    descripciones[opcion] = "Descripción no disponible"

            return descripciones

        except Exception as e:
            logger.error(f"Error al obtener descripciones: {e}")
            # Fallback: descripciones vacías
            return {opcion: "" for opcion in self.__menu.keys()}

    def _renderizar_botones_menu(self):
        """
        Renderiza los botones del menú con manejo de excepciones
        """
        try:
            descripciones = self._obtener_descripciones()

            # Crear botones para cada opción del menú
            for nombre_opcion in self.__menu.keys():
                try:
                    descripcion = descripciones.get(nombre_opcion, "")

                    # Botón principal con key único
                    boton = st.sidebar.button(
                        nombre_opcion,
                        key=f"btn_{nombre_opcion}",
                        use_container_width=True
                    )

                    if boton:
                        st.session_state.pagina_seleccionada = nombre_opcion
                        logger.info(f"Página seleccionada: {nombre_opcion}")
                        st.rerun()

                except Exception as e:
                    logger.error(f"Error al renderizar botón {nombre_opcion}: {e}")
                    # Continuar con el siguiente botón
                    continue

            logger.debug("Botones del menú renderizados exitosamente")

        except Exception as e:
            logger.error(f"Error al renderizar botones del menú: {e}")
            st.sidebar.error("Error al cargar el menú")

    def _renderizar_pagina_seleccionada(self):
        """
        Renderiza la página seleccionada con manejo de excepciones
        """
        try:
            # Validar que existe una página seleccionada
            if 'pagina_seleccionada' not in st.session_state:
                logger.warning("No hay página seleccionada, usando predeterminada")
                st.session_state.pagina_seleccionada = "Modelo ANN"

            pagina_actual = st.session_state.pagina_seleccionada

            # Validar que la página existe en el menú
            if pagina_actual not in self.__menu:
                logger.error(f"Página no válida: {pagina_actual}")
                st.error(f"Página no encontrada: {pagina_actual}")
                return

            # Obtener el módulo de la página
            pagina_modulo = self.__menu[pagina_actual]

            if pagina_modulo is None:
                logger.info(f"Módulo no implementado para: {pagina_actual}")
                st.info(f"El módulo '{pagina_actual}' está en desarrollo")
                st.markdown("### Próximamente disponible")
                st.markdown(f"La funcionalidad de **{pagina_actual}** estará disponible pronto.")
                return

            # Renderizar la página
            if hasattr(pagina_modulo, 'render'):
                pagina_modulo.render()
                logger.debug(f"Página renderizada: {pagina_actual}")
            else:
                logger.error(f"Módulo {pagina_actual} no tiene método render")
                st.error(f"Error en el módulo {pagina_actual}")

        except KeyError as e:
            logger.error(f"Error de clave en renderizar_pagina: {e}")
            st.error("Error al acceder a la página seleccionada")
        except Exception as e:
            logger.error(f"Error inesperado al renderizar página: {e}")
            st.error("Error inesperado al cargar la página")

    def _renderizar_footer(self):
        """
        Renderiza el footer con manejo de excepciones
        """
        try:
            # Espaciador
            st.sidebar.markdown("<br>", unsafe_allow_html=True)

            # Footer
            footer_html = """
            <hr style='margin-top: 50px; border: 1px solid #dee2e6;'>
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; 
                        text-align: center; margin-top: 10px;'>
                <div style='font-size: 0.9em; color: #1f77b4; font-weight: 600;'>
                    © 2025 | Inteligencia Artificial Aplicada
                </div>
                <div style='font-size: 0.8em; color: #6c757d; margin-top: 5px;'>
                    Big Data CUC
                </div>
            </div>
            """

            st.sidebar.markdown(footer_html, unsafe_allow_html=True)
            logger.debug("Footer renderizado exitosamente")

        except Exception as e:
            logger.error(f"Error al renderizar footer: {e}")
            # Fallback: footer simple
            st.sidebar.markdown("---")
            st.sidebar.text("© 2025 | Inteligencia Artificial Aplicada")

    def home(self):
        """
        Método principal que renderiza la página home con manejo completo de excepciones
        """
        try:
            # Configurar página
            self._configurar_pagina()

            # Renderizar componentes del sidebar
            self._renderizar_sidebar_header()
            self._aplicar_estilos_css()
            self._renderizar_botones_menu()

            # Renderizar la página seleccionada
            self._renderizar_pagina_seleccionada()

            # Renderizar footer
            self._renderizar_footer()

            logger.info("Página home renderizada exitosamente")

        except Exception as e:
            logger.critical(f"Error crítico en home(): {e}")
            st.error("Error crítico al cargar la aplicación")
            st.info("Por favor, recarga la página o contacta al administrador")

            # Mostrar información de debug en modo desarrollo
            if os.getenv('DEBUG', 'False').lower() == 'true':
                st.exception(e)

    def agregar_modulo(self, nombre: str, modulo: Any):
        """
        Agrega un nuevo módulo al menú con validación

        Args:
            nombre (str): Nombre del módulo
            modulo (Any): Instancia del módulo
        """
        try:
            if not nombre:
                raise ValueError("El nombre del módulo no puede estar vacío")

            if not hasattr(modulo, 'render'):
                raise AttributeError(f"El módulo {nombre} debe tener un método 'render'")

            self.__menu[nombre] = modulo
            logger.info(f"Módulo agregado exitosamente: {nombre}")

        except ValueError as e:
            logger.error(f"Error de validación al agregar módulo: {e}")
            raise
        except AttributeError as e:
            logger.error(f"Error de atributo al agregar módulo: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al agregar módulo: {e}")
            raise

    def obtener_modulos(self) -> Dict[str, Any]:
        """
        Obtiene la lista de módulos disponibles

        Returns:
            Dict[str, Any]: Diccionario con los módulos
        """
        try:
            return self.__menu.copy()
        except Exception as e:
            logger.error(f"Error al obtener módulos: {e}")
            return {}