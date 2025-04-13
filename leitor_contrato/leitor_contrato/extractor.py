
import re

def extract_contract_info(text):
    if not text:
        return None
    duracao_match = re.search(r"(?:Duração|Duracao).*?(\d{1,2})\s*meses", text, re.IGNORECASE)
    valor_match = re.search(r"(?:R\$\s?|Valor total).*?(\d+[\.,]\d{2,})", text)
    return {
        "duracao_meses": int(duracao_match.group(1)) if duracao_match else None,
        "valor_total": valor_match.group(1).replace(",", ".") if valor_match else None,
        "snippet": text[:400]
    }
