import streamlit as st

#Componentes generales de Streamlit que se utilizarán en el proyecto.

#Ejemplo de uso

def project_input_form():
    st.subheader("Definición del Proyecto")
    name = st.text_input("Nombre del proyecto")
    activities = st.text_area("Actividades (JSON)")
    return name, activities

def montecarlo_results_chart(df):
    st.subheader("Resultados de Simulación Monte Carlo")
    st.bar_chart(df)

def evm_metrics_display(metrics):
    st.subheader("Métricas EVM")
    st.json(metrics)