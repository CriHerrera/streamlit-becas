import pandas as pd
import streamlit as st
import urllib.parse
from io import StringIO

# ========== Carga de datos ==========
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

# ========== Configuración Streamlit ==========
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

# ========== Capturar parámetro desde URL ==========
params = st.query_params
beca_param = params.get("name", [None])[0]

# ========== Normalizar parámetros ==========
if beca_param:
    beca_param = beca_param.strip().lower()
    becas['name_lower'] = becas['name'].astype(str).str.strip().str.lower()
    becas['nombre_larga_lower'] = becas['nombre_de_la_beca'].astype(str).str.strip().str.lower()

    match = becas[becas['name_lower'] == beca_param]

    if not match.empty:
        nombre_limpio = match['name'].values[0]
        nombre_visible = match['nombre_de_la_beca'].values[0]

        # Mostrar encabezado individual
        st.markdown(f"""
        <div style="background-color:#F1F6FF;padding:20px 10px;border-radius:10px;text-align:center;">
            <h2 style="color:#0C1461;margin-bottom:0;">{nombre_visible}</h2>
            <p style="color:#444;">Reporte exclusivo generado para esta beca</p>
        </div>
        """, unsafe_allow_html=True)

        # Filtrar info individualmente
        beca_est = pivot_estudiantes[pivot_estudiantes['Nombre de la Beca'].str.lower() == nombre_limpio.lower()]
        beca_req = pivot_requisitos[pivot_requisitos['Nombre de la Beca'].str.lower() == nombre_visible.lower()]
        beca_pasos = pivot_pasos[pivot_pasos['Nombre de la Beca'].str.lower() == nombre_visible.lower()]

        # Mostrar pestañas si hay datos
        if not beca_est.empty or not beca_req.empty or not beca_pasos.empty:
            tab1, tab2, tab3 = st.tabs(["Estudiantes Nuevos/Antiguos", "Requisitos", "Pasos"])

            with tab1:
                st.markdown("#### Frecuencia de Estudiantes Nuevos/Antiguos")
                st.dataframe(beca_est, use_container_width=True)

            with tab2:
                st.markdown("#### Requisitos para la Beca")
                st.dataframe(beca_req, use_container_width=True)

            with tab3:
                st.markdown("#### Pasos para Postulación")
                st.dataframe(beca_pasos, use_container_width=True)
        else:
            st.warning("⚠️ No se encontraron datos específicos para esta beca.")
    else:
        st.warning("⚠️ La beca indicada no fue encontrada.")
else:
    # Si no hay parámetro, mostrar resumen
    st.markdown("### 📊 Resumen general de todas las becas")
    tab1, tab2, tab3 = st.tabs(["Estudiantes Nuevos/Antiguos", "Requisitos", "Pasos"])

    with tab1:
        st.markdown("#### Frecuencia por tipo de estudiante")
        st.dataframe(pivot_estudiantes, use_container_width=True)

    with tab2:
        st.markdown("#### Frecuencia de requisitos por beca")
        st.dataframe(pivot_requisitos, use_container_width=True)

    with tab3:
        st.markdown("#### Frecuencia de pasos por beca")
        st.dataframe(pivot_pasos, use_container_width=True)
