import streamlit as st
import pandas as pd
from pathlib import Path
from pdf_reports import (
    convertir_imagen_base64,
    generar_tabla_completitud,
    generar_lista_participacion,
    generar_estado_admision,
    generar_grafico_grado,
    generar_imagen_base64_grafico
)

def mostrar(selected_school):
    if not selected_school:
        return
    base_path = Path(__file__).parent.parent.resolve()
    base_path_inputs = base_path / "inputs"
    df = pd.read_csv(base_path_inputs / "estadisticas_completitud_dummys.csv")
    df_panel_grade = pd.read_csv(base_path_inputs / "panel_grade.csv")
    logo_base64 = convertir_imagen_base64(base_path_inputs / "assets" / "TETHER.png")
    check_base64 = convertir_imagen_base64(base_path_inputs / "assets" / "ok.png")

    df_school = df[df["nombre_colegio"] == selected_school]
    if df_school.empty:
        st.error(f"No se encontraron datos para el colegio {selected_school}")
        st.stop()
    fila = df_school.iloc[0]
    codigo_del_colegio = fila["campus_code"]
    st.markdown(
        f'<div style="position: absolute; top: 10px; right: 10px;"><img src="data:image/png;base64,{logo_base64}" width="100"></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div class="header">
            <h1>Informe Avance Colegio {selected_school}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    El objetivo principal de esta iniciativa es asegurar la digitalización del proceso de matrícula, 
    una reposición rápida de vacantes y una interacción constante y transparente con las familias, 
    permitiendo que estas puedan matricular 24/7 de forma remota y conforme a los lineamientos de la Superintendencia.
    """)
    st.markdown(
        "A continuación dejamos una tabla con todos los indicadores que podemos ver desde la plataforma y a los cuales tenemos acceso:"
    )
    estado_admision = generar_estado_admision(fila)
    estado_df = pd.DataFrame(estado_admision)
    st.dataframe(estado_df, use_container_width=True, hide_index=True)
    st.markdown("### Completitud de información")
    st.markdown(
        "Porcentaje de estudiantes matriculados que cuentan con la siguiente información:"
    )
    completitud = generar_tabla_completitud(fila)
    for item in completitud:
        st.markdown(f"""
            <div class=\"bar-row\">
                <span class=\"bar-label\">{item['Información']} ({item['Porcentaje Completado']})</span>
                <div class=\"bar\">
                    <div class=\"bar-fill\" style=\"width: {item['Porcentaje Completado'].strip('%')}%\"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("### Resumen de Participación")
    participacion = generar_lista_participacion(fila, check_base64)
    for item in participacion:
        st.markdown(f"{item['estado']} {item['texto']}", unsafe_allow_html=True)
    st.markdown("### Matrícula por grado")
    grafico_grados = generar_grafico_grado(df_panel_grade, codigo_del_colegio)
    for grado in grafico_grados:
        st.markdown(f"""
            <div class=\"bar-row\">
                <span class=\"bar-label\">{grado['Grado']} ({grado['Cantidad']} estudiantes)</span>
                <div class=\"bar\">
                    <div class=\"bar-fill\" style=\"width: {grado['Porcentaje']}%\"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    grafico_base64 = generar_imagen_base64_grafico(df_panel_grade, codigo_del_colegio)
    if grafico_base64:
        st.markdown("### Distribución de matrícula por grado")
        st.image(f"data:image/png;base64,{grafico_base64}", use_container_width=True) 