# Simulador de Proyectos con Riesgo y EVM

Este proyecto consiste en un simulador web para el cumplimiento, métricas y desarrollo de proyectos. A continuación se detallan los pasos que deberá seguir para poder hacer uso del aplicativo y la instalación de las dependencias necesarias. De igual forma, se brinda una breve descripción del proyecto, recursos adicionales que puedan ser valioso y contacto

## Preparación del ambiente, instalación de dependencias y ejecución del aplicativo

1. Se recomienda tener instalado un ambiente de python. Cualquier versión superior a la 3.0.0 es funcional. En caso de no tener instalado un ambiente, utilizar la siguiente documentación para poder hacer el setup: [PYTHON](https://www.python.org/downloads/)
2. Con el ambiente listo para python, ejecutar el siguiente comando desde el directorio raíz del proyecto para instalar las dependencias requeridas:

   ```python
   pip install -r requirements.txt
   ```
3. Ejecutar el comando para levantar el servidor web:

   ```python
   streamlit run app.py
   ```


    4. Tras esto, se abrirá una pestaña del navegador en un puerto aleatorio disponible. Esperar a la carga del contenido y el aplicativo estará listo apra ser usado.

## Descripción por archivo/carpeta

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

### 10. Carpeta `ui/`

- **Rol:** Funciones reutilizables
- **Archivos:**

  - `plots.py` → Herramientas para visualización de resultados
  - `ui_evm.json` → Resultados de simulación.
  - `ui_montecarlo.json` → Despliegue de resultados de la simulación de Monte Carlo 
  - `visualizacion_pert` → Generador de grafos


## Tablero KanBan

[Jira](https://pio-galileo.atlassian.net/issues/?jql=project%20%3D%20SWDGP%20ORDER%20BY%20created%20DESC&referrer=agility)

## Contacto de los desarolladores

1. Jorge Anibal Velasquez Folgar - jorge_velasquez@galileo.edu
2. Rene Andres Tarot Palma - rene.tarot@galileo.edu
3. Andrés de Jesús Gonzalez Melgar - 20004118@galileo.edu
