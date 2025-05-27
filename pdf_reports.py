import os
import pandas as pd
from jinja2 import Template
from weasyprint import HTML
import matplotlib.pyplot as plt
import base64
from pathlib import Path
import io

def convertir_imagen_base64(ruta):
    """Convierte una imagen a formato Base64 para incrustarla en el HTML."""
    with open(ruta, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def generar_imagen_base64_grafico(df_panel, campus_code):
    """Genera un gráfico de barras para la distribución de grados."""
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

def generar_lista_participacion(fila, check_base64):
    """Genera la lista de participación con estados."""
    img_ok = f'<img src="data:image/png;base64,{check_base64}" style="width: 14px; height: 14px; object-fit: contain; vertical-align: middle; margin-right: 4px;">'
    return [
        {"texto": "Comunicación de intención de colaboración", "estado": img_ok if int(fila["colegio_notificado_colaboracion"]) == 1 else "[Pendiente]"},
        {"texto": "Acuerdo firmado", "estado": img_ok if int(fila["colegio_firmo_compromisos"]) == 1 else "[Pendiente]"},
        {"texto": "Base de datos recibida", "estado": img_ok if int(fila["colegio_envio_base"]) == 1 else "[Pendiente]"},
        {"texto": "QR enviado a apoderados para validación de datos", "estado": img_ok if int(fila["napsis"]) == 1 else "[Pendiente]"},
    ] + ([{"texto": "Información previa disponible desde Napsis", "estado": img_ok}]
         if int(fila["napsis"]) == 1 else [])

def generar_tabla_completitud(fila):
    """Genera la tabla de completitud de información."""
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

def generar_estado_admision(fila):
    """Genera el estado de admisión."""
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

def generar_grafico_grado(df_panel, campus_code):
    """Genera el gráfico de distribución por grado."""
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

def generate_pdf_for_school(school_name, school_df, df_panel_grade, output_folder, logo_base64, check_base64, html_template):
    """Genera el PDF para un colegio específico."""
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

    output_path = output_folder / f"Reporte_{school_name.replace('/', '_')}.pdf"
    HTML(string=html_out, base_url=os.getcwd()).write_pdf(output_path)
    return output_path 