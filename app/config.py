"""
Configuración de rutas y constantes de la app.
Todas las rutas son relativas al directorio raíz del proyecto.
"""
import os

# Directorio base del proyecto (un directorio arriba de app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directorio para archivos de datos
DATA_DIR = os.path.join(BASE_DIR, 'test-data')

# Rutas a los archivos por defecto
DEFAULT_CANDIDATES_PATH = os.path.join(DATA_DIR, 'Modelit_candidates_2-1.csv')
DEFAULT_COMMENTS_PATH = os.path.join(DATA_DIR, 'Modelit_comments.xlsx')
DEFAULT_TEMPLATE_PATH = os.path.join(DATA_DIR, 'Teamtailor_Import_Template.xlsx')

# Configuración de hojas
SHEET_TEMPLATE = "Candidates"

# Asegurar que el directorio de datos exista
os.makedirs(DATA_DIR, exist_ok=True)