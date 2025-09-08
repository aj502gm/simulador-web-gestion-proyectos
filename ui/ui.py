import pandas as pd
import streamlit as st
from ui.visualizacion_pert import render_pert_tasks
from file_utils import csv_json, validate_csv
import streamlit.components.v1 as components


def init_session_state(default_name):
    if "project_name" not in st.session_state:
        st.session_state.project_name = default_name
        st.session_state.project_json = None
        st.session_state.data_frame = None
        st.session_state.tasks = []
        st.session_state.critical_path = []
        st.session_state.html_graph = None


def handle_file_upload(uploaded_file, load_from_data_csv, name):
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        elif load_from_data_csv:
            df = pd.read_csv("data/project_input.csv")
        else:
            st.warning("No se ha seleccionado ningún archivo CSV.")
            return None

        valid, msg = validate_csv(df)
        if valid:
            st.success(msg)
            st.session_state.data_frame = df
            st.session_state.project_json = csv_json(df, name)
            return df
        else:
            st.error(msg)
            return None
    except Exception as e:
        st.error(f"Error al leer el CSV: {e}")
        return None


def show_project_graph_and_metrics():
    if st.session_state.project_json:
        html_graph, critical_path, tasks = render_pert_tasks(
            st.session_state.project_json
        )
        st.session_state.html_graph = html_graph
        st.session_state.critical_path = critical_path
        st.session_state.tasks = tasks

    if st.session_state.html_graph:
        st.markdown(f"**Ruta crítica:** {' → '.join(st.session_state.critical_path)}")
        components.html(
            st.session_state.html_graph, width=None, height=700, scrolling=True
        )


def show_data_table():
    if st.session_state.data_frame is not None:
        st.dataframe(st.session_state.data_frame)


def project_input_form(default_name="Proyecto", load_from_data_csv=False):
    st.subheader("Definición del Proyecto")
    init_session_state(default_name)

    with st.form(key="input_form"):
        name = st.text_input("Nombre del proyecto", value=st.session_state.project_name)
        uploaded_file = st.file_uploader("Subir archivo .csv", type=["csv"])
        submit = st.form_submit_button("Subir")

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

    st.session_state.project_name = name

    if submit:
        df = handle_file_upload(uploaded_file, load_from_data_csv, name)
        if df is not None:
            show_data_table()
            show_project_graph_and_metrics()
    else:
        show_data_table()
        show_project_graph_and_metrics()

    return (
        st.session_state.project_name,
        st.session_state.project_json,
        st.session_state.critical_path,
    )
