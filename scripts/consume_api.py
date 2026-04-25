import requests
import time

BASE_URL = "http://localhost:5000"

def wait_for_api(retries=5, delay=2):
    """Espera a que la API esté disponible en localhost."""
    for i in range(retries):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print(f"✅ API conectada en el intento {i+1}")
                return True
        except requests.exceptions.ConnectionError:
            print(f"Wait: Intento {i+1} fallido, reintentando...")
            time.sleep(delay)
    return False

def list_all_items():
    response = requests.get(f"{BASE_URL}/items")
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == "__main__":
    if wait_for_api():
        items = list_all_items()
        print(f"Items encontrados: {items}")
    else:
        print("❌ API is unreachable after retries")
        exit(1) # Forzamos error en el pipeline si no conecta