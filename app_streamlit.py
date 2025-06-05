import streamlit as st
<<<<<<< HEAD
import importlib
import os

# Configuración de la página
st.set_page_config(
    page_title="Reportes Colegios",
    page_icon="📊",
    layout="wide"
)

# BLOQUE DE CSS GLOBAL
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
=======
import os

# Paths
becas = pd.read_csv('becas_procesadas_para_dash.csv', sep=';')

# Colapsar por name y numero_corrida
becas_collapsed = becas.groupby(['name', 'numero_corrida']).first().reset_index()

# Tabla de estudiantes nuevos/antiguos
pivot_estudiantes = pd.crosstab(
    becas_collapsed['name'],
    becas_collapsed['para_estudiantes_nuevos_y_antiguos_o_no']
).reset_index().rename(columns={'name': 'Nombre de la Beca'})

# Tabla de requisitos
pivot_requisitos = pd.crosstab(becas['nombre_de_la_beca'], becas['n_requisitos'])
pivot_requisitos.columns = [f'{col} Requisitos' for col in pivot_requisitos.columns]
pivot_requisitos = pivot_requisitos.reset_index().rename(columns={'nombre_de_la_beca': 'Nombre de la Beca'})

# Tabla de pasos
pivot_pasos = pd.crosstab(becas['nombre_de_la_beca'], becas['n_pasos'])
pivot_pasos.columns = [f'{col} Pasos' for col in pivot_pasos.columns]
pivot_pasos = pivot_pasos.reset_index().rename(columns={'nombre_de_la_beca': 'Nombre de la Beca'})

# ==== Streamlit App ====

# Estilos base
st.set_page_config(page_title="Análisis de Becas Chile", layout="wide")

# Header
st.markdown(
    """
    <div style="background-color:#0C1461;padding:20px;border-radius:10px;text-align:center;">
        <h1 style="color:white;font-family: 'DM Sans', sans-serif;">Análisis de Becas Chile</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Tabs
tab1, tab2, tab3 = st.tabs(["Estudiantes Nuevos/Antiguos", "Requisitos", "Pasos"])

with tab1:
    st.markdown("### Frecuencia de Estudiantes Nuevos/Antiguos por Beca")
    st.dataframe(pivot_estudiantes, use_container_width=True)

with tab2:
    st.markdown("### Frecuencia de Requisitos por Beca")
    st.dataframe(pivot_requisitos, use_container_width=True)

with tab3:
    st.markdown("### Frecuencia de Pasos por Beca")
    st.dataframe(pivot_pasos, use_container_width=True)
>>>>>>> parent of 0c3f713 (Update app_streamlit.py)
