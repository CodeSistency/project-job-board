import streamlit as st
import pandas as pd
import os
from app import data_processing as dp
from app import ui
from app import config

st.set_page_config(page_title="Unificación de Candidatos Teamtailor", layout="wide")
st.title("Unificación y Exportación de Candidatos para Teamtailor")

# --- Carga de archivos ---
def get_file(path, file_uploader_label, type, key):
    uploaded = ui.file_uploader(file_uploader_label, type=type, key=key)
    if uploaded:
        return uploaded, True
    elif os.path.exists(path):
        return path, False
    else:
        st.warning(f"No se encontró el archivo por defecto en {path} y no se ha subido ninguno.")
        return None, False

candidates_file, candidates_uploaded = get_file(config.DEFAULT_CANDIDATES_PATH, "Sube archivo de candidatos (CSV)", ["csv"], "cand")
comments_file, comments_uploaded = get_file(config.DEFAULT_COMMENTS_PATH, "Sube archivo de comentarios (XLSX)", ["xlsx"], "comm")
template_file, template_uploaded = get_file(config.DEFAULT_TEMPLATE_PATH, "Sube template Teamtailor (XLSX)", ["xlsx"], "templ")

if not all([candidates_file, comments_file, template_file]):
    st.stop()

# --- Procesamiento de datos ---
import streamlit as st
if candidates_uploaded and str(candidates_file.name).lower().endswith('.xlsx'):
    candidates_df = pd.read_excel(candidates_file)
elif candidates_uploaded and str(candidates_file.name).lower().endswith('.csv'):
    candidates_df = pd.read_csv(candidates_file, sep=',', engine='python')
else:
    candidates_df = dp.read_candidates(candidates_file)


comments_df = pd.read_excel(comments_file) if comments_uploaded else dp.read_comments_excel(comments_file)
template_df = dp.read_template(template_file, sheet=config.SHEET_TEMPLATE)

# --- Merge de comentarios ---
comments_map = dp.merge_comments(comments_df)

# --- Construcción de tabla final ---
import json

def extract_linkedin(row):
    # Buscar primero columnas extraídas
    extracted_cols = [c for c in row.index if c.lower().replace(' ', '').startswith('linkedin') and c.endswith('_Extracted')]
    for col in extracted_cols:
        val = row.get(col)
        if pd.notnull(val):
            return str(val)
    # Si no, buscar en las columnas originales
    for col in ['14_Linkedin URL', 'Linkedin Url', 'LinkedIn', 'linkedin']:
        val = row.get(col)
        if pd.notnull(val):
            # Si es un hipervínculo de Excel (openpyxl lo puede leer como objeto), extraer string
            if hasattr(val, 'hyperlink') and val.hyperlink:
                return val.hyperlink.target
            # Si es un string JSON, intentar extraer el campo 'uri'
            val_str = str(val)
            if val_str.strip().startswith('{'):
                try:
                    js = json.loads(val_str)
                    if 'uri' in js:
                        return js['uri']
                except Exception:
                    pass
            return val_str
    return ''

def build_final_table(candidates_df, comments_map):
    rows = []
    for idx, row in candidates_df.iterrows():
        cid = row.get('id')
        # Split name into first and last for the template
        name = dp.clean_and_concat_names(row)
        first_name = ''
        last_name = ''
        if name:
            parts = name.strip().split()
            if len(parts) == 1:
                first_name = parts[0]
                last_name = ''
            elif len(parts) == 2:
                first_name = parts[0]
                last_name = parts[1]
            elif len(parts) == 3:
                first_name = ' '.join(parts[:2])
                last_name = parts[2]
            else:  # 4 or more
                first_name = ' '.join(parts[:2])
                last_name = ' '.join(parts[-2:])
        email = row.get('email')
        phone = row.get('phone')
        download = row.get('download')  # Resume Name / CV Name
        tags = row.get('tags')
        linkedin = extract_linkedin(row)
        note_raw = comments_map.get(cid, '')
        note = note_raw if note_raw else ''
        # Build row in the exact Teamtailor template order:
        rows.append({
            'Candidate Id': cid,
            'Email': email,
            'Resume Name / CV Name': download,
            'First Name': first_name,
            'Last Name': last_name,
            'Phone': phone,
            'Linkedin Url': linkedin,
            'Tags': tags,
            'Note 1': note
        })
    return pd.DataFrame(rows)



final_df = build_final_table(candidates_df, comments_map)

# --- Selección de filas a exportar ---
st.subheader("Vista previa de la tabla final")
filtered_df = ui.row_selector(final_df)
ui.show_table(filtered_df)

# --- Botón para descargar template ---
def to_excel(df):
    import io
    from openpyxl import load_workbook
    import pandas as pd
    import numpy as np
    # Clean DataFrame: fill NaN/None, convert all to string, and remove invalid XML characters
    import re
    def clean_xml_chars(val):
        if not isinstance(val, str):
            val = str(val)
        # Remove all control characters except tab, CR, LF, and only allow valid XML unicode ranges
        return re.sub(r'[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD]', '', val)
    df_clean = df.fillna('').replace({None: ''})
    df_clean = df_clean.astype(str)
    df_clean = df_clean.applymap(clean_xml_chars)

    # Load template and get headers
    wb = load_workbook(template_file)
    ws = wb.active
    template_headers = [cell.value for cell in ws[1]]
    df_headers = list(df_clean.columns)
    if template_headers != df_headers:
        raise ValueError(f"DataFrame headers do not match template headers.\nDataFrame: {df_headers}\nTemplate: {template_headers}")

    # Remove previous data (keep headers)
    ws.delete_rows(3, ws.max_row-2)  # Borra datos anteriores, deja headers y notas
    ws.delete_rows(2, 1)  # Borra la fila de notas/instrucciones (segunda fila)

    # Append data row by row
    for _, row in df_clean.iterrows():
        ws.append(list(row.values))
    # Save to in-memory bytes
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

# Streamlit download button for normal export
excel_bytes = to_excel(filtered_df)
if excel_bytes:
    st.download_button(
        label="Descargar Excel exportado",
        data=excel_bytes,
        file_name="Teamtailor_Export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
#     file_name="Teamtailor_Import_Template.xlsx",
#     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# )
