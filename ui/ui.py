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

    Returns:
        tuple: Contiene el nombre del proyecto y el archivo JSON.
    """

    st.subheader("Definición del Proyecto")

    # Creación del formulario de entrada
    with st.form(key="input_form"):
        name = st.text_input(label="Nombre del proyecto", value=default_name)
        file = st.file_uploader(label="Subir archivo .csv", type=["csv"])
        critical_path = []
        df = None

        send = st.form_submit_button(label="Subir")

    # Procesamiento del archivo después de enviar el formulario
    if send:
        if file is not None or load_from_data_csv:
            try:
                if file is not None:
                    df = pd.read_csv(file)
                elif load_from_data_csv:
                    df = pd.read_csv("data/project_input.csv")

                valid, msg = validate_csv(df)
                if valid:
                    st.success(msg)
                    st.dataframe(df.head())
                else:
                    st.error(msg)
            except Exception as e:
                st.error(f"Error al leer el CSV: {e}")

        else:
            st.warning("No se ha seleccionado ningún archivo CSV.")

        file = csv_json(data_frame=df, project_name=name)

        st.title("Visualización de PERT")
        html_graph, critical_path = render_pert_tasks(file)
        st.markdown(f"**Ruta crítica:** {' → '.join(critical_path)}")
        components.html(html_graph, width=None, height=700, scrolling=True)

    return name, file, critical_path
