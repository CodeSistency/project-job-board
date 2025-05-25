"""
Componentes de interfaz Streamlit para la app de candidatos.
"""
import streamlit as st
import pandas as pd
from typing import Optional

def show_table(df: pd.DataFrame, filters: bool = True):
    """Muestra una tabla con filtros avanzados."""
    if filters:
        st.dataframe(df, use_container_width=True)
    else:
        st.table(df)

def file_uploader(label: str, type: Optional[list] = None, key: Optional[str] = None):
    """Componente para subir archivos."""
    return st.file_uploader(label, type=type, key=key)

def row_selector(df: pd.DataFrame):
    """Permite seleccionar cuántas filas mostrar/exportar."""
    base_options = [5, 10, 15, 25, 50, 100]
    max_rows = len(df)
    valid_options = [opt for opt in base_options if opt < max_rows] + [max_rows]
    choice = st.selectbox(
        '¿Cuántas filas quieres exportar?',
        valid_options,
        format_func=lambda x: f"{x} filas" if x != max_rows else "Todas las filas"
    )
    if choice == max_rows:
        st.info(f"Estás mostrando/exportando todas las filas ({max_rows} filas). Si el archivo exportado no abre, puede ser demasiado grande para Excel o tu sistema.")
    else:
        st.write(f"Mostrando/exportando las primeras {choice} filas de {max_rows}.")
    return df.head(choice) if choice != max_rows else df
