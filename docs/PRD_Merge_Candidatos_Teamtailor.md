# PRD: App de Unificación y Exportación de Candidatos para Teamtailor

## Objetivo

Desarrollar una aplicación web en **Streamlit** que permita:
- Unificar y transformar datos de candidatos provenientes de múltiples fuentes (Excel/CSV).
- Generar un archivo final compatible con el template de importación de Teamtailor.
- Visualizar y filtrar los datos resultantes.
- Subir y validar archivos de template.
- Descargar el template generado.

---

## Entradas

### Archivos requeridos

- **Candidatos:** (ej: `Modelit_candidates_2-1.csv`)
- **Comentarios:** (ej: `Modelit_comments.xlsx`)
- **Template de importación:** (ej: `Teamtailor_Import_Template.xlsx`)

---

## Headers del CSV de Candidatos

A continuación se detallan los headers (claves) del archivo `Modelit_candidates_2-1.csv` según la inspección visual de las imágenes:

```
id,download,basic,email,headline,type,phone,address,summary,disqualified_at,disqualification_reason,disqualification_reason_description,social_profiles,created_at,stage,job,job_id,talent_pool,cover_letter,education,experience,answers,source,tags,disqualified,keyword_matches,skills,1_Country-,2_Salary Expectations,3_Source,4_Initial Salary,5_Start Day,6_Benefits,7_Comments,8_Type of Contract,9_Why was this candidate disqualified?,10_Disqualification comments,11_Company,12_Reference,13_Country,14_Linkedin URL,15_Ok from candidate,16_Level,17_English Comments,18_Available Date,19_Available Date Comments,20_Date
```

> **Nota:** Algunos campos pueden venir vacíos o contener información compuesta (por ejemplo, `social_profiles` como JSON o string).

---

## Headers del Excel de Comentarios

Del archivo `Modelit_comments.xlsx`:

```
candidate_id,id,body,created_at,member_id,attachment_id,attachment_name,rating_id
```

---

## Headers del Template a Rellenar

La hoja a rellenar del template es **Candidates** y los headers son (según la imagen):

```
Candidate Id,Email,Resume Name / CV Name,First Name,Last Name,Phone,Linkedin Url,Tags,Note 1
```

> **Nota:** En la app, solo se deben rellenar los campos requeridos según constraints y requerimientos del merge.

---

## Constraints y Lógica de Merge

### 1. Comentarios de Candidatos

- En `Modelit_comments.xlsx`, cada row tiene:
  - `candidate_id`
  - `body` (comentario)
  - `created_at` (fecha)
  - `id` (id del comentario)
- Si un candidato tiene varios comentarios, deben concatenarse en un solo string, con el siguiente formato:

  ```
  id + date: body

  id + date: body
  ```

  Ejemplo:
  ```
  59607072 2022-06-29 20:48:48.110448: Head of the team. Senior for this position.

  59395457 2022-06-27 15:41:08.746139: Busca reubicarse en Estados Unidos.
  ```

- Este string se agregará como un campo adicional (`Note 1`) en la estructura final.

---

### 2. Nombres de Candidatos

- El campo requerido en el template es `name` (que se mapea a `First Name` y `Last Name` si aplica).
- En los datos de origen (`Modelit_candidates_2-1.csv`), los nombres pueden venir:
  - Solo nombre
  - Nombre + uno o más apellidos
  - Varias combinaciones
- Reglas:
  - Si hay campos separados para nombre y apellido, concatenar ambos con espacio.
  - Si solo hay un campo, usarlo tal cual.
  - Si hay más de dos partes (ej: nombre compuesto, dos apellidos), concatenar todos los valores disponibles, respetando el orden.
  - El resultado debe ser el nombre completo, sin duplicados ni espacios extra.

---

### 3. Validaciones

- Validar que los campos requeridos estén presentes y completos en cada registro.
- Validar que el archivo template subido tenga las columnas obligatorias.
- Si se sube un archivo nuevo, actualizar la vista y la ruta de trabajo.
- Si falta algún archivo, mostrar un mensaje de error claro.
- Si algún campo clave (ej: email, id) está duplicado, advertir al usuario.

---

## Requerimientos Funcionales de la App

1. **Carga de archivos**
   - Por defecto, la app buscará los archivos en una ruta predefinida.
   - Permitir subir archivos manualmente (Excel o CSV).
   - Si se sube un archivo, usar esa ruta para procesar y renderizar.

2. **Visualización de tabla**
   - Mostrar la tabla final resultante en pantalla.
   - Incluir filtros avanzados por cualquier campo (nombre, email, tags, etc).
   - Permitir búsqueda y ordenamiento.

3. **Generación y descarga de template**
   - Botón para generar el archivo de importación (`Teamtailor_Import_Template.xlsx`) ya mergeado.
   - Validar que el archivo generado tenga el formato correcto.
   - Permitir descargar el archivo final.
   - **Nuevo requerimiento:** El botón para generar el template debe permitir seleccionar cuántas filas incluir (por ejemplo: 5 filas o todas las filas) para facilitar pruebas.

4. **Validación automática**
   - Si el archivo subido no cumple con el formato esperado, mostrar advertencia y no procesar.
   - Validar unicidad de ids y emails.

---

## Estructura de la Tabla Final

| id           | name                | email                  | phone         | download              | tags                         | 14_Linkedin URL         | comments            |
|--------------|---------------------|------------------------|---------------|-----------------------|------------------------------|-------------------------|---------------------|
| ...          | ...                 | ...                    | ...           | ...                   | ...                          | ...                     | ...                 |

---

## UX/UI

- Interfaz clara, moderna y minimalista.
- Botones grandes y claros para cargar archivos, generar template y descargar.
- Tabla con filtros tipo Excel (por columna).
- Mensajes de error y éxito visibles y descriptivos.
- **Nuevo:** Selector para elegir cuántas filas incluir al generar el template (5 filas o todas).

---

## Stack Técnico

- **Frontend y backend:** Streamlit
- **Procesamiento de datos:** pandas
- **Validación de archivos Excel:** openpyxl
- **Visualización de tablas:** Streamlit DataFrame con filtros

---

## Ejemplo de Flujo

1. El usuario entra y ve la tabla generada automáticamente con los archivos por defecto.
2. Puede cargar un nuevo archivo de candidatos, comentarios o template.
3. La tabla se actualiza y puede filtrar/buscar.
4. Puede descargar el template listo para importar en Teamtailor.
5. Puede seleccionar cuántas filas quiere exportar para pruebas.
- **Template de importación:** (ej: `Teamtailor_Import_Template.xlsx`)

### Campos requeridos para el template (ver imagen):

- `tags`
- `14_Linkedin URL`
- `id`
- `download` (nombre de archivo de CV)
- `name` (nombre completo, ver constraints)
- `email`
- `phone`

---

## Constraints y Lógica de Merge

### 1. Comentarios de Candidatos

- En `Modelit_comments.xlsx`, cada row tiene:
  - `candidate_id`
  - `body` (comentario)
  - `created_at` (fecha)
  - `id` (id del comentario)
- Si un candidato tiene varios comentarios, deben concatenarse en un solo string, con el siguiente formato:

  ```
  id + date: body

  id + date: body
  ```

  Ejemplo:
  ```
  59607072 2022-06-29 20:48:48.110448: Head of the team. Senior for this position.

  59395457 2022-06-27 15:41:08.746139: Busca reubicarse en Estados Unidos.
  ```

- Este string se agregará como un campo adicional (`comments`) en la estructura final.

---

### 2. Nombres de Candidatos

- El campo requerido en el template es `name`.
- En los datos de origen (`Modelit_candidates_2-1.csv`), los nombres pueden venir:
  - Solo nombre
  - Nombre + uno o más apellidos
  - Varias combinaciones
- Reglas:
  - Si hay campos separados para nombre y apellido, concatenar ambos con espacio.
  - Si solo hay un campo, usarlo tal cual.
  - Si hay más de dos partes (ej: nombre compuesto, dos apellidos), concatenar todos los valores disponibles, respetando el orden.
  - El resultado debe ser el nombre completo, sin duplicados ni espacios extra.

---

### 3. Validaciones

- Validar que los campos requeridos estén presentes y completos en cada registro.
- Validar que el archivo template subido tenga las columnas obligatorias.
- Si se sube un archivo nuevo, actualizar la vista y la ruta de trabajo.
- Si falta algún archivo, mostrar un mensaje de error claro.
- Si algún campo clave (ej: email, id) está duplicado, advertir al usuario.

---

## Funcionalidades de la App

1. **Carga de archivos**
   - Por defecto, la app buscará los archivos en una ruta predefinida.
   - Permitir subir archivos manualmente (Excel o CSV).
   - Si se sube un archivo, usar esa ruta para procesar y renderizar.

2. **Visualización de tabla**
   - Mostrar la tabla final resultante en pantalla.
   - Incluir filtros avanzados por cualquier campo (nombre, email, tags, etc).
   - Permitir búsqueda y ordenamiento.

3. **Generación y descarga de template**
   - Botón para generar el archivo de importación (`Teamtailor_Import_Template.xlsx`) ya mergeado.
   - Validar que el archivo generado tenga el formato correcto.
   - Permitir descargar el archivo final.

4. **Validación automática**
   - Si el archivo subido no cumple con el formato esperado, mostrar advertencia y no procesar.
   - Validar unicidad de ids y emails.

---

## Estructura de la Tabla Final

| id           | name                | email                  | phone         | download              | tags                         | 14_Linkedin URL         | comments            |
|--------------|---------------------|------------------------|---------------|-----------------------|------------------------------|-------------------------|---------------------|
| ...          | ...                 | ...                    | ...           | ...                   | ...                          | ...                     | ...                 |

---

## UX/UI

- Interfaz clara, moderna y minimalista.
- Botones grandes y claros para cargar archivos, generar template y descargar.
- Tabla con filtros tipo Excel (por columna).
- Mensajes de error y éxito visibles y descriptivos.

---

## Stack Técnico

- **Frontend y backend:** Streamlit
- **Procesamiento de datos:** pandas
- **Validación de archivos Excel:** openpyxl
- **Visualización de tablas:** Streamlit DataFrame con filtros

---

## Ejemplo de Flujo

1. El usuario entra y ve la tabla generada automáticamente con los archivos por defecto.
2. Puede cargar un nuevo archivo de candidatos, comentarios o template.
3. La tabla se actualiza y puede filtrar/buscar.
4. Puede descargar el template listo para importar en Teamtailor.
