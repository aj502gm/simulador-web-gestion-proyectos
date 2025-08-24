# Archivo principal del proyecto. Controla el flujo y la lógica de los elementos.
import streamlit as st
import montecarlo
import evm
import ui.ui as ui
import ui.ui_montecarlo as ui_montecarlo
import ui.ui_evm as ui_evm

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

# TODO: Implement csv download template
# Boton para descargar CSV template
csv_template = st.button(label="Descargar .csv ejemplo")


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
