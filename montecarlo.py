import numpy as np

simulaciones = 5000


def run_simulation(activities_json, critical_path):
    duraciones = []
    costos = []

    for i in range(simulaciones):
        duracion_iteracion = 0
        costo_iteracion = 0

        for activity in activities_json["activities"]:
            if activity["id"] in critical_path:
                valor_iteracion = random_pert(
                    activity["duration"]["optimistic"],
                    activity["duration"]["most_likely"],
                    activity["duration"]["pessimistic"],
                )

                valor_duracion_iteracion = max(
                    0, valor_iteracion
                )  # Asegurar que no sea negativo
                duracion_iteracion += valor_duracion_iteracion

            valor_costo_iteracion = random_pert(
                activity["cost"]["optimistic"],
                activity["cost"]["most_likely"],
                activity["cost"]["pessimistic"],
            )

            valor_costo_iteracion = max(0, valor_costo_iteracion)
            costo_iteracion += valor_costo_iteracion

        duraciones.append(duracion_iteracion)
        costos.append(costo_iteracion)

    duraciones_result = {
        "duraciones": duraciones,
        "media": np.mean(duraciones),
        "mediana": np.median(duraciones),
        "desviacion_standar": np.std(duraciones),
        "minimo": np.min(duraciones),
        "maximo": np.max(duraciones),
    }

    costos_result = {
        "costos": costos,
        "media": np.mean(costos),
        "mediana": np.median(costos),
        "desviacion_standar": np.std(costos),
        "minimo": np.min(costos),
        "maximo": np.max(costos),
    }

    return duraciones_result, costos_result


def run_projection_simulation(evm_results):
    costos = []

    for i in range(simulaciones):
        costo_iteracion = random_pert(
            evm_results["EAC Optimista"],
            evm_results["EAC Realista"],
            evm_results["EAC Pesimista"],
        )

        costo_iteracion = max(0, costo_iteracion)

        costos.append(costo_iteracion)

    costos_result = {
        "costos": costos,
        "media": np.mean(costos),
        "mediana": np.median(costos),
        "desviacion_standar": np.std(costos),
        "minimo": np.min(costos),
        "maximo": np.max(costos),
    }

    return costos_result


def random_pert(optimista, mas_probable, pesimista):
    """
    Genera valores aleatorios con distribución PERT.

    Parámetros:
    - optimista (float): El valor más bajo esperado.
    - mas_probable (float): El valor más probable.
    - pesimista (float): El valor más alto esperado.
    """
    alpha = 1 + 4 * (mas_probable - optimista) / (pesimista - optimista)
    beta = 1 + 4 * (pesimista - mas_probable) / (pesimista - optimista)
    sample = np.random.beta(alpha, beta, 1)[0]
    return optimista + sample * (pesimista - optimista)
