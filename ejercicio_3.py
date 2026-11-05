# Ejercicio 3 - Auditoría con Tests Unitarios e Integración Web

import unittest

try:
    from django.shortcuts import render
except ImportError:
    # Definición auxiliar en caso de correr las pruebas sin tener Django instalado en el entorno
    def render(request, template_name, context=None):
        return {"template": template_name, "context": context}


# Punto A: Algoritmo y pruebas unitarias

def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    if consumo_kwh < 0:
        raise ValueError("El consumo en kWh no puede ser negativo.")
    return consumo_kwh * factor_emision


class TestCalculoEmisiones(unittest.TestCase):
    def test_calculo_consumo_nominal(self):
        resultado = calcular_emisiones_carbono(100)
        self.assertAlmostEqual(resultado, 40.0)

    def test_calculo_con_factor_personalizado(self):
        resultado = calcular_emisiones_carbono(250, 0.5)
        self.assertAlmostEqual(resultado, 125.0)

    def test_calculo_consumo_cero(self):
        resultado = calcular_emisiones_carbono(0)
        self.assertEqual(resultado, 0.0)

    def test_consumo_negativo_eleva_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50)


# Punto B: Procesamiento de métricas y vista de Django

def obtener_metricas_consumo(registros):
    if not registros:
        return {
            "total_emisiones": 0.0,
            "planta_mayor_consumo": None,
        }

    total_emisiones = 0.0
    planta_mayor_consumo = None
    mayor_consumo = -1.0

    for reg in registros:
        consumo = reg["consumo_kwh"]
        factor = reg.get("factor_emision", 0.4)

        emisiones = calcular_emisiones_carbono(consumo, factor)
        total_emisiones += emisiones

        if consumo > mayor_consumo:
            mayor_consumo = consumo
            planta_mayor_consumo = reg["planta"]

    return {
        "total_emisiones": round(total_emisiones, 2),
        "planta_mayor_consumo": planta_mayor_consumo,
    }


def vista_panel_sustentabilidad(request):
    historial_consumos = [
        {"planta": "Planta Norte", "consumo_kwh": 1500.0},
        {"planta": "Planta Sur", "consumo_kwh": 3200.0},
        {"planta": "Planta Central", "consumo_kwh": 2100.0},
    ]

    metricas = obtener_metricas_consumo(historial_consumos)

    contexto = {
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "registros": historial_consumos,
    }

    try:
        return render(request, "sustentabilidad/panel.html", contexto)
    except Exception:
        # Fallback si se ejecuta de forma aislada sin un proyecto Django activo
        return {"template": "sustentabilidad/panel.html", "context": contexto}


if __name__ == "__main__":
    # 1. Pruebas unitarias con unittest (Punto A)
    unittest.main(exit=False)

    # 2. Comprobación de la vista de Django (Punto B)
    print("\n--- Comprobación de la Vista Django (Punto B) ---")
    respuesta = vista_panel_sustentabilidad(None)
    print(f"Plantilla invocada: {respuesta.get('template')}")
    print(f"Contexto generado: {respuesta.get('context')}")
