import streamlit as st
import importlib
import os

# Configuración de la página
st.set_page_config(
    page_title="Reportes de Colegios",
    page_icon="📊",
    layout="wide"
)

# Descubrir secciones disponibles en la carpeta 'secciones'
secciones_path = os.path.join(os.path.dirname(__file__), 'secciones')
secciones = [f[:-3] for f in os.listdir(secciones_path) if f.endswith('.py') and not f.startswith('__')]

# Sidebar para seleccionar sección
seccion = st.sidebar.selectbox("Selecciona una sección", secciones, format_func=lambda x: x.capitalize())

# Importar y mostrar la sección seleccionada
def mostrar_seccion(nombre):
    modulo = importlib.import_module(f'secciones.{nombre}')
    modulo.mostrar()

mostrar_seccion(seccion)
