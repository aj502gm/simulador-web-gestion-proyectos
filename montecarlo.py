import numpy as np

simulaciones = 1000

def run_simulation(activities_json, critical_path):
    duraciones = []
    costos = []

    for i in range(simulaciones):
        duracion_iteracion = 0
        costo_iteracion = 0

        for activity in activities_json["activities"]:
            if activity["id"] in critical_path:
                duracion_iteracion += (float)(np.random.triangular(
                    left = activity["duration"]["optimistic"],
                    mode = activity["duration"]["most_likely"],
                    right = activity["duration"]["pessimistic"],
                    size = 1)[0])
                
            costo_iteracion += (float)(np.random.triangular(
                left = activity["cost"]["optimistic"],
                mode = activity["cost"]["most_likely"],
                right = activity["cost"]["pessimistic"],
                size = 1)[0])
            
        duraciones.append(duracion_iteracion)
        costos.append(costo_iteracion)

    duraciones_result = { "duraciones": duraciones, "media": np.mean(duraciones), "mediana": np.median(duraciones), "desviacion_standar": np.std(duraciones), "minimo": np.min(duraciones), "maximo": np.max(duraciones) }

    costos_result = { "costos": costos, "media": np.mean(costos), "mediana": np.median(costos), "desviacion_standar": np.std(costos), "minimo": np.min(costos), "maximo": np.max(costos) }

    return duraciones_result, costos_result