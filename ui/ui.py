import pandas as pd
import streamlit as st
from ui.visualizacion_pert import render_pert_tasks
from file_utils import csv_json, validate_csv
import streamlit.components.v1 as components
from ui.metrics_table import evm_table
# Componentes generales de Streamlit que se utilizarán en el proyecto.

# Ejemplo de uso

def project_input_form(default_name="Proyecto", load_from_data_csv=False):
    """
    Muestra un formulario de entrada para definir un proyecto y subir un archivo CSV con las tareas.

    Args:
        default_name (str): Nombre por defecto del proyecto.
        load_from_data_csv (bool): Si es True, carga el archivo data/project_input.csv por defecto.

    Returns:
        tuple: (nombre del proyecto, datos del proyecto en JSON, ruta crítica)
    """
    st.subheader("Definición del Proyecto")

    # PREVENT STATE RELOAD FROM DELETING DATA
    if "project_name" not in st.session_state:
        st.session_state.project_name = default_name
        st.session_state.project_json = None
        st.session_state.tasks = []
        st.session_state.critical_path = []
        st.session_state.html_graph = None

    with st.form(key="input_form"):
        name = st.text_input("Nombre del proyecto", value=st.session_state.project_name)
        uploaded_file = st.file_uploader("Subir archivo .csv", type=["csv"])
        submit = st.form_submit_button("Subir")

    st.session_state.project_name = name

    if submit:
        try:
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
            elif load_from_data_csv:
                df = pd.read_csv("data/project_input.csv")
            else:
                st.warning("No se ha seleccionado ningún archivo CSV.")
                return st.session_state.project_name, None, []

            valid, msg = validate_csv(df)
            if valid:
                st.success(msg)
                st.dataframe(df.head())
                st.session_state.project_json = csv_json(df, name)

                # IF RELOADED AND STATE SAVED, SHOW GRAPH
                html_graph, critical_path, tasks = render_pert_tasks(st.session_state.project_json)
                st.session_state.html_graph = html_graph
                st.session_state.critical_path = critical_path
                st.session_state.tasks = tasks
            else:
                st.error(msg)
        except Exception as e:
            st.error(f"Error al leer el CSV: {e}")

    # IF RELOADED AND STATE SAVED, SHOW GRAPH
    if st.session_state.html_graph:
        st.markdown(f"**Ruta crítica:** {' → '.join(st.session_state.critical_path)}")
        components.html(st.session_state.html_graph, width=None, height=700, scrolling=True)

    # IF RELOADED AN STATE SAVED, SHOW EVM
    if st.session_state.tasks:
        evm_table(st.session_state.tasks)

    return st.session_state.project_name, st.session_state.project_json, st.session_state.critical_path
