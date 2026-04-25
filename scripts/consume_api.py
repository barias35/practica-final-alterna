import requests
import time
import sys
import os # Importante para leer variables de entorno


BASE_URL = os.getenv("BASE_URL", "")

def wait_for_api(retries=5, delay=2):
    """Espera a que la API responda antes de proceder."""
    print(f"DEBUG: Intentando conectar a {BASE_URL}") # Útil para ver en los logs de GitHub
    for i in range(retries):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print(f"✅ API lista en el intento {i+1}")
                return True
        except requests.exceptions.ConnectionError:
            print(f"Sincronizando: Intento {i+1} fallido...")
            time.sleep(delay)
    return False

# ... el resto de tus funciones run_consumption y el bloque __main__ se mantienen igual

def run_consumption():
    try:
        # Intentamos obtener los items definidos en tu app.py
        response = requests.get(f"{BASE_URL}/items")
        response.raise_for_status() # Lanza excepción si hay error 4xx o 5xx
        
        items = response.json()
        print(f"🚀 Datos consumidos exitosamente: {items}")
        return True
    except Exception as e:
        print(f"❌ Error durante el consumo: {e}")
        return False

if __name__ == "__main__":
    if not wait_for_api():
        print("🚨 Error Crítico: La API nunca estuvo disponible.")
        sys.exit(1) # Código 1: Falla el pipeline
        
    if not run_consumption():
        print("🚨 Error Crítico: Fallo en la lógica de consumo.")
        sys.exit(1) # Código 1: Falla el pipeline
    
    print("✅ Proceso completado exitosamente.")
    sys.exit(0) # Código 0: Éxito