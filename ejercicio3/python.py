import unittest
from django.shortcuts import render


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
  """Calcula las emisiones de carbono basadas en el consumo en kWh

  y un factor de emisión determinado.
  """
  if consumo_kwh < 0:
    raise ValueError("El consumo en kWh no puede ser negativo.")
  return consumo_kwh * factor_emision


class TestCalculoEmisiones(unittest.TestCase):
  """Casos de prueba unitarios para validar la función de cálculo

  de emisiones de carbono.
  """

  def test_calculo_nominal_personalizado(self):
    resultado = calcular_emisiones_carbono(1500, 0.4)
    self.assertEqual(resultado, 600.0)

  def test_calculo_con_factor_por_defecto(self):
    resultado = calcular_emisiones_carbono(500)
    self.assertEqual(resultado, 200.0)

  def test_calculo_consumo_cero(self):
    resultado = calcular_emisiones_carbono(0)
    self.assertEqual(resultado, 0.0)

  def test_consumo_negativo_lanza_excepcion(self):
    with self.assertRaises(ValueError):
      calcular_emisiones_carbono(-150)


def obtener_metricas_consumo(registros):
  """Procesa una lista de registros de consumo para calcular

  el total global de emisiones y detectar la planta con mayor consumo.
  """
  total_global_emisiones = 0.0
  planta_mayor_consumo = None
  max_consumo = -1.0

  for reg in registros:
    planta = reg.get("planta") if isinstance(reg, dict) else reg.planta
    consumo = reg.get("consumo") if isinstance(reg, dict) else reg.consumo

    emisiones = calcular_emisiones_carbono(consumo)
    total_global_emisiones += emisiones

    if consumo > max_consumo:
      max_consumo = consumo
      planta_mayor_consumo = planta

  return {
      "total_global_emisiones": total_global_emisiones,
      "planta_mayor_consumo": planta_mayor_consumo,
      "consumo_maximo": max_consumo,
  }


def vista_panel_sustentabilidad(request):
  """Vista de Django que procesa las métricas de consumo

  y renderiza el panel de sustentabilidad corporativa.
  """
  registros_industriales = [
      {"planta": "Planta Metalúrgica Central", "consumo": 12500},
      {"planta": "Planta Ensamblaje Norte", "consumo": 8400},
      {"planta": "Planta Logística Sur", "consumo": 15200},
      {"planta": "Planta Química Este", "consumo": 9100},
  ]

  metricas = obtener_metricas_consumo(registros_industriales)

  contexto = {
      "registros": registros_industriales,
      "total_emisiones": metricas["total_global_emisiones"],
      "planta_critica": metricas["planta_mayor_consumo"],
      "max_consumo": metricas["consumo_maximo"],
  }

  return render(request, "sustentabilidad/panel.html", contexto)


if __name__ == "__main__":
  unittest.main()
