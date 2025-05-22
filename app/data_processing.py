"""
Funciones para el procesamiento, validación y merge de datos de candidatos y comentarios.
"""
import pandas as pd
from typing import Optional, List, Dict
import os

def read_candidates(path: str) -> pd.DataFrame:
    """Lee el archivo de candidatos (CSV o XLSX) y retorna un DataFrame."""
    if path.lower().endswith('.csv'):
        return pd.read_csv(path)
    elif path.lower().endswith('.xlsx'):
        return pd.read_excel(path)
    else:
        raise ValueError(f"Formato de archivo no soportado: {path}")

def read_comments_excel(path: str) -> pd.DataFrame:
    """Lee el archivo de comentarios Excel y retorna un DataFrame."""
    return pd.read_excel(path)

def read_template(path: str, sheet: str = 'Candidates') -> pd.DataFrame:
    """Lee la hoja 'Candidates' del template y retorna un DataFrame."""
    return pd.read_excel(path, sheet_name=sheet)

def merge_comments(comments_df: pd.DataFrame) -> Dict:
    """
    Agrupa y concatena comentarios por candidate_id en el formato requerido.
    Retorna un dict: {candidate_id: comentarios_concatenados}
    """
    result = {}
    grouped = comments_df.groupby('candidate_id')
    for cid, group in grouped:
        comentarios = []
        for _, row in group.iterrows():
            comentarios.append(f"{row['id']} {row['created_at']}: {row['body']}")
        result[cid] = '\n\n'.join(comentarios)
    return result

def clean_and_concat_names(row: pd.Series) -> str:
    """
    Concatena y limpia nombres y apellidos según reglas del PRD.
    """
    parts = []
    # Ajustar según los nombres de columnas en el CSV
    for col in ['name', 'lastname', 'basic', 'First Name', 'Last Name']:
        if col in row and pd.notnull(row[col]):
            parts.append(str(row[col]).strip())
    return ' '.join(parts).replace('  ', ' ')

# Más funciones a agregar según avance del desarrollo
