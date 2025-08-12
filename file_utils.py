import pandas as pd

EXPECTED_COLUMNS = [
    "id",
    "name",
    "optimistic_duration",
    "most_likely_duration",
    "pessimistic_duration",
    "optimistic_cost",
    "most_likely_cost",
    "pessimistic_cost",
    "dependencies"
]

def validate_csv(df):
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    extra_cols = [col for col in df.columns if col not in EXPECTED_COLUMNS]

    if missing_cols:
        return False, f"Faltan columnas en el CSV: {missing_cols}"
    if extra_cols:
        return False, f"Columnas inesperadas en el CSV: {extra_cols}"
    
    num_cols = [
        "optimistic_duration",
        "most_likely_duration",
        "pessimistic_duration",
        "optimistic_cost",
        "most_likely_cost",
        "pessimistic_cost"
    ]

    for col in num_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            return False, f"La columna '{col}' debe contener valores numéricos."
        if (df[col] < 0 ).any():
            return False, f"La columna '{col}' no debe contener valores negativos."

    if df["id"].duplicated().any():
        return False, "La columna 'id' tiene valores duplicados."
    
    all_ids = set(df["id"])
    for dep in df["dependencies"].dropna():
        deps = [d.strip() for d in dep.split(",") if d.strip()]
        
        for d in deps:
            if d not in all_ids:
                return(
                    False,
                    f"Dependencia '{d}' no corresponde a ningún 'id'.",
                )
            
    return True, "Archivo CSV válido."