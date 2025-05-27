import streamlit as st
import importlib
import os

# Configuración de la página
st.set_page_config(
    page_title="Reportes de Colegios",
    page_icon="📊",
    layout="wide"
)

{# BLOQUE DE CSS GLOBAL
st.markdown("""
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #eaefff;
        }
        .stApp {
            background-color: #eaefff;
        }
        h1, h2, h3 {
            font-family: 'DM Sans', sans-serif;
            color: black;
        }
        .header {
            background-color: #0C1461;
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            position: relative;
            margin-top: 50px;
        }
        .header h1 {
            color: white;
        }
        .stDataFrame, .stTable {
            background: transparent !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        .stDataFrame table, .stTable table {
            background: transparent !important;
            border-radius: 10px !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        .stDataFrame th, .stTable th {
            background-color: #5DDBDB !important;
            color: white !important;
            padding: 12px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 1.08em !important;
            border: 1px solid #BDC3C7 !important;
        }
        .stDataFrame td, .stTable td {
            background-color: white !important;
            color: #222 !important;
            padding: 12px !important;
            border: 1px solid #BDC3C7 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1em !important;
        }
        .stDataFrame tr, .stTable tr {
            background: transparent !important;
        }
        .bar-row {
            margin-bottom: 12px;
        }
        .bar-label {
            display: block;
            font-weight: 500;
            margin-bottom: 4px;
        }
        .bar {
            width: 100%;
            background-color: #ddd;
            border-radius: 8px;
            height: 24px;
        }
        .bar-fill {
            background-color: #5DDBDB;
            height: 100%;
            border-radius: 8px;
        }
        .stButton > button {
            background-color: #0C1461;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #5DDBDB;
            color: white;
        }
        body, .stApp, .markdown-text-container, .stMarkdown, p, span, label, div {
            color: #111 !important;
        }
        .header h1, .header h2, .header h3 {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)
}

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

