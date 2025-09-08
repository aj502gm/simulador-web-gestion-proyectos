import streamlit as st
import pandas as pd
import numpy as np
from ui.plots import plot_s_curve_with_labels


def evm_table(tasks: dict):
    # IF PAGE RELOAD, USED SAVED DATA
    if "evm_form_data" not in st.session_state:
        st.session_state.evm_form_data = {
            key: {"BCWP": 0.0, "ACWP": 0.0, "tiempo_trabajado": 0}
            for key in tasks.keys()
        }

    st.header("Earned Value Management (EVM)")
    st.markdown(
        "#### Complete la siguiente tabla con los valores actuales del proyecto:"
    )

    with st.form("evm_form"):
        # Create the table headers
        cols = st.columns([2, 1, 1, 1, 1, 1])
        headers = [
            "Tarea",
            "Presupuesto estimado (BAC)",
            "Tiempo planeados",
            "Valor Ganado (BCWP/EV)",
            "Costo Real (ACWP/AC)",
            "Tiempo trabajado",
        ]

        for col, header in zip(cols, headers):
            col.markdown(f"**{header}**")

        # Create rows for each task
        for key in tasks.keys():
            cols = st.columns([2, 1, 1, 1, 1, 1])

            # Display task name (read-only)
            cols[0].text(tasks[key]["task"])

            # Display BAC (read-only)
            cols[1].text(f"{tasks[key]['BAC']:.2f}")

            # Display planned duration (read-only)
            cols[2].text(str(tasks[key]["duration"]))

            # Input fields
            bcwp = cols[3].number_input(
                "BCWP",
                min_value=0.0,
                value=st.session_state.evm_form_data[key]["BCWP"],
                step=100.0,
                key=f"BCWP_{key}",
                label_visibility="collapsed",
            )

            acwp = cols[4].number_input(
                "ACWP",
                min_value=0.0,
                value=st.session_state.evm_form_data[key]["ACWP"],
                step=100.0,
                key=f"ACWP_{key}",
                label_visibility="collapsed",
            )

            tiempo = cols[5].number_input(
                "Tiempo trabajado",
                min_value=0,
                value=st.session_state.evm_form_data[key].get("tiempo_trabajado", 0),
                step=1,
                key=f"tiempo_{key}",
                label_visibility="collapsed",
            )

            # Update session state
            st.session_state.evm_form_data[key] = {
                "BCWP": bcwp,
                "ACWP": acwp,
                "tiempo_trabajado": tiempo,
            }

        submitted = st.form_submit_button("Calcular proyección")

    if submitted:
        df = pd.DataFrame(
            [
                {
                    "TAREA": tasks[key]["task"],
                    "BAC": tasks[key]["BAC"],
                    "duration": tasks[key]["duration"],
                    **st.session_state.evm_form_data[key],
                }
                for key in tasks.keys()
            ]
        )

        # CALCULATE EVM METRICS
        df["CPI"] = np.where(df["ACWP"] != 0, df["BCWP"] / df["ACWP"], 0)

        # Fixed SPI calculation using proper pandas operations
        df["PV"] = df["BAC"] * (df["tiempo_trabajado"] / df["duration"])
        df["SPI"] = np.where(df["PV"] != 0, df["BCWP"] / df["PV"], 0)

        df["EAC Optimista"] = 0.0
        df["EAC Realista"] = np.where(df["CPI"] != 0, df["BAC"] / df["CPI"], df["BAC"])
        df["EAC Optimista"] = df["ACWP"] + (df["BAC"] - df["BCWP"])
        df["EAC Optimista"] = np.minimum(df["EAC Optimista"], df["EAC Realista"])

        # Fixed EAC Pesimista calculation
        condition = (df["CPI"] != 0) & (df["SPI"] != 0)
        df["EAC Pesimista"] = np.where(
            condition,
            df["ACWP"] + (df["BAC"] - df["BCWP"]) / (df["CPI"] * df["SPI"]),
            df["EAC Realista"],
        )
        df["EAC Pesimista"] = np.maximum(df["EAC Pesimista"], df["EAC Realista"])

        # Calculate totals
        totals = {
            "TAREA": "TOTALES",
            "BAC": df["BAC"].astype(float).sum(),
            "duration": df["duration"].astype(float).sum(),
            "BCWP": df["BCWP"].astype(float).sum(),
            "ACWP": df["ACWP"].astype(float).sum(),
            "tiempo_trabajado": df["tiempo_trabajado"].astype(float).sum(),
            "CPI": (
                df["BCWP"].astype(float).sum() / df["ACWP"].astype(float).sum()
                if df["ACWP"].astype(float).sum() > 0
                else 0
            ),
            "SPI": (
                df["BCWP"].astype(float).sum() / df["PV"].astype(float).sum()
                if df["PV"].astype(float).sum() > 0
                else 0
            ),
            "EAC Optimista": df["EAC Optimista"].astype(float).sum(),
            "EAC Realista": df["EAC Realista"].astype(float).sum(),
            "EAC Pesimista": df["EAC Pesimista"].astype(float).sum(),
        }

        df = df.drop(columns=["PV"])

        # SAVE CURRENT STATE with numeric values
        st.session_state.evm_results = df.copy()
        st.session_state.evm_totals = totals.copy()

        # Now format numbers for display
        numeric_columns = df.select_dtypes(include=["number"]).columns
        df[numeric_columns] = df[numeric_columns].map(lambda x: f"{x:.2f}")

        # Format totals for display
        display_totals = totals.copy()
        for key in display_totals:
            if key != "TAREA":
                display_totals[key] = f"{float(display_totals[key]):.2f}"

        # Add totals row to DataFrame for display
        df_with_totals = pd.concat(
            [df, pd.DataFrame([display_totals])], ignore_index=True
        )

        # Display metrics table with totals
        st.subheader("Tabla de métricas")
        st.dataframe(df_with_totals, use_container_width=True)

        # SAVE CURRENT STATE
        st.session_state.evm_results = df
        st.session_state.evm_totals = totals

        # Prepare data for S-curve plot
        s_curve_data = pd.DataFrame(
            {
                "TAREA": [tasks[key]["task"] for key in tasks.keys()],
                "Costo Planeado (BAC)": np.cumsum(
                    [tasks[key]["BAC"] for key in tasks.keys()]
                ),
                "Costo Real (ACWP)": np.cumsum(
                    [
                        st.session_state.evm_form_data[key]["ACWP"]
                        for key in tasks.keys()
                    ]
                ),
            }
        )

        # Plot S-curve
        st.subheader("Curva S")
        plot_s_curve_with_labels(
            s_curve_data, x_column="TAREA", y_label="Costo", title="Curva S de Costos"
        )
