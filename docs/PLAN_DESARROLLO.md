# Plan de Desarrollo: App de Unificación y Exportación de Candidatos

## 1. Inicialización del Proyecto

- Crear un repositorio Git privado/publico y definir ramas principales (`main`, `dev`).
- Definir un archivo `README.md` con descripción, requerimientos y pasos de instalación.
- Crear un entorno virtual (`venv` o `conda`) para aislar dependencias.
- Añadir un archivo `.gitignore` para excluir archivos temporales, de entorno, y datos sensibles.

---

## 2. Estructura del Proyecto

```
/project-root
│
├── app/                    # Código fuente principal de la app Streamlit
│   ├── __init__.py
│   ├── data_processing.py  # Funciones para merge, validaciones, etc.
│   ├── ui.py               # Componentes de interfaz Streamlit
│   └── config.py           # Configuración de rutas, constantes, etc.
│
├── tests/                  # Pruebas unitarias y de integración
│   ├── __init__.py
│   └── test_data_processing.py
│
├── data/                   # Archivos de entrada/salida por defecto (no versionar datos reales)
│
├── requirements.txt        # Dependencias del proyecto
├── README.md
├── .gitignore
└── PRD_Merge_Candidatos_Teamtailor.md
```

---

## 3. Desarrollo Iterativo y Buenas Prácticas

### A. Procesamiento de Datos
- Implementar funciones modulares para:
  - Leer y validar archivos de entrada (candidatos, comentarios, template).
  - Realizar el merge según constraints.
  - Normalizar y limpiar datos (nombres, emails, tags, comentarios).
  - Validar unicidad y formato de campos clave.
- Añadir pruebas unitarias para cada función crítica.

### B. Interfaz de Usuario (Streamlit)
- Crear prototipo básico con carga de archivos y visualización de tabla.
- Añadir filtros avanzados y búsqueda por columna.
- Implementar el selector de filas para exportar (5 o todas).
- Añadir mensajes claros de error/éxito.
- Respetar principios de UX/UI: interfaz clara, botones bien identificados, feedback inmediato.

### C. Generación y Validación del Template
- Automatizar la generación del archivo Excel de salida.
- Validar que la hoja y columnas sean correctas antes de permitir la descarga.
- Permitir la descarga directa desde la app.

### D. Subida y Validación de Archivos
- Permitir subir archivos nuevos y actualizar la vista.
- Validar formato y estructura antes de procesar los datos.

---

## 4. Control de Calidad y Testing

- Escribir tests para:
  - Validación de formatos de entrada.
  - Merge correcto de datos y comentarios.
  - Exportación del template.
- Usar `pytest` o similar para automatización.
- Revisar edge cases: datos faltantes, duplicados, formatos incorrectos.

---

## 5. Documentación y Soporte

- Mantener actualizado el `README.md` con instrucciones claras.
- Documentar funciones y módulos con docstrings.
- Añadir ejemplos de uso y troubleshooting común.

---

## 6. Despliegue y Entrega

- Probar la app localmente y en entorno limpio.
- (Opcional) Publicar la app en Streamlit Cloud o servidor propio para pruebas de usuario.
- Validar con usuarios finales el flujo y la exportación del template.

---

## 7. Iteración y Feedback

- Recoger feedback de usuarios y stakeholders.
- Priorizar mejoras y bugs en issues del repositorio.
- Iterar en sprints cortos para entregar valor incremental.

---

### Checklist de Buenas Prácticas

- [ ] Código modular y reutilizable.
- [ ] Validaciones robustas y mensajes claros.
- [ ] Pruebas unitarias y de integración.
- [ ] Documentación clara y actualizada.
- [ ] Control de versiones y ramas limpias.
- [ ] Interface intuitiva y amigable.
