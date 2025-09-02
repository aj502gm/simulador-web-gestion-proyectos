import streamlit as st
import pandas as pd
import numpy as np

def evm_table(tasks: dict):

    # IF PAGE RELOAD, USED SAVED DATA
    if "evm_form_data" not in st.session_state:
        st.session_state.evm_form_data = {
            key: {"BCWP": 0.0, "ACWP": 0.0} for key in tasks.keys()
        }

    st.markdown("### Ingrese los valores para cada tarea:")

    # SHOW NUMERICAL VALUES FOR EDITING
    for key in tasks.keys():
        with st.expander(key, expanded=True):
            bcwp = st.number_input(
                "BCWP", 
                min_value=0.0, 
                value=st.session_state.evm_form_data[key]["BCWP"], 
                step=100.0, 
                key=f"BCWP_{key}"
            )
            acwp = st.number_input(
                "ACWP", 
                min_value=0.0, 
                value=st.session_state.evm_form_data[key]["ACWP"], 
                step=100.0, 
                key=f"ACWP_{key}"
            )
            # ON NUMERICAL INPUT CHANGE, SAVE CURRENT STATE
            st.session_state.evm_form_data[key] = {"BCWP": bcwp, "ACWP": acwp}


    if st.button("Calcular métricas"):
        df = pd.DataFrame([
            {"TAREA": tasks[key]["task"], "BAC": tasks[key]['BAC'], **st.session_state.evm_form_data[key]}
            for key in tasks.keys()
        ])

        # CALCULATE EVM METRICS
        df["CPI"] = np.where(df["ACWP"] > 0, df["BCWP"] / df["ACWP"], 0)
        df["EAC Optimista"] = np.where(df["CPI"] > 0, df["BAC"] / np.maximum(df["CPI"], 1), df["BAC"])
        df["EAC Realista"] = np.where(df["CPI"] > 0, df["BAC"] / df["CPI"], df["BAC"])
        df["EAC Pesimista"] = np.where(df["CPI"] > 0, df["BAC"] * (1 / (df["CPI"] ** 2)), df["BAC"])

        st.subheader("Tabla de métricas")
        st.dataframe(df, use_container_width=True)

        totals = {
            "BAC": df["BAC"].sum(),
            "BCWP": df["BCWP"].sum(),
            "ACWP": df["ACWP"].sum(),
            "CPI": df["BCWP"].sum() / df["ACWP"].sum() if df["ACWP"].sum() > 0 else 0,
            "EAC Optimista": df["EAC Optimista"].sum(),
            "EAC Realista": df["EAC Realista"].sum(),
            "EAC Pesimista": df["EAC Pesimista"].sum(),
        }

        st.subheader("Totales del Proyecto")
        st.write(totals)

        # SAVE CURRENT STATE
        st.session_state.evm_results = df
        st.session_state.evm_totals = totals
