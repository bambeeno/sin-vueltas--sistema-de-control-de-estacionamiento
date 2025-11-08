import requests
import random
import time

URL = "http://localhost:5000/api/update"

while True:
    data = {
        "espacio_id": 1,
        "ocupado": random.choice([True, False]),
        "distancia": random.uniform(10, 80)
    }
    r = requests.post(URL, json=data)
    print("POST:", r.status_code, data)
    time.sleep(3)
