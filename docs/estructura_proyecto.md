# 📂 Estructura del Proyecto - Simulador de Proyectos con Riesgo y EVM

Este documento describe la organización de carpetas y archivos del proyecto, así como el propósito de cada uno.  
El objetivo es mantener el orden, facilitar el trabajo en paralelo y evitar confusiones al integrar.

---

---

## 📌 Descripción por archivo/carpeta

### 1. `app.py`

- **Rol:** Controlador principal de la aplicación Streamlit.
- **Contenido:** Carga de páginas, manejo de navegación, llamado a funciones de lógica (Monte Carlo y EVM) y visualización de resultados.

### 2. Carpeta `ui.py/`

- **Rol:** Funciones reutilizables de interfaz gráfica.
- **Contenido:** Formularios, botones, tablas, gráficos, widgets y otros elementos que se usan en distintas partes de la app.

### 3. `montecarlo.py`

- **Rol:** Lógica de simulación de proyectos con incertidumbre usando el método de Monte Carlo.
- **Contenido:** Funciones para procesar las actividades, generar duraciones/costos aleatorios, calcular distribuciones y promedios.

### 4. `evm.py`

- **Rol:** Cálculo de métricas de Valor Ganado (EVM).
- **Contenido:** Funciones para calcular PV, EV, AC, SPI, CPI, EAC, ETC y estados de avance.

### 5. `models.py`

- **Rol:** Definir los **formatos estándar de datos** en JSON para que todos los módulos sean compatibles.
- **Contenido:** Diccionarios o modelos que actúan como plantillas para entradas y salidas.

### 6. Carpeta `data/`

- **Rol:** Guardar ejemplos reales para pruebas e integración, sin necesidad de estar ingresandolos manualmente.
- **Archivos:**
  - `project_input.json` → Actividades del proyecto.
  - `montecarlo_output.json` → Resultados de simulación.
  - `evm_input.json` → Avances y costos reales.
  - `evm_output.json` → Métricas calculadas.
  - `visualization.json` → Datos listos para gráficos.

### 7. Carpeta `docs/`

- **Rol:** Documentación interna del proyecto.
- **Archivos:**
  - `estructura_proyecto.md` → Este documento.

### 8. `requirements.txt`

- **Rol:** Lista de dependencias necesarias para correr el proyecto.
- **Modo de uso:**
  - `Comando para alimentarlo` → pip freeze > requirements.txt
  - `Comando para instalar dependencias` → pip install -r requirements.txt

### 9. `file_utils.py`

- **Rol:** Manejo de archivos
- **Contenido:** Funciones para guardar JSON y CSV; convertir CSV a JSON
