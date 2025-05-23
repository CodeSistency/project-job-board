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
        name = dp.clean_and_concat_names(row)
        email = row.get('email')
        phone = row.get('phone')
        download = row.get('download')
        tags = row.get('tags')
        linkedin = extract_linkedin(row)
        # DEBUG: Log the input and output of extract_linkedin for first 10 rows
        if idx < 10:
            import streamlit as st
            # st.write(f"[DEBUG] Row {idx} LinkedIn raw value:", row.get('14_Linkedin URL'))
            # st.write(f"[DEBUG] Row {idx} LinkedIn extracted:", linkedin)
        # Formato de comentarios: "Comentario ID: <id> | Fecha: <fecha>\n<texto>"
        note_raw = comments_map.get(cid, '')
        if note_raw:
            note_lines = []
            for line in note_raw.split('\n\n'):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    meta, body = parts
                    meta_parts = meta.strip().split(' ', 1)
                    if len(meta_parts) == 2:
                        note_lines.append(f"📝 ID: {meta_parts[0]} | Fecha: {meta_parts[1]}\n{body.strip()}")
                    else:
                        note_lines.append(line)
                else:
                    note_lines.append(line)
            note = '\n\n'.join(note_lines)
        else:
            note = ''
        rows.append({
            'id': cid,
            'name': name,
            'email': email,
            'phone': phone,
            'download': download,
            'tags': tags,
            'linkedin_url': linkedin,
            'comments': note
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
    output = io.BytesIO()
    wb = load_workbook(template_file)
    ws = wb[config.SHEET_TEMPLATE]
    ws.delete_rows(3, ws.max_row-2)  # Borra datos anteriores, deja headers y notas
    ws.delete_rows(2, 1)  # Borra la fila de notas/instrucciones (segunda fila)
    for i, row in df.iterrows():
        ws.append(list(row.values))
    wb.save(output)
    return output.getvalue()

st.subheader("Descargar template Teamtailor listo para importar")
st.download_button(
    label="Descargar archivo Teamtailor",
    data=to_excel(filtered_df),
    file_name="Teamtailor_Import_Template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
