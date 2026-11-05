# Ejercicio 1 - Sanitización y Análisis Estadístico de Sensores


def limpiar_registro_sensor(registro_raw):
    # Limpiamos los espacios sobrantes
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()

    temp_raw = str(registro_raw.get("temperatura", "0")).strip()
    temp_limpia = (
        temp_raw.replace("°C", "")
        .replace("°c", "")
        .replace("C", "")
        .replace("c", "")
        .replace("°", "")
        .strip()
    )
    temperatura = float(temp_limpia)

    # Si no se registró ubicación o está vacía, asignamos un valor por defecto 
    ubicacion_raw = registro_raw.get("ubicacion")
    if not ubicacion_raw or not str(ubicacion_raw).strip():
        ubicacion = "Sin especificar"
    else:
        ubicacion = str(ubicacion_raw).strip()

    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    if not lista_sensores_limpios:
        return ([], 0.0)

    lista_sensores_alerta = []
    suma_temperaturas = 0.0

    for sensor in lista_sensores_limpios:
        temp = sensor["temperatura"]
        suma_temperaturas += temp

        if temp > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

    promedio_temperatura = round(suma_temperaturas / len(lista_sensores_limpios), 2)
    return (lista_sensores_alerta, promedio_temperatura)


if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002 ", "temperatura": "31.2C", "ubicacion": "Planta Sur"},
        {"sensor_id": "  SENSOR-003", "temperatura": "19.8°C"},
        {"sensor_id": " SENSOR-004 ", "temperatura": "34.0C", "ubicacion": "Planta Central"},
        {"sensor_id": "SENSOR-005", "temperatura": "28.0 C", "ubicacion": "   "},
    ]

    print("--- Limpieza de registros ---")
    sensores_limpios = []
    for reg in registros_crudos:
        registro_limpio = limpiar_registro_sensor(reg)
        sensores_limpios.append(registro_limpio)
        print(f"ID: {registro_limpio['sensor_id']} | Temp: {registro_limpio['temperatura']}°C | Ubicación: {registro_limpio['ubicacion']}")

    umbral = 30.0
    sensores_alerta, promedio = generar_resumen_sensores(sensores_limpios, umbral)

    print("\n--- Reporte Consolidado de Sensores ---")
    print(f"Umbral configurado: {umbral:.1f}°C")
    print(f"Promedio térmico global: {promedio:.2f}°C")
    print(f"Sensores en alerta (superan el umbral): {sensores_alerta}")
