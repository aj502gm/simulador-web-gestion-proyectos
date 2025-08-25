"""
Módulo: file_utils
Funciones para el manejo de archivos.
"""

import json
import os
import streamlit as st
import networkx as nx
import pandas as pd

# Columnas esperadas en el archivo CSV
EXPECTED_COLUMNS = [
    "id",
    "name",
    "optimistic_duration",
    "most_likely_duration",
    "pessimistic_duration",
    "optimistic_cost",
    "most_likely_cost",
    "pessimistic_cost",
    "dependencies",
]


# TODO: Validar dependencias (no dependencias, circulares, que el grafo tenga fin, tareas con duracion validas)


def validate_csv(df):
    """
    Valida un DataFrame según el formato esperado para el CSV del proyecto.

    Args:
        df (pd.DataFrame): DataFrame a validar.

    Returns:
        tuple: (bool, str) donde el booleano indica si es válido y el string es un mensaje.
    """
    errors = []

    # Verificar columnas faltantes o inesperadas
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    extra_cols = [col for col in df.columns if col not in EXPECTED_COLUMNS]

    if missing_cols:
        errors.append(f"Faltan columnas en el CSV: {', '.join(missing_cols)}")
    if extra_cols:
        errors.append(f"Columnas inesperadas en el CSV: {', '.join(extra_cols)}")

    # Columnas que deben ser numéricas
    num_cols = [
        "optimistic_duration",
        "most_likely_duration",
        "pessimistic_duration",
        "optimistic_cost",
        "most_likely_cost",
        "pessimistic_cost",
    ]

    for col in num_cols:
        try:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        except Exception:
            errors.append(f"No se pudo convertir la columna '{col}' a numérica.")
            continue
        if df[col].isna().any():
            errors.append(f"La columna '{col}' contiene valores no numéricos.")
        if (df[col] < 0).any():
            errors.append(f"La columna '{col}' no debe contener valores negativos.")

    # Verificar duplicados en 'id'
    if df["id"].duplicated().any():
        errors.append("La columna 'id' tiene valores duplicados.")

    # Validar que las dependencias existan en los IDs
    all_ids = set(df["id"].astype(str))
    invalid_deps = []
    for dep in df["dependencies"].dropna():
        deps = [d.strip() for d in dep.split(",") if d.strip()]
        invalid_deps.extend([d for d in deps if d not in all_ids])
    if invalid_deps:
        errors.append(f"Dependencias inválidas: {set(invalid_deps)}")

    # Validar dependencias circulares
    G = nx.DiGraph()
    for _, row in df.iterrows():
        activity_id = str(row["id"])
        G.add_node(activity_id)
        if pd.notna(row["dependencies"]) and row["dependencies"] != "":
            for dep in row["dependencies"].split(","):
                dep = dep.strip()
                G.add_edge(dep, activity_id)

    try:
        cycle = nx.find_cycle(G, orientation="original")
        errors.append(f"Ciclo detectado en dependencias: {cycle}")
    except nx.NetworkXNoCycle:
        pass

    # Validar si tiene tarea final
    final_task = [n for n in G.nodes if G.out_degree(n) == 0]
    if not final_task:
        errors.append(
            "No hay tareas finales en el proyecto (todas tienen dependientes)."
        )

    if errors:
        return False, " | ".join(errors)
    return True, "Archivo CSV válido."


def csv_json(data_frame, project_name, json_filename="project_input.json"):
    """
    Convierte un dataframe de actividades en un JSON con la estructura de proyecto.

    Args:
        data_frame (pd.Dataframe): Dataframe a convertir en JSON.
        project_name (str): Nombre del proyecto.
        json_filename (str): Nombre del archivo JSON de salida (por defecto 'project_input.json').

    Returns:
        dict: JSON del proyecto como diccionario de Python.
    """

    # Transformar cada fila en la estructura deseada
    activities = []
    for _, row in data_frame.iterrows():
        dependencies = []
        if pd.notna(row["dependencies"]) and row["dependencies"] != "":
            dependencies = [dep.strip() for dep in row["dependencies"].split(",")]

        activity = {
            "id": row["id"],
            "name": row["name"],
            "duration": {
                "optimistic": int(row["optimistic_duration"]),
                "most_likely": int(row["most_likely_duration"]),
                "pessimistic": int(row["pessimistic_duration"]),
            },
            "cost": {
                "optimistic": int(row["optimistic_cost"]),
                "most_likely": int(row["most_likely_cost"]),
                "pessimistic": int(row["pessimistic_cost"]),
            },
            "dependencies": dependencies,
        }
        activities.append(activity)

    # Crear el JSON final
    project_json = {"project_name": project_name, "activities": activities}

    # Crear carpeta 'data' si no existe
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)

    # Guardar JSON en la carpeta 'data'
    json_path = os.path.join(data_folder, json_filename)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(project_json, f, indent=4, ensure_ascii=False)

    return project_json


@st.cache_data
def get_data(path: str = "data/example_input.csv"):
    """
    Lee un archivo CSV y lo devuelve como un DataFrame de pandas.

    Parameters
    ----------
    path : str, optional
        Ruta al archivo CSV. Por defecto 'data/example_input.csv'.

    Returns
    -------
    pandas.DataFrame
        Datos cargados desde el archivo CSV.
    """
    df = pd.read_csv(path)
    return df


@st.cache_data
def convert_for_download(df: pd.DataFrame) -> bytes:
    """
    Convierte un DataFrame en una representación CSV codificada en UTF-8,
    lista para ser descargada en un botón de Streamlit.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame a convertir.

    Returns
    -------
    bytes
        Contenido en formato CSV codificado como UTF-8 con BOM.
    """
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
