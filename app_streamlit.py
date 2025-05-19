# -*- coding: utf-8 -*-
"""
Created on Mon May 19 11:24:36 2025

@author: crish
"""

import pandas as pd
import streamlit as st
import os

# Paths
pathData_inputs = r"C:\Users\crish\ConsiliumBots Dropbox\ConsiliumBots\Projects\Chile\HigherEd\intermediante\becas chile"
becas = pd.read_csv(os.path.join(pathData_inputs, 'becas_procesadas_para_dash.csv'), sep=";")

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