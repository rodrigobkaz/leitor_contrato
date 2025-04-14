import os
import time
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()

API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_file_download_url(file_id):
    url = f"{BASE_URL}/files/v3/files/{file_id}/signed-url"
    response = requests.get(url, headers=HEADERS)
    if not response.ok:
        print(f"Erro ao obter signed URL do arquivo {file_id}: {response.status_code}, {response.text}")
        return None
    data = response.json()
    return data.get("url")

def create_note_for_company(company_id, contrato_info):
    url = f"{BASE_URL}/engagements/v1/engagements"

    timestamp = int(time.time() * 1000)

    descricao = f"""
📄 Contrato processado automaticamente:

- Duração: {contrato_info.get("duracao_meses", "N/A")} meses
- Valor Total: R$ {contrato_info.get("valor_total", "N/A")}

Trecho do contrato:
{contrato_info.get("snippet", "")}

(Análise gerada via GitHub Actions 🚀)
"""

    payload = {
        "engagement": {
            "active": True,
            "type": "NOTE",
            "timestamp": timestamp
        },
        "associations": {
            "companyIds": [company_id]
        },
        "metadata": {
            "body": descricao.strip()
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if not response.ok:
        print(f"❌ Erro ao criar nota (engagement) para empresa {company_id}: {response.status_code}, {response.text}")
    else:
        print(f"📝 Nota visível criada com sucesso para a empresa {company_id}.")

def search_recent_closed_deals():
    url = f"{BASE_URL}/crm/v3/objects/deals/search"
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    timestamp = int(one_day_ago.timestamp() * 1000)

    payload = {
        "filterGroups": [
            {
                "filters": [
                    {"propertyName": "dealstage", "operator": "EQ", "value": "closedwon"},
                    {"propertyName": "closedate", "operator": "GTE", "value": str(timestamp)}
                ]
            }
        ],
        "properties": ["dealname", "contrato"],
        "limit": 10
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if not response.ok:
        print(f"Erro ao buscar negócios fechados: {response.status_code}, {response.text}")
        return []

    return response.json().get("results", [])

def get_associated_company_id(deal_id):
    url = f"{BASE_URL}/crm/v4/objects/deals/{deal_id}/associations/companies"
    response = requests.get(url, headers=HEADERS)
    if not response.ok:
        print(f"Erro ao buscar empresa associada ao deal {deal_id}: {response.status_code}, {response.text}")
        return None
    results = response.json().get("results", [])
    if not results:
        return None
    return results[0].get("toObjectId")
