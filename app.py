# Archivo principal del proyecto. Controla el flujo y la lógica de los elementos.
import streamlit as st
import montecarlo
import evm
import ui.ui as ui
from ui.visualizacion_pert import render_pert_tasks, MOCK_TASKS
import streamlit.components.v1 as components

# Configuraciones de pagina
st.set_page_config(page_title="Gestion de Proyectos",
                   page_icon=":bar_chart:",
                   layout="wide")
st.markdown(
    """
    <style>
    .css-1d391kg {  /* Reemplaza esta clase si es diferente en tu Streamlit */
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    .main {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    .st-emotion-cache-1kztmhs {
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Ejemplo de uso
st.title("Simulador de Proyectos con Riesgo y EVM")

# Formulario de entrada
name, activities_json = ui.project_input_form()

if st.button("Ejecutar Simulación"):
    mc_results = montecarlo.run_simulation(activities_json)
    ui.montecarlo_results_chart(mc_results)

# ------------------ PERT VISUALIZATION EXAMPLE ------------------ 
st.title("Visualización de PERT")
html_graph, critical_path = render_pert_tasks(MOCK_TASKS)
st.markdown(f"**Ruta crítica:** {' → '.join(critical_path)}")
duracion_total = sum(MOCK_TASKS[t]['duracion'] for t in critical_path)
st.markdown(f"**Duración total:** {duracion_total} días")
components.html(html_graph, width=None, height=700, scrolling=True)
# ------------------------------------------------------------------------

if st.button("Calcular EVM"):
    evm_results = evm.calculate_metrics(activities_json)
    ui.evm_metrics_display(evm_results)
    pass
