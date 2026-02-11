import requests

BASE_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/"

def get_car_models(make: str):
    url = f"{BASE_URL}{make}?format=json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Errore API auto: {response.status_code}")

    data = response.json()
    return [model["Model_Name"] for model in data.get("Results", [])]
