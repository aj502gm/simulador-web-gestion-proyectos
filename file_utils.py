import json
import os
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

# TODO: Validar error al subir un archivo (error desconocido)
# TODO: Validar formato correcto (columnas, tipo de dato, etc)
# TODO: Validar dependencias (no dependencias, circulares, que el grafo tenga fin, tareas con duracion validas)
# TODO: Mostrar los errores de forma descriptiva en alguna parte de la web (si es un error desconocido, mostrar mensaje generico, caso contrario, un mensaje especifico)


def validate_csv(df):
    """
    Valida un DataFrame según el formato esperado para el CSV del proyecto.

    Args:
        df (pd.DataFrame): DataFrame a validar.

    Returns:
        tuple: (bool, str) donde el booleano indica si es válido y el string es un mensaje.
    """

    # Verificar columnas faltantes o inesperadas
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    extra_cols = [col for col in df.columns if col not in EXPECTED_COLUMNS]

    if missing_cols:
        return False, f"Faltan columnas en el CSV: {missing_cols}"
    if extra_cols:
        return False, f"Columnas inesperadas en el CSV: {extra_cols}"

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
        if not pd.api.types.is_numeric_dtype(df[col]):
            return False, f"La columna '{col}' debe contener valores numéricos."
        if (df[col] < 0).any():
            return False, f"La columna '{col}' no debe contener valores negativos."

    # Verificar duplicados en 'id'
    if df["id"].duplicated().any():
        return False, "La columna 'id' tiene valores duplicados."

    # Validar que las dependencias existan en los IDs
    all_ids = set(df["id"])
    for dep in df["dependencies"].dropna():
        deps = [d.strip() for d in dep.split(",") if d.strip()]

        for d in deps:
            if d not in all_ids:
                return (
                    False,
                    f"Dependencia '{d}' no corresponde a ningún 'id'.",
                )

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

    print(f"JSON guardado en: {json_path}")
    return project_json
