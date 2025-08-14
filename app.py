# Archivo principal del proyecto. Controla el flujo y la lógica de los elementos.
import streamlit as st
import montecarlo
import evm
import ui.ui as ui

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
# ------------------------------------------------------------------------

if st.button("Calcular EVM"):
    evm_results = evm.calculate_metrics(activities_json)
    ui.evm_metrics_display(evm_results)
    pass
