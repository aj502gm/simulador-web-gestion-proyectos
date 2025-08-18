import streamlit as st
import matplotlib.pyplot as plt

def show_simulation_results(duraciones_result, costos_result):
    st.header("📊 Resultados de la Simulación Monte Carlo")

    # --- Duraciones ---
    st.subheader("Duraciones")
    st.write(f"Media: {duraciones_result['media']:.2f}")
    st.write(f"Mediana: {duraciones_result['mediana']:.2f}")
    st.write(f"Mínimo: {duraciones_result['minimo']:.2f}")
    st.write(f"Máximo: {duraciones_result['maximo']:.2f}")
    st.write(f"Desviación Estándar: {duraciones_result['desviacion_standar']:.2f}")

    fig1, ax1 = plt.subplots(figsize=(4,2))  # ancho=6, alto=4 (en pulgadas)
    ax1.hist(duraciones_result["duraciones"], bins=20, edgecolor="black")
    ax1.set_title("Distribución de Duraciones")
    ax1.set_xlabel("Duración Total del Proyecto")
    ax1.set_ylabel("Frecuencia")
    st.pyplot(fig1, use_container_width=False)

    # --- Costos ---
    st.subheader("Costos")
    st.write(f"Media: ${costos_result['media']:.2f}")
    st.write(f"Mediana: ${costos_result['mediana']:.2f}")
    st.write(f"Mínimo: ${costos_result['minimo']:.2f}")
    st.write(f"Máximo: ${costos_result['maximo']:.2f}")
    st.write(f"Desviación Estándar: ${costos_result['desviacion_standar']:.2f}")

    fig2, ax2 = plt.subplots(figsize=(4,2))
    ax2.hist(costos_result["costos"], bins=20, edgecolor="black", color="green")
    ax2.set_title("Distribución de Costos")
    ax2.set_xlabel("Costo Total del Proyecto")
    ax2.set_ylabel("Frecuencia")
    st.pyplot(fig2, use_container_width=False)