# Archivo principal del proyecto. Controla el flujo y la lógica de los elementos.
import evm
import montecarlo
import os
import pandas as pd
import streamlit as st
from ui.metrics_table import evm_table
import ui.ui as ui
import ui.ui_evm as ui_evm
import ui.ui_montecarlo as ui_montecarlo
from file_utils import get_data, convert_for_download


# Configuraciones de pagina
st.set_page_config(
    page_title="Gestion de Proyectos", page_icon=":bar_chart:", layout="wide"
)
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
    unsafe_allow_html=True,
)

# Ejemplo de uso
st.title("Simulador de Proyectos con Riesgo y EVM")

# Formulario de entrada
name, activities_json, critical_path = ui.project_input_form(load_from_data_csv=True)


@st.fragment
def download_file():
    """
    Fragmento de Streamlit que renderiza un botón de descarga
    para un DataFrame cargado desde el módulo file_utils.
    """
    df = get_data()
    csv = convert_for_download(df)
    st.download_button(
        label="Descargar CSV ejemplo",
        data=csv,
        file_name="project_input.csv",
        mime="text/csv",
        icon=":material/download:",
    )


download_file()

# Simulación Montecarlo
if "montecarlo_done" not in st.session_state:
    st.session_state.montecarlo_done = False
    st.session_state.duraciones_result = None
    st.session_state.costos_result = None

if critical_path and not st.session_state.montecarlo_done:
    # Ejecutar la simulación una sola vez
    duraciones_result, costos_result = montecarlo.run_simulation(
        activities_json, critical_path
    )
    st.session_state.duraciones_result = duraciones_result
    st.session_state.costos_result = costos_result
    st.session_state.montecarlo_done = True

# Mostrar resultados solo si existen
if st.session_state.montecarlo_done:
    ui_montecarlo.show_simulation_results(
        st.session_state.duraciones_result, st.session_state.costos_result
    )


if st.session_state.tasks:
    evm_table(st.session_state.tasks)

if "evm_totals" in st.session_state:
    projection_results = montecarlo.run_projection_simulation(
        st.session_state.evm_totals
    )
    ui_montecarlo.show_projection_results(projection_results)

# EVM
# if critical_path:
#    evm_results = evm.calculate_metrics(activities_json)
#    ui_evm.evm_metrics_display(evm_results)
#    pass
