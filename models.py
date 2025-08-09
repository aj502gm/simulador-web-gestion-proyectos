# Formatos estandar de los json que se utilizarán durante el proyecto

# Formato para entrada del proyecto
project_input_schema = {
    "project_name": "string",
    "activities": [
        {
            "id": "string",
            "name": "string",
            "duration": {
                "optimistic": "number",
                "most_likely": "number",
                "pessimistic": "number"
            },
            "cost": {
                "optimistic": "number",
                "most_likely": "number",
                "pessimistic": "number"
            },
            "dependencies": ["string"]
        }
    ]
}

# Formato para resultados Monte Carlo
montecarlo_output_schema = {
    "simulations": [
        {"run_id": "number", "total_duration": "number", "total_cost": "number"}
    ],
    "expected_duration": "number",
    "expected_cost": "number"
}