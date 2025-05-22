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
candidates_df = pd.read_excel(candidates_file) if candidates_uploaded and str(candidates_file.name).lower().endswith('.xlsx') \
    else pd.read_csv(candidates_file) if candidates_uploaded and str(candidates_file.name).lower().endswith('.csv') \
    else dp.read_candidates(candidates_file)

comments_df = pd.read_excel(comments_file) if comments_uploaded else dp.read_comments_excel(comments_file)
template_df = dp.read_template(template_file, sheet=config.SHEET_TEMPLATE)

# --- Merge de comentarios ---
comments_map = dp.merge_comments(comments_df)

# --- Construcción de tabla final ---
def extract_linkedin(row):
    # Busca en varias columnas posibles de LinkedIn
    for col in ['14_Linkedin URL', 'Linkedin Url', 'LinkedIn', 'linkedin']:
        val = row.get(col)
        if pd.notnull(val):
            # Si es un hipervínculo de Excel (openpyxl lo puede leer como objeto), extraer string
            if hasattr(val, 'hyperlink') and val.hyperlink:
                return val.hyperlink.target
            return str(val)
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
            '14_Linkedin URL': linkedin,
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
