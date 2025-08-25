import pandas as pd
import streamlit as st
from ui.visualizacion_pert import render_pert_tasks
from file_utils import csv_json, validate_csv
import streamlit.components.v1 as components

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

    # Creación del formulario de entrada
    with st.form(key="input_form"):
        name = st.text_input(label="Nombre del proyecto", value=default_name)
        uploaded_file = st.file_uploader(label="Subir archivo .csv", type=["csv"])
        send = st.form_submit_button(label="Subir")

    df = None
    project_json, critical_path = None, []

    # Procesamiento del archivo después de enviar el formulario
    if send:

        try:
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
            elif load_from_data_csv:
                df = pd.read_csv("data/project_input.csv")
            else:
                st.warning("No se ha seleccionado ningún archivo CSV.")
                return name, None, []

            if df is not None:
                valid, msg = validate_csv(df)
                if valid:
                    st.success(msg)
                    st.dataframe(df.head())
                    project_json = csv_json(data_frame=df, project_name=name)

                    st.title("Visualización de PERT")
                    html_graph, critical_path = render_pert_tasks(project_json)
                    st.markdown(f"**Ruta crítica:** {' → '.join(critical_path)}")
                    components.html(html_graph, width=None, height=700, scrolling=True)
                else:
                    st.error(msg)
        except Exception as e:
            st.error(f"Error al leer el CSV: {e}")

    return name, project_json, critical_path
