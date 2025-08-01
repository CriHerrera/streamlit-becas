import pandas as pd
import os

# Leer el archivo CSV desde el directorio raíz
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

# Exportar a Excel con tres hojas
target_excel = 'resumen_becas.xlsx'
with pd.ExcelWriter(target_excel) as writer:
    pivot_estudiantes.to_excel(writer, sheet_name='Estudiantes', index=False)
    pivot_requisitos.to_excel(writer, sheet_name='Requisitos', index=False)
    pivot_pasos.to_excel(writer, sheet_name='Pasos', index=False)

print(f'Archivo Excel generado: {target_excel}') 