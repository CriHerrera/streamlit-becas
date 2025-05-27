import streamlit as st
import pandas as pd
from pathlib import Path
import base64
from pdf_reports import (
    convertir_imagen_base64,
    generar_tabla_completitud,
    generar_lista_participacion,
    generar_estado_admision,
    generar_grafico_grado,
    generar_imagen_base64_grafico
)
from urllib.parse import quote

# Configuración de la página
st.set_page_config(
    page_title="Reportes de Colegios",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
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
        
        .table-container {
            background-color: white;
            padding: 30px;
            margin: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }
        
        .stDataFrame {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }
        
        .stProgress > div > div {
            background-color: #5DDBDB;
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
        
        /* Fondo y texto de las tablas de Streamlit */
        .stDataFrame, .stTable {
            background-color: white !important;
            color: #222 !important;
            border-radius: 10px !important;
            font-family: 'Inter', sans-serif !important;
        }
        /* Encabezados de tabla */
        .stDataFrame th, .stTable th {
            background-color: #5DDBDB !important;
            color: white !important;
            font-weight: bold !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 1.1em !important;
            border: none !important;
        }
        /* Celdas de tabla */
        .stDataFrame td, .stTable td {
            background-color: white !important;
            color: #222 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1em !important;
            border: none !important;
        }
        /* Bordes suaves */
        .stDataFrame table, .stTable table {
            border-radius: 10px !important;
            overflow: hidden !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
        }
        /* Quitar fondo oscuro de filas seleccionadas */
        .stDataFrame tr, .stTable tr {
            background-color: white !important;
        }
        /* Mejorar padding */
        .stDataFrame td, .stTable td, .stDataFrame th, .stTable th {
            padding: 14px 18px !important;
        }
        /* Sombra sutil */
        .stDataFrame, .stTable {
            box-shadow: 2px 2px 12px rgba(0,0,0,0.07);
        }
        body, .stApp, .markdown-text-container, .stMarkdown, p, span, label, div {
            color: #111 !important;
        }
        /* Si quieres que los títulos sigan siendo blancos en el header: */
        .header h1, .header h2, .header h3 {
            color: white !important;
        }
        /* Botones siguen igual */
        .stButton > button {
            color: white !important;
        }
        /* Forzar color negro en todos los textos de markdown y contenedores de texto */
        .stMarkdown, .markdown-text-container, .stApp, body, p, span, div, label {
            color: #111 !important;
        }
        /* Mantener títulos en header en blanco */
        .header h1, .header h2, .header h3 {
            color: white !important;
        }
        /* Botones siguen igual */
        .stButton > button {
            color: white !important;
        }
        .info-box {
            background: #d6f6fb;
            color: #111;
            border-radius: 6px;
            padding: 12px 18px;
            margin-bottom: 18px;
            font-size: 1.05em;
            font-family: 'Inter', sans-serif;
        }
        /* Contenedor de la tabla */
        .stDataFrame, .stTable {
            background-color: white !important;
            border-radius: 10px !important;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1) !important;
            padding: 30px !important;
            margin: 20px 0 !important;
        }
        /* Tabla interna */
        .stDataFrame table, .stTable table {
            width: 100% !important;
            border-collapse: collapse !important;
            margin: 20px 0 !important;
            border-radius: 10px !important;
            overflow: hidden !important;
        }
        /* Encabezado */
        .stDataFrame th, .stTable th {
            background-color: #5DDBDB !important;
            color: white !important;
            padding: 12px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 1.08em !important;
            border: 1px solid #BDC3C7 !important;
        }
        /* Celdas */
        .stDataFrame td, .stTable td {
            background-color: white !important;
            color: #222 !important;
            padding: 12px !important;
            border: 1px solid #BDC3C7 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1em !important;
        }
        /* Quitar fondo oscuro de filas seleccionadas */
        .stDataFrame tr, .stTable tr {
            background-color: white !important;
        }
        /* Texto pequeño */
        .small-text {
            font-size: 12px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Definir rutas base
base_path = Path(__file__).parent.resolve()
base_path_inputs = base_path / "inputs"

# Cargar datos
@st.cache_data
def load_data():
    # Cargar el primer DataFrame con tipos específicos
    df = pd.read_csv(
        base_path_inputs / "estadisticas_completitud_dummys.csv",
        dtype={
            'campus_code': str,
            'nombre_colegio': str,
            'colegio_notificado_colaboracion': int,
            'colegio_firmo_compromisos': int,
            'colegio_envio_base': int,
            'napsis': int
        }
    )
    
    # Cargar el segundo DataFrame con low_memory=False para evitar advertencias de tipos mixtos
    df_panel_grade = pd.read_csv(
        base_path_inputs / "panel_grade.csv",
        low_memory=False,
        dtype={
            'campusId': str,
            'gradetrack_name': str
        }
    )
    
    return df, df_panel_grade

# Cargar imágenes
@st.cache_data
def load_images():
    try:
        ruta_logo = base_path_inputs / "assets" / "TETHER.png"
        ruta_check = base_path_inputs / "assets" / "ok.png"
        
        logo_base64 = convertir_imagen_base64(ruta_logo)
        check_base64 = convertir_imagen_base64(ruta_check)
        
        return logo_base64, check_base64
    except Exception as e:
        st.error(f"Error al cargar las imágenes: {str(e)}")
        return None, None

# Leer parámetro de la URL (SOLO NUEVA API)
selected_school = st.query_params.get("colegio", None)

df, df_panel_grade = load_data()
logo_base64, check_base64 = load_images()
schools = df["nombre_colegio"].dropna().unique()


if not selected_school:
    # Página principal: lista de botones
    st.markdown(
        """
        <div class="header">
            <h1>Reportes de Colegios</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("### Seleccione un colegio para ver su reporte:")
    for school in schools:
        if st.button(school):
            st.query_params["colegio"] = school
            st.rerun()
else:
    # Página de reporte individual
    if logo_base64 is None or check_base64 is None:
        st.error("No se pudieron cargar las imágenes necesarias. Por favor, verifique que los archivos existan en la carpeta assets.")
        st.stop()
    df_school = df[df["nombre_colegio"] == selected_school]
    if df_school.empty:
        st.error(f"No se encontraron datos para el colegio {selected_school}")
        st.stop()
    fila = df_school.iloc[0]
    codigo_del_colegio = fila["campus_code"]
    
    # Logo en la esquina superior derecha
    st.markdown(
        f'<div style="position: absolute; top: 10px; right: 10px;"><img src="data:image/png;base64,{logo_base64}" width="100"></div>',
        unsafe_allow_html=True
    )
    
    # Título del reporte
    st.markdown(
        f"""
        <div class="header">
            <h1>Informe Avance Colegio {selected_school}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Descripción
    st.markdown("""
    El objetivo principal de esta iniciativa es asegurar la digitalización del proceso de matrícula, 
    una reposición rápida de vacantes y una interacción constante y transparente con las familias, 
    permitiendo que estas puedan matricular 24/7 de forma remota y conforme a los lineamientos de la Superintendencia.
    """)
    
    # Estado actual del proceso
    st.markdown("### Estado actual del proceso")

    # Texto explicativo normal, sin recuadro
    st.markdown(
        "A continuación dejamos una tabla con todos los indicadores que podemos ver desde la plataforma y a los cuales tenemos acceso:"
    )
    estado_admision = generar_estado_admision(fila)
    st.dataframe(
        pd.DataFrame(estado_admision),
        use_container_width=True,
        hide_index=True
    )
    
    # Completitud de información
    st.markdown("### Completitud de información")
    
    #Texto explicativo normal, sin recuadro
    st.markdown(
        "Porcentaje de estudiantes matriculados que cuentan con la siguiente información:"
    )
    completitud = generar_tabla_completitud(fila)
    for item in completitud:
        st.markdown(f"""
            <div class="bar-row">
                <span class="bar-label">{item['Información']} ({item['Porcentaje Completado']})</span>
                <div class="bar">
                    <div class="bar-fill" style="width: {item['Porcentaje Completado'].strip('%')}%"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Resumen de participación
    st.markdown("### Resumen de Participación")
    participacion = generar_lista_participacion(fila, check_base64)
    for item in participacion:
        st.markdown(f"{item['estado']} {item['texto']}", unsafe_allow_html=True)
    
    # Matrícula por grado
    st.markdown("### Matrícula por grado")
    grafico_grados = generar_grafico_grado(df_panel_grade, codigo_del_colegio)
    for grado in grafico_grados:
        st.markdown(f"""
            <div class="bar-row">
                <span class="bar-label">{grado['Grado']} ({grado['Cantidad']} estudiantes)</span>
                <div class="bar">
                    <div class="bar-fill" style="width: {grado['Porcentaje']}%"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de barras
    grafico_base64 = generar_imagen_base64_grafico(df_panel_grade, codigo_del_colegio)
    if grafico_base64:
        st.markdown("### Distribución de matrícula por grado")
        st.image(f"data:image/png;base64,{grafico_base64}", use_container_width=True)

