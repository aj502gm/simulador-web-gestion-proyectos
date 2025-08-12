import pandas as pd
import streamlit as st

from file_utils import validate_csv

#Componentes generales de Streamlit que se utilizarán en el proyecto.

#Ejemplo de uso

def project_input_form(default_name="Proyecto"):
    st.subheader("Definición del Proyecto")
    
    with st.form(key="input_form"):
        name = st.text_input(label="Nombre del proyecto", value=default_name)
        file = st.file_uploader(label="Subir archivo .csv", type=["csv"])
        st.markdown("""
                    **Formato esperado del archivo CSV:**

                    ```csv
                    id,name,optimistic_duration,most_likely_duration,pessimistic_duration,optimistic_cost,most_likely_cost,pessimistic_cost,dependencies
                    A1,Diseño,2,4,6,500,800,1000,
                    A2,Construcción,10,14,20,2000,2500,3000,A1
                    A3,Limpieza,5,6,10,100,150,200,"A1,A2"
                    ```
                    """)

        send = st.form_submit_button(label="Subir")

    if send:
        ...
    
    return name, file

def montecarlo_results_chart(df):
    st.subheader("Resultados de Simulación Monte Carlo")
    st.bar_chart(df)

def evm_metrics_display(metrics):
    st.subheader("Métricas EVM")
    st.json(metrics)