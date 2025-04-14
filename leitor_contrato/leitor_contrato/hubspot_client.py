
import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def create_note_for_company(company_id, contrato_info):
    url = f"{BASE_URL}/crm/v3/objects/notes"
    
    descricao = f"""
📄 Contrato processado automaticamente:

- Duração: {contrato_info.get("duracao_meses", "N/A")} meses
- Valor Total: R$ {contrato_info.get("valor_total", "N/A")}

Trecho do contrato:
{contrato_info.get("snippet", "")}

(Análise gerada via GitHub Actions 🚀)
"""

    payload = {
        "properties": {
            "hs_note_body": descricao.strip()
        },
        "associations": [
            {
                "to": {"id": company_id},
                "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 1}]
            }
        ]
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if not response.ok:
        print(f"Erro ao criar nota para a empresa {company_id}: {response.text}")
    else:
        print(f"📝 Nota criada com sucesso para a empresa {company_id}.")

