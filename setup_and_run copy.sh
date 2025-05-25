#!/bin/bash
# Instala dependencias y ejecuta la app Streamlit
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run main.py
