import streamlit as st
from ui.plots import plot_histogram
import pandas as pd

def show_simulation_results(duraciones_result, costos_result):
    st.header("📊 Resultados de la Simulación Monte Carlo")

    # --- Duraciones ---
    st.subheader("Duraciones")
    st.write(f"Media: {duraciones_result['media']:.2f}")
    st.write(f"Mediana: {duraciones_result['mediana']:.2f}")
    st.write(f"Mínimo: {duraciones_result['minimo']:.2f}")
    st.write(f"Máximo: {duraciones_result['maximo']:.2f}")
    st.write(f"Desviación Estándar: {duraciones_result['desviacion_standar']:.2f}")

    plot_histogram(data=duraciones_result["duraciones"], title="Distribución PERT de Duraciones del proyecto", x_title="Duración Total del Proyecto", y_label="Frecuencia", bins=20)

    # --- Costos ---
    st.subheader("Costos")
    st.write(f"Media: ${costos_result['media']:.2f}")
    st.write(f"Mediana: ${costos_result['mediana']:.2f}")
    st.write(f"Mínimo: ${costos_result['minimo']:.2f}")
    st.write(f"Máximo: ${costos_result['maximo']:.2f}")
    st.write(f"Desviación Estándar: ${costos_result['desviacion_standar']:.2f}")

    plot_histogram(data=costos_result["costos"], title="Distribución PERT de Costos", x_title="Costos total del Proyecto", y_label="Frecuencia", bins=20, edgecolor='Green')

def show_projection_results(costos_result):
    st.header("📊 Resultados de la Simulación Monte Carlo para la proyección del proyecto")

    # --- Costos ---
    st.subheader("Costos proyectados")
    st.write(f"Media: ${costos_result['media']:.2f}")
    st.write(f"Mediana: ${costos_result['mediana']:.2f}")
    st.write(f"Mínimo: ${costos_result['minimo']:.2f}")
    st.write(f"Máximo: ${costos_result['maximo']:.2f}")
    st.write(f"Desviación Estándar: ${costos_result['desviacion_standar']:.2f}")

    plot_histogram(data=costos_result["costos"], title="Histograma de Simulación Montecarlo", x_title="Costo final estimado (EAC)", y_label="Frecuencia", bins=20, edgecolor='Green')