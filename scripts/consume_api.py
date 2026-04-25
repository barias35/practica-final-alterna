import requests

BASE_URL = "http://localhost:5000"

def get_health_status() -> bool:
    """Verifica si la API está arriba."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        return response.status_code == 200 and response.json().get("status") == "ok"
    except requests.exceptions.ConnectionError:
        return False

def list_all_items():
    """Lista los items de la API."""
    response = requests.get(f"{BASE_URL}/items")
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == "__main__":
    if get_health_status():
        print("✅ API is healthy")
        items = list_all_items()
        print(f"Items encontrados: {items}")
    else:
        print("❌ API is unreachable")