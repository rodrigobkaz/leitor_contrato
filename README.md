# Leitor de Contrato

Extrai informações de contratos em PDF armazenados no HubSpot Deals.

## Instalação

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` com sua chave de API do HubSpot:

```
HUBSPOT_API_KEY=xxxxxxxxxx
```

## Uso

```python
from leitor_contrato.processor import process_contract_from_deal

deal = {"properties": {"contrato": "123456"}}
info = process_contract_from_deal(deal)
print(info)
```
