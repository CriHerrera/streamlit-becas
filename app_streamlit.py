import streamlit as st
import importlib
import os
import pandas as pd
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Reportes de Colegios",
    page_icon="📊",
    layout="wide"
)

# Cargar datos para la portada
base_path = Path(__file__).parent.resolve()
base_path_inputs = base_path / "inputs"
df = pd.read_csv(base_path_inputs / "estadisticas_completitud_dummys.csv")
schools = df["nombre_colegio"].dropna().unique()

# Sidebar para seleccionar sección
secciones = ["Colegios"]  # Puedes agregar más secciones aquí
seccion = st.sidebar.selectbox("Selecciona una sección", secciones)

if seccion == "Colegios":
    selected_school = st.query_params.get("colegio", None)
    if not selected_school:
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
        colegios = importlib.import_module("secciones.colegios")
        colegios.mostrar(selected_school)

