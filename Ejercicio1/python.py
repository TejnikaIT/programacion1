def limpiar_registro_sensor(registro_raw):
    """
    Punto A: Normaliza un diccionario con datos crudos de un sensor.
    - Elimina espacios sobrantes en el identificador.
    - Convierte la temperatura a float removiendo sufijos de unidad ('C', '°C').
    - Asigna una ubicación por defecto si no está registrada o está vacía.
    """
    # 1. Limpieza del identificador
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()
    
    # 2. Limpieza y conversión de la temperatura
    temp_raw = str(registro_raw.get("temperatura", "0"))
    # Reemplazamos posibles sufijos y limpiamos espacios
    temp_clean = temp_raw.replace("°C", "").replace("C", "").strip()
    try:
        temperatura = float(temp_clean)
    except ValueError:
        temperatura = 0.0  # Valor seguro ante datos corruptos
        
    # 3. Ubicación con valor por defecto seguro
    ubicacion_raw = registro_raw.get("ubicacion")
    if not ubicacion_raw or not str(ubicacion_raw).strip():
        ubicacion = "Planta General"
    else:
        ubicacion = str(ubicacion_raw).strip()
        
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """
    Punto B: Monitoreo y Mapeo Estadístico.
    Toma la lista de sensores limpios y un umbral, retornando una tupla:
    (lista_sensores_alerta, promedio_temperatura)
    """
    if not lista_sensores_limpios:
        return [], 0.0
        
    lista_sensores_alerta = []
    suma_temperaturas = 0.0
    total_sensores = len(lista_sensores_limpios)
    
    for sensor in lista_sensores_limpios:
        temp = sensor["temperatura"]
        suma_temperaturas += temp
        
        # Identificar dispositivos que superan el umbral
        if temp > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])
            
    promedio_temperatura = suma_temperaturas / total_sensores
    
    return lista_sensores_alerta, promedio_temperatura


# ==========================================
# Bloque de Ejecución y Demostración
# ==========================================
if __name__ == "__main__":
   
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 30.2 °C ", "ubicacion": "Planta Sur"},
        {"sensor_id": " SENSOR-003 ", "temperatura": "28.0C"}, 
        {"sensor_id": "SENSOR-004", "temperatura": "35.8C", "ubicacion": "Planta Este"},
        {"sensor_id": " SENSOR-005 ", "temperatura": "22.1 C", "ubicacion": "Planta Oeste"}
    ]
    
    print("--- 1. PROCESO DE SANITIZACIÓN (Punto A) ---")
    sensores_limpios = []
    for reg in registros_crudos:
        sensor_normalizado = limpiar_registro_sensor(reg)
        sensores_limpios.append(sensor_normalizado)
        print(f"Crudo: {reg}")
        print(f"LimPIO: {sensor_normalizado}\n")
        
    
    UMBRAL = 29.0
    
    print(f"--- 2. ANÁLISIS ESTADÍSTICO Y ALERTAS (Punto B) [Umbral: {UMBRAL}°C] ---")
    sensores_en_alerta, promedio_global = generar_resumen_sensores(sensores_limpios, UMBRAL)
    
    
    print("========================================")
    print("       REPORTE CONSOLIDADO ECOTECH      ")
    print("========================================")
    print(f"• Promedio térmico global: {promedio_global:.2f} °C")
    print(f"• Dispositivos en estado de alerta: {sensores_en_alerta if sensores_en_alerta else 'Ninguno'}")
    print("----------------------------------------")
    print("Detalle de dispositivos analizados:")
    for s in sensores_limpios:
        estado = "ALERTA" * (s["temperatura"] > UMBRAL) or "Normal"
        print(f" - [{s['sensor_id']}] Ubicación: {s['ubicacion']} | Temp: {s['temperatura']} °C ({estado})")
    print("========================================")
