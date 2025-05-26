# -*- coding: utf-8 -*-
"""
Created on Mon May 19 11:24:36 2025
@author: crish
"""

import pandas as pd
import streamlit as st
import urllib.parse
from io import StringIO

# ========== Carga de datos ==========
becas = pd.read_csv('becas_procesadas_para_dash.csv', sep=';')

# Colapsar por name y numero_corrida
becas_collapsed = becas.groupby(['name', 'numero_corrida']).first().reset_index()

# Crear tablas dinámicas
pivot_estudiantes = pd.crosstab(
    becas_collapsed['numero_corrida'],
    becas_collapsed['para_estudiantes_nuevos_y_antiguos_o_no']
).reset_index()

pivot_requisitos = pd.crosstab(becas['numero_corrida'], becas['n_requisitos'])
pivot_requisitos.columns = [f'{col} Requisitos' for col in pivot_requisitos.columns]
pivot_requisitos = pivot_requisitos.reset_index()

pivot_pasos = pd.crosstab(becas['numero_corrida'], becas['n_pasos'])
pivot_pasos.columns = [f'{col} Pasos' for col in pivot_pasos.columns]
pivot_pasos = pivot_pasos.reset_index()

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
corrida_param = params.get("corrida", [None])[0]

# ========== Si se pasa un número de corrida ==========
if corrida_param:
    corrida_str = str(corrida_param).strip()

    # Obtener nombre visible de esa corrida
    match = becas[becas['numero_corrida'].astype(str) == corrida_str]

    if not match.empty:
        nombre_visible = match['nombre_de_la_beca'].values[0]

        # Header individual
        st.markdown(f"""
        <div style="background-color:#F1F6FF;padding:20px 10px;border-radius:10px;text-align:center;">
            <h2 style="color:#0C1461;margin-bottom:0;">{nombre_visible}</h2>
            <p style="color:#444;">Reporte exclusivo generado para esta beca (corrida {corrida_str})</p>
        </div>
        """, unsafe_allow_html=True)

        # Filtrar por corrida
        beca_est = pivot_estudiantes[pivot_estudiantes['numero_corrida'].astype(str) == corrida_str]
        beca_req = pivot_requisitos[pivot_requisitos['numero_corrida'].astype(str) == corrida_str]
        beca_pasos = pivot_pasos[pivot_pasos['numero_corrida'].astype(str) == corrida_str]

        # Mostrar pestañas
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
        st.warning("⚠️ No se encontró ninguna beca con esa corrida.")

# ========== Si no se pasa parámetro, mostrar resumen general ==========
else:
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
