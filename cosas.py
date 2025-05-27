!pip install weasyprint

import os
import pandas as pd
from jinja2 import Template
from weasyprint import HTML
import matplotlib.pyplot as plt
import base64
from pathlib import Path
import io
import streamlit as st

from google.colab import drive
drive.mount('/content/drive')

# # Definir la ruta base de manera dinámica según el sistema operativo
# if os.name == "nt":  # Windows
#     base_path = Path("H:/") / ".shortcut-targets-by-id" / "1NKxw_hiPlQ0qbxXaqHTPvxaeEm_H_qAg" / "Reportes_mensajeria_tether"
# elif os.getenv("USER") == "Valentina":  # Ruta específica para Valentina
#     base_path = Path.home() / "Library" / "CloudStorage" / "GoogleDrive-valentinahurtado@consiliumbots.com" / "My Drive" / "Reportes_mensajeria_tether"
# else:  # Mac/Linux general
#     base_path = Path.home() / "Library" / "CloudStorage" / "GoogleDrive-leidy@tether.education" / "My Drive" / "Reportes_mensajeria_tether"

## pruebas vale##
from pathlib import Path

base_path = Path("/content/drive/MyDrive/Tether")
base_path_inputs = base_path / "inputs"
base_path_outputs = base_path / "outputs"

# 📌 Ruta del logo de TETHER
ruta_logo = base_path_inputs / "assets" / "TETHER.png"
ruta_check = base_path_inputs / "assets" / "ok.png"

# 📌 Función para convertir la imagen a Base64
def convertir_imagen_base64(ruta_logo):
    """Convierte una imagen a formato Base64 para incrustarla en el HTML."""
    with open(ruta_logo, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# 📌 Convertir logo a Base64
logo_base64 = convertir_imagen_base64(ruta_logo)

def convertir_imagen_base64(ruta):
    with open(ruta, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

check_base64 = convertir_imagen_base64(ruta_check)

# 📌 Cargar el CSV asegurando que la columna 'user' sea tratada como texto
df = pd.read_csv(
    base_path_inputs / "estadisticas_completitud_dummys.csv"
   ).head(20)

#Carga con los grados
df_panel_grade = pd.read_csv(base_path_inputs / "panel_grade.csv")

# Asegura que ambos códigos sean strings
df["campus_code"] = df["campus_code"].astype(str)
df_panel_grade["campusId"] = df_panel_grade["campusId"].astype(str)



# 📌 Crear carpeta para almacenar los PDFs
output_folder = base_path_outputs / "reportes_colegios"
os.makedirs(output_folder, exist_ok=True)

# 📌 Obtener la lista única de colegios
#schools = df["school"].dropna().unique()


def generar_imagen_base64_grafico(df_panel, campus_code):
    import matplotlib.pyplot as plt
    import io
    import base64

    df_filtrado = df_panel[df_panel["campusId"] == campus_code]

    if df_filtrado.empty:
        return None

    # Renombrar grados
    df_filtrado = df_filtrado.copy()
    df_filtrado["grado_limpio"] = df_filtrado["gradetrack_name"].replace({
        "1er nivel de Transición (Pre-kínder)": "Prekínder",
        "2do nivel de Transición (Kínder)": "Kínder"
    })

    # Orden de grados deseado
    orden_grados = [
        "1° básico", "2° básico", "3° básico",
        "4° básico", "5° básico", "6° básico", "7° básico", "8° básico"
    ]
    conteo = df_filtrado["grado_limpio"].value_counts().reindex(orden_grados, fill_value=0)

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(6.5, 4), facecolor="#eaefff")
    ax.bar(conteo.index, conteo.values, color="#0C1461")

    ax.set_title("Matrícula por grado", fontsize=14, fontweight='bold')
    ax.set_xlabel("Grado", fontsize=12)
    ax.set_ylabel("Cantidad de estudiantes", fontsize=12)
    ax.tick_params(axis='x', rotation=30)
    ax.set_facecolor("#eaefff")
    fig.patch.set_facecolor("#eaefff")
    ax.grid(axis='y', linestyle="--", alpha=0.3)

    # Texto de total
    total_alumnos = conteo.sum()
    ax.text(
        0.5, -0.15,
        f"Total estudiantes: {total_alumnos}",
        ha='center',
        va='center',
        transform=ax.transAxes,
        fontsize=10,
        color="#333"
    )

    plt.tight_layout()

    # Exportar imagen
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Informe Colegio - {{ school_name }}</title>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Inter:wght@300;400;500;600&display=swap');

        body {
            font-family: 'Inter', sans-serif;
            background-color: #eaefff;
            margin: 0;
            padding: 0;
        }

        .page-content {
            padding: 40px 60px;
        }

        h1, h2, h3 {
            font-family: 'DM Sans', sans-serif;
            color: black;
        }

        .header h1 {
            color: white;
        }

        .logo-container {
            position: absolute;
            top: 15px;
            right: 20px;
        }

        .logo-container img {
            width: 100px;
        }

        .header {
            background-color: #0C1461;
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            position: relative;
            margin-top: 50px;
        }

        .table-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th {
            background-color: #5DDBDB;
            color: white;
            padding: 10px;
        }

        td {
            padding: 8px;
            border: 1px solid #BDC3C7;
        }

        .small-text {
            font-size: 12px;
        }
          .bar {
    width: 100%;
    background-color: #ddd;
    border-radius: 8px;
    margin-bottom: 10px;
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

body {
    font-family: 'Inter', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif;
}


    </style>
</head>
<body>

<div class="logo-container">
    <img src="data:image/png;base64,{{ logo_base64 }}" alt="Logo TetherEd">
</div>

<div class="page-content">
    <div class="header">
        <h1>Informe Avance Colegio {{ school_name }}</h1>
    </div>

    <p style="text-align: justify;">
        El objetivo principal de esta iniciativa es asegurar la digitalización del proceso de matrícula, una reposición rápida de vacantes y una interacción constante y transparente con las familias, permitiendo que estas puedan matricular 24/7 de forma remota y conforme a los lineamientos de la Superintendencia.
    </p>

    <h2>Estado actual del proceso</h2>
    <p style="text-align: justify;">
        A continuación dejamos una tabla con todos los indicadores que podemos ver desde la plataforma y a los cuales tenemos acceso:
    </p>

   <table>
    <tr>
        <th>Proceso de Admisión</th>
        <th>Cantidad de Estudiantes</th>
        <th>Porcentaje</th>
    </tr>
    {% for fila in estado_admision %}
    <tr>
        <td>{{ fila['Proceso'] }}</td>
        <td>{{ fila['Cantidad'] }}</td>
        <td>{{ fila['Porcentaje'] }}</td>
    </tr>
    {% endfor %}
</table>



<h2>Completitud de información</h2>
<p>Porcentaje de estudiantes matriculados que cuentan con la siguiente información:</p>

{% for fila in completitud %}
<div class="bar-row">
    <span class="bar-label">{{ fila['Información'] }} ({{ fila['Porcentaje Completado'] }})</span>
    <div class="bar">
        <div class="bar-fill" style="width: {{ fila['Porcentaje Completado'] }};"></div>
    </div>
</div>
{% endfor %}


<h2>Resumen de Participación</h2>
<p style="text-align: justify;">
    Estado de avance en los pasos clave del acompañamiento al colegio:
</p>

<ul>
    {% for item in participacion %}
    <li>{{ item['estado']|safe }} {{ item['texto'] }}</li>
    {% endfor %}
</ul>

<h2>Matrícula por grado</h2>
<p>Distribución de estudiantes matriculados según nivel:</p>

{% for fila in grafico_grados %}
<div style="margin-bottom: 12px;">
  <strong>{{ fila['Grado'] }}</strong> - {{ fila['Cantidad'] }} estudiantes
  <div style="background: #eee; border-radius: 8px; height: 20px; margin-top: 4px;">
    <div style="background: #5DDBDB; height: 100%; width: {{ fila['Porcentaje'] }}%; border-radius: 8px; transition: width 1s;"></div>
  </div>
</div>
{% endfor %}

{% if grafico_base64 %}
<h2>Matrícula por grado</h2>
<img src="data:image/png;base64,{{ grafico_base64 }}" style="width: 100%; max-width: 500px; height: auto;" />
{% endif %}



</body>
</html>"""

# 📌 Función: participación tipo lista
def generar_lista_participacion(fila, check_base64):
    img_ok = f'<img src="data:image/png;base64,{check_base64}" style="width: 14px; height: 14px; object-fit: contain; vertical-align: middle; margin-right: 4px;">'
    return [
        {"texto": "Comunicación de intención de colaboración", "estado": img_ok if int(fila["colegio_notificado_colaboracion"]) == 1 else "[Pendiente]"},
        {"texto": "Acuerdo firmado", "estado": img_ok if int(fila["colegio_firmo_compromisos"]) == 1 else "[Pendiente]"},
        {"texto": "Base de datos recibida", "estado": img_ok if int(fila["colegio_envio_base"]) == 1 else "[Pendiente]"},
        {"texto": "QR enviado a apoderados para validación de datos", "estado": img_ok if int(fila["napsis"]) == 1 else "[Pendiente]"},
    ] + ([{"texto": "Información previa disponible desde Napsis", "estado": img_ok}]
         if int(fila["napsis"]) == 1 else [])

# 📌 Función: barras de completitud
def generar_tabla_completitud(fila):
    info_map = {
        "Primer Nombre del Estudiante": "admission-completed_with_student_first_name",
        "Género del Estudiante": "admission-completed_with_student_gender",
        "Nombre del Apoderado": "admission-completed_with_legalguardian_first_name",
        "Teléfono del Apoderado": "admission-completed_with_legalguardian_cellphone",
        "Correo del Apoderado": "admission-completed_with_legalguardian_email",
        "RUT del Apoderado": "admission-completed_with_legalguardian_id_number",
        "Dirección del Apoderado": "admission-completed_with_Dirección Apoderado",
        "Ciudad del Apoderado": "admission-completed_with_Ciudad Apoderado",
        "Fecha de Nacimiento del Estudiante": "admission-completed_with_Fecha de Nacimiento estudiante"
    }

    total = fila["admission-completed_total"]
    tabla = []
    for descripcion, col in info_map.items():
        completado = fila[col]
        pct_completo_val = round(completado / total * 100) if total else 0
        pct_incompleto = 100 - pct_completo_val
        tabla.append({
            "Información": descripcion,
            "Total Completado": int(completado),
            "Porcentaje Completado": f"{pct_completo_val}%",
            "Porcentaje Incompleto": f"{pct_incompleto}%"
        })
    return tabla

# 📌 Función: tabla vertical del estado de admisión
def generar_estado_admision(fila):
    total = fila["admission-completed_total"]

    def safe_int(val):
        return int(val) if pd.notna(val) else 0

    def safe_pct(val):
        return round(val / total * 100) if total and pd.notna(val) else 0

    return [
        {
            "Proceso": "Matrícula completada SAE",
            "Cantidad": safe_int(fila["Admisión Escolar (SAE) Ingreso 2025_admission-completed"]),
            "Porcentaje": f"{safe_pct(fila['Admisión Escolar (SAE) Ingreso 2025_admission-completed'])}%"
        },
        {
            "Proceso": "Matrícula completada AEL",
            "Cantidad": safe_int(fila["Anótate en la Lista 2025_admission-completed"]),
            "Porcentaje": f"{safe_pct(fila['Anótate en la Lista 2025_admission-completed'])}%"
        },
        {
            "Proceso": "Matrícula extraordinaria",
            "Cantidad": safe_int(fila["Admision Extraordinaria 2025_admission-completed"]),
            "Porcentaje": f"{safe_pct(fila['Admision Extraordinaria 2025_admission-completed'])}%"
        },
        {
            "Proceso": "Total de matrículas completadas",
            "Cantidad": int(total),
            "Porcentaje": "100%"
        }
    ]


# 📌 Función principal para generar el PDF
def generar_grafico_grado(df_panel, campus_code):
    df_filtrado = df_panel[df_panel["campusId"] == campus_code]
    total = len(df_filtrado)
    grafico = []

    for grado, grupo in df_filtrado.groupby("gradetrack_name"):
        count = len(grupo)
        pct = (count / total) * 100 if total else 0
        grafico.append({
            "Grado": grado,
            "Cantidad": count,
            "Porcentaje": round(pct, 2)
        })

    return grafico


def generate_pdf_for_school(school_name, school_df):
    total_messages = len(school_df)
    fila = school_df.iloc[0]

    completitud = generar_tabla_completitud(fila)
    participacion_info = generar_lista_participacion(fila, check_base64)
    estado_admision = generar_estado_admision(fila)
    codigo_del_colegio = fila["campus_code"]
    grafico_grados = generar_grafico_grado(df_panel_grade, codigo_del_colegio)
    grafico_base64 = generar_imagen_base64_grafico(df_panel_grade, codigo_del_colegio)


    colegios_info = school_df[[
        'campus_code',
        'nombre_colegio',
        'Admisión Escolar (SAE) Ingreso 2025_admission-completed',
        'Anótate en la Lista 2025_admission-completed',
        'admission-completed_total'
    ]].drop_duplicates().to_dict(orient='records')

    template = Template(html_template)
    html_out = template.render(
        school_name=school_name,
        logo_base64=logo_base64,
        total_messages=total_messages,
        colegios=colegios_info,
        participacion=participacion_info,
        completitud=completitud,
        estado_admision=estado_admision,
        grafico_grados=grafico_grados,
        grafico_base64=grafico_base64
    )

    print(f"[{school_name}] Alumnos en panel: {len(df_panel_grade[df_panel_grade['campusId'] == codigo_del_colegio])}")


    output_path = output_folder / f"Reporte_{school_name.replace('/', '_')}.pdf"
    HTML(string=html_out, base_url=os.getcwd()).write_pdf(output_path)
    print(f"✅ PDF generado para {school_name} en {output_path}")
    
# Leer parámetro de la URL (SOLO NUEVA API)
selected_school = st.query_params.get("colegio", None)

if not selected_school:
    # Página principal: lista de botones
    st.markdown(
        """
        <div style="background-color:#0C1461;padding:20px;border-radius:10px;text-align:center;">
            <h1 style="color:white;font-family: 'DM Sans', sans-serif;">Reportes de Colegios</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("### Seleccione un colegio para ver su reporte:")
    for school in df["nombre_colegio"].dropna().unique():
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
    
    # Botón para volver a la lista principal
    if st.button("⬅️ Volver a la lista de colegios"):
        st.query_params.clear()
        st.rerun()
    
    # ... (resto del código del reporte)
