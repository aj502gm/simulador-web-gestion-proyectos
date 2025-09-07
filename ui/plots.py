import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import numpy as np
from scipy.optimize import curve_fit

def plot_table(df: pd.DataFrame):
    """
    This function creates a table visualization
    
    Uso:
    >>>    plot_table(pd.DataFrame({
    >>>        "SEMANA": [1, 2, 3, 4, 5, 6],
    >>>        "EVM": [100, 200, 300, 400, 500, 600],
    >>>        "AC": [200, 300, 400, 500, 600, 700]
    >>>    }))
    """
    fig, ax = plt.subplots()
    
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    fig.tight_layout()
    st.pyplot(fig)  



def plot_lines(lines_to_plot: dict, title: str, x_title: str, x_labels: list = None):
    """
    Create a line plot with multiple lines
    
    Usage:
    >>>    plot_lines({
    >>>       'Test': [10,10,20,40,30],
    >>>       'Test2': [50,15,25,30,70]
    >>>    }, title='Testing', x_title='Testing')
    """
    fig, ax = plt.subplots()

    if x_labels is None:
        x_labels = list(range(1, len(next(iter(lines_to_plot.values()))) + 1))

    for label, y_values in lines_to_plot.items():
        ax.plot(x_labels, y_values, marker='o', label=label) 

    ax.set_title(title)
    ax.set_xlabel(x_title)
    ax.set_xticks(x_labels)  
    ax.legend()
    ax.grid(True)  
    st.pyplot(fig, use_container_width=True)

def plot_histogram(data:list, title: str, x_title: str, y_label: str, bins: int,edgecolor: str = 'black'):
    """
    Create a histogram
    
    Usage:
    >>>    plot_lines({
    >>>       'Test': [10,10,20,40,30],
    >>>       'Test2': [50,15,25,30,70]
    >>>    }, title='Testing', x_title='Testing')
    """
    fig, ax = plt.subplots()

    ax.hist(data, bins=bins, edgecolor=edgecolor)       
    ax.set_title(title)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_label)
    ax.legend()
    st.pyplot(fig, use_container_width=True)

def sigmoid(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

def plot_s_curve(df: pd.DataFrame, x_column: str, y_label: str, title: str):
    """
        Plot S curve.
        Usage:
        >>>    data = {
        >>>       "SEMANA": [1, 2, 3, 4, 5, 6],
        >>>       "EV": [100, 150, 220, 300, 400, 480],
        >>>       "AC": [90, 160, 210, 310, 390, 470],
        >>>       "PV": [120, 180, 240, 320, 420, 500]
        >>>    }
        >>>    df = pd.DataFrame(data)
        >>>    plot_s_curve(df, x_column="SEMANA", y_label="Test", title="Test")
    """
    fig, ax = plt.subplots()
    x_data = df[x_column].values

    for col in df.columns:
        if col == x_column:
            continue
        y_data = df[col].values
        
        try:
            popt, _ = curve_fit(sigmoid, x_data, y_data, p0=[max(y_data), 1, np.median(x_data)])
            x_fit = np.linspace(min(x_data), max(x_data), 100)
            y_fit = sigmoid(x_fit, *popt)
            ax.plot(x_fit, y_fit, label=f"{col} - Curva S")
            ax.scatter(x_data, y_data, marker='o', label=f"{col} - Datos")
        except Exception as e:
            st.warning(f"No se pudo ajustar la curva para {col}: {e}")

    ax.set_xlabel(x_column)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

    st.pyplot(fig, use_container_width=True)

def plot_s_curve_with_labels(df: pd.DataFrame, x_column: str, y_label: str, title: str):
    fig, ax = plt.subplots()

    x_labels = df[x_column].values

    for col in df.columns:
        if col == x_column:
            continue
        y_data = pd.to_numeric(df[col], errors='coerce').dropna().values  

        # Recortar valores constantes al final pero mantener el índice original
        trimmed_data = trim_constant_tail(y_data)
        x_data = np.arange(len(trimmed_data))  

        if len(trimmed_data) < 3 or len(np.unique(trimmed_data)) < 3:
            # Demasiado pocos datos para ajustar sigmoide → solo graficamos los puntos
            ax.plot(x_data, trimmed_data, marker='o', linestyle='-', label=f"{col} - Datos (sin curva)")
            continue

        try:
            popt, _ = curve_fit(sigmoid, x_data, trimmed_data, p0=[max(trimmed_data), 1, np.median(x_data)])
            x_fit = np.linspace(min(x_data), max(x_data), 100)
            y_fit = sigmoid(x_fit, *popt)
            ax.plot(x_fit, y_fit, label=f"{col} - Curva S")
            ax.scatter(x_data, trimmed_data, marker='o', label=f"{col} - Datos")
        except Exception as e:
            st.warning(f"No se pudo ajustar la curva para {col}: {e}")

    # Mostrar todas las etiquetas del eje X
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha="right")

    ax.set_xlabel(x_column)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

    st.pyplot(fig, use_container_width=True)



def trim_constant_tail(values: np.ndarray) -> np.ndarray:
    """
    Recorta los valores al eliminar la parte final constante (cola plana).
    """
    if len(values) == 0:
        return values
    last_change_idx = len(values) - 1
    for i in range(len(values) - 2, -1, -1):
        if values[i] != values[i + 1]:
            last_change_idx = i + 1
            break
    return values[: last_change_idx + 1]