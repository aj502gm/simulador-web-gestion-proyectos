import streamlit as st
import pandas as pd
import numpy as np
from ui.plots import plot_s_curve_with_labels

def evm_table(tasks: dict):

    # IF PAGE RELOAD, USED SAVED DATA
    if "evm_form_data" not in st.session_state:
        st.session_state.evm_form_data = {
            key: {"BCWP": 0.0, "ACWP": 0.0} for key in tasks.keys()
        }

    st.header("Earned Value Management (EVM)")
    st.markdown("#### Ingresa los valores de Valor Ganado (BCWP/EV) y Costo Real (ACWP/AC) para cada tarea:")

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

        df["CPI"] = np.where(df["ACWP"] != 0, df["BCWP"] / df["ACWP"], 0)

        df["EAC Optimista"] = 0

        # Realista
        df["EAC Realista"] = np.where(df["CPI"] != 0, df["BAC"] / df["CPI"], df["BAC"])

        # Optimista
        df["EAC Optimista"] = df["ACWP"] + (df["BAC"] - df["BCWP"])
        df["EAC Optimista"] = np.minimum(df["EAC Optimista"], df["EAC Realista"])

        # Pesimista (con SPI estimado)
        SPI_pesimista = 0.9  # ajusta según riesgo
        df["EAC Pesimista"] = np.where(df["CPI"] != 0, df["ACWP"] + (df["BAC"] - df["BCWP"]) / (df["CPI"] * SPI_pesimista), df["EAC Realista"])
        df["EAC Pesimista"] = np.maximum(df["EAC Pesimista"], df["EAC Realista"])

        # FORMAT NUMERIC COLUMNS TO 2 DECIMALS
        numeric_columns = df.select_dtypes(include=["number"]).columns
        df[numeric_columns] = df[numeric_columns].map(lambda x: f"{x:.2f}")

        st.subheader("Tabla de métricas")
        st.dataframe(df, use_container_width=True)

        totals = {
            "BAC": df["BAC"].astype(float).sum(),
            "BCWP": df["BCWP"].astype(float).sum(),
            "ACWP": df["ACWP"].astype(float).sum(),
            "CPI": df["BCWP"].astype(float).sum() / df["ACWP"].astype(float).sum() if df["ACWP"].astype(float).sum() > 0 else 0,
            "EAC Optimista": df["EAC Optimista"].astype(float).sum(),
            "EAC Realista": df["EAC Realista"].astype(float).sum(),
            "EAC Pesimista": df["EAC Pesimista"].astype(float).sum(),
        }

        st.subheader("Totales del Proyecto")
        st.write({key: f"{value:.2f}" for key, value in totals.items()})

        # SAVE CURRENT STATE
        st.session_state.evm_results = df
        st.session_state.evm_totals = totals

        # Prepare data for S-curve plot
        s_curve_data = pd.DataFrame({
            "TAREA": [tasks[key]["task"] for key in tasks.keys()],
            "Costo Planeado (BAC)": np.cumsum([tasks[key]["BAC"] for key in tasks.keys()]),
            "Costo Real (ACWP)": np.cumsum([st.session_state.evm_form_data[key]["ACWP"] for key in tasks.keys()])
        })

        # Plot S-curve
        st.subheader("Curva S")
        plot_s_curve_with_labels(s_curve_data, x_column="TAREA", y_label="Costo", title="Curva S de Costos")