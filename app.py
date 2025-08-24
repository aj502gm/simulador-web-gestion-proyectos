# Archivo principal del proyecto. Controla el flujo y la lógica de los elementos.
import evm
import montecarlo
import os
import pandas as pd
import streamlit as st
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

# Información sobre el formato esperado del CSV
st.markdown(
    """
            **Formato esperado del archivo CSV:**

            ```csv
            id,name,optimistic_duration,most_likely_duration,pessimistic_duration,optimistic_cost,most_likely_cost,pessimistic_cost,dependencies
            A1,Diseño,2,4,6,500,800,1000,
            A2,Construcción,10,14,20,2000,2500,3000,A1
            A3,Limpieza,5,6,10,100,150,200,"A1,A2"
            ```
            """
)


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
if critical_path:
    duraciones_result, costos_result = montecarlo.run_simulation(
        activities_json, critical_path
    )
    ui_montecarlo.show_simulation_results(duraciones_result, costos_result)
# ------------------------------------------------------------------------


# EVM
# if critical_path:
#    evm_results = evm.calculate_metrics(activities_json)
#    ui_evm.evm_metrics_display(evm_results)
#    pass
