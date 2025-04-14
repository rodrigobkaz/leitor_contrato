import re
import spacy
from spacy.matcher import Matcher

# Carrega modelo do spaCy (use no setup local: python -m spacy download pt_core_news_sm)
nlp = spacy.load("pt_core_news_sm")

def extract_contract_info(text):
    if not text:
        return None

    doc = nlp(text)

    # Regex tradicionais
    duracao, duracao_context = extract_duracao(text)
    valor, valor_context = extract_valor(text)

    # Matcher do spaCy
    matcher = Matcher(nlp.vocab)
    add_matcher_patterns(matcher)
    matches = matcher(doc)

    clausulas = {
        "prazo_cancelamento": None,
        "inadimplencia": None,
        "fidelidade": None,
        "reajuste": None
    }

    for match_id, start, end in matches:
        span = doc[start:end].sent
        label = nlp.vocab.strings[match_id]
        if clausulas.get(label) is None:
            clausulas[label] = span.text.strip()

    return {
        "duracao_meses": duracao,
        "valor_total": valor,
        "vigencia": clausulas.get("fidelidade"),
        "prazo_cancelamento": clausulas.get("prazo_cancelamento"),
        "inadimplencia": clausulas.get("inadimplencia"),
        "fidelidade": clausulas.get("fidelidade"),
        "reajuste": clausulas.get("reajuste"),
        "snippet": build_snippet(text, duracao_context or valor_context)
    }

def add_matcher_patterns(matcher):
    matcher.add("prazo_cancelamento", [[{"LOWER": {"IN": ["aviso", "notificação"]}}, {"LOWER": "prévio"}]])
    matcher.add("inadimplencia", [[{"LOWER": "inadimplência"}], [{"LOWER": "inadimplemento"}]])
    matcher.add("fidelidade", [[{"LOWER": "reduzidos"}], [{"LOWER": "redução"}]])
    matcher.add("reajuste", [[{"LOWER": "reajuste"}], [{"LOWER": "igp-m"}], [{"LOWER": "índice"}]])

def extract_duracao(text):
    padroes_duracao = [
        r"(?:vig[eê]ncia|dura[cç][aã]o|prazo).*?(\d{1,2})\s*(?:meses|mês|mes)",
        r"(\d{1,2})\s*(?:meses|mês|mes)\s*(?:de)?\s*(?:vig[eê]ncia|dura[cç][aã]o|prazo)"
    ]
    for padrao in padroes_duracao:
        match = re.search(padrao, text, flags=re.IGNORECASE)
        if match:
            return int(match.group(1)), match.group(0)
    return None, None

def extract_valor(text):
    padroes_valor = [
        r"(?:valor\s*(?:total)?|R\$)\s*[:\-]?\s*(R\$)?\s?(\d{1,3}(?:[\.,]\d{3})*[\.,]\d{2})",
        r"(R\$)?\s?(\d{1,3}(?:[\.,]\d{3})*[\.,]\d{2})\s*(?:reais|BRL)?"
    ]
    for padrao in padroes_valor:
        match = re.search(padrao, text, flags=re.IGNORECASE)
        if match:
            valor_bruto = match.group(2).replace('.', '').replace(',', '.')
            return valor_bruto, match.group(0)
    return None, None

def build_snippet(text, contexto):
    if not contexto:
        return text[:400]
    index = text.lower().find(contexto.lower())
    if index == -1:
        return text[:400]
    start = max(index - 100, 0)
    end = min(index + 300, len(text))
    return text[start:end].strip()
