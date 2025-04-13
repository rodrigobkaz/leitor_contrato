
import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def get_file_download_url(file_id):
    url = f"{BASE_URL}/files/v3/files/{file_id}"
    response = requests.get(url, headers=HEADERS)
    if not response.ok:
        print(f"Erro ao obter metadados do arquivo {file_id}: {response.text}")
        return None
    return response.json().get("url")
