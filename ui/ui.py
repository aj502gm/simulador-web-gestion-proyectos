import streamlit as st

#Componentes generales de Streamlit que se utilizarán en el proyecto.

#Ejemplo de uso

def project_input_form():
    st.subheader("Definición del Proyecto")
    
    with st.form("input_form"):
        name = st.text_input("Nombre del proyecto")
        file = st.file_uploader("Subir archivo .csv", type=["csv"])
        st.markdown("""
                    **Formato esperado del archivo CSV:**

                    ```csv
                    id,name,optimistic_duration,most_likely_duration,pessimistic_duration,optimistic_cost,most_likely_cost,pessimistic_cost,dependencies
                    A1,Diseño,2,4,6,500,800,1000,
                    A2,Construcción,10,14,20,2000,2500,3000,A1
                    ```
                    """)

        send = st.form_submit_button("Subir")

    return name, file

def montecarlo_results_chart(df):
    st.subheader("Resultados de Simulación Monte Carlo")
    st.bar_chart(df)

def evm_metrics_display(metrics):
    st.subheader("Métricas EVM")
    st.json(metrics)