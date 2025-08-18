# Archivo principal del proyecto. Controla el flujo y la lógica de los elementos.
import streamlit as st
import montecarlo
import evm
import ui.ui as ui
import ui.ui_montecarlo as ui_montecarlo
import ui.ui_evm as ui_evm

# Configuraciones de pagina
st.set_page_config(page_title="Gestion de Proyectos",
                   page_icon=":bar_chart:",
                   layout="wide")
st.markdown(
    """
    <style>
    .css-1d391kg {
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
name, activities_json, critical_path = ui.project_input_form(load_from_data_csv = True)

# Simulación Montecarlo
if critical_path:
    duraciones_result, costos_result = montecarlo.run_simulation(activities_json, critical_path)
    ui_montecarlo.show_simulation_results(duraciones_result, costos_result)
# ------------------------------------------------------------------------


# EVM
#if critical_path:
#    evm_results = evm.calculate_metrics(activities_json)
#    ui_evm.evm_metrics_display(evm_results)
#    pass