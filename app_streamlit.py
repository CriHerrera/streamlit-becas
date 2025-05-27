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

# Configuración de la página
st.set_page_config(
    page_title="Reportes de Colegios",
    page_icon="📊",
    layout="wide"
)

# Definir rutas base
base_path = Path("C:/Users/crish/OneDrive - Universidad Adolfo Ibanez/Documents/GitHub/streamlit-becas")
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

# Título principal
st.markdown(
    """
    <div style="background-color:#0C1461;padding:20px;border-radius:10px;text-align:center;">
        <h1 style="color:white;font-family: 'DM Sans', sans-serif;">Reportes de Colegios</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Cargar datos
try:
    df, df_panel_grade = load_data()
    logo_base64, check_base64 = load_images()
    
    if logo_base64 is None or check_base64 is None:
        st.error("No se pudieron cargar las imágenes necesarias. Por favor, verifique que los archivos existan en la carpeta assets.")
        st.stop()
    
    # Obtener lista de colegios
    schools = df["nombre_colegio"].dropna().unique()
    
    if len(schools) == 0:
        st.error("No se encontraron colegios en los datos. Por favor, verifique el archivo de datos.")
        st.stop()
    
    # Sidebar para selección de colegio
    st.sidebar.title("Selección de Colegio")
    selected_school = st.sidebar.selectbox(
        "Seleccione un colegio:",
        options=schools,
        index=0
    )
    
    # Mostrar reporte para el colegio seleccionado
    if selected_school:
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
        st.markdown(f"## Informe Avance Colegio {selected_school}")
        
        # Descripción
        st.markdown("""
        El objetivo principal de esta iniciativa es asegurar la digitalización del proceso de matrícula, 
        una reposición rápida de vacantes y una interacción constante y transparente con las familias, 
        permitiendo que estas puedan matricular 24/7 de forma remota y conforme a los lineamientos de la Superintendencia.
        """)
        
        # Estado actual del proceso
        st.markdown("### Estado actual del proceso")
        estado_admision = generar_estado_admision(fila)
        st.dataframe(
            pd.DataFrame(estado_admision),
            use_container_width=True,
            hide_index=True
        )
        
        # Completitud de información
        st.markdown("### Completitud de información")
        completitud = generar_tabla_completitud(fila)
        for item in completitud:
            st.markdown(f"**{item['Información']}** ({item['Porcentaje Completado']})")
            st.progress(float(item['Porcentaje Completado'].strip('%')) / 100)
        
        # Resumen de participación
        st.markdown("### Resumen de Participación")
        participacion = generar_lista_participacion(fila, check_base64)
        for item in participacion:
            st.markdown(f"{item['estado']} {item['texto']}", unsafe_allow_html=True)
        
        # Matrícula por grado
        st.markdown("### Matrícula por grado")
        grafico_grados = generar_grafico_grado(df_panel_grade, codigo_del_colegio)
        for grado in grafico_grados:
            st.markdown(f"**{grado['Grado']}** - {grado['Cantidad']} estudiantes")
            st.progress(grado['Porcentaje'] / 100)
        
        # Gráfico de barras
        grafico_base64 = generar_imagen_base64_grafico(df_panel_grade, codigo_del_colegio)
        if grafico_base64:
            st.markdown("### Distribución de matrícula por grado")
            st.image(f"data:image/png;base64,{grafico_base64}", use_column_width=True)
        
except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    st.info("Por favor, asegúrese de que los archivos de datos estén en la ubicación correcta.") 