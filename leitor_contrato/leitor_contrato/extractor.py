import re
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("pt_core_news_sm")

def extract_contract_info(text):
    if not text:
        return None

    doc = nlp(text)

    duracao, duracao_context = extract_duracao(text)
    valor, valor_context = extract_valor(text)

    matcher = Matcher(nlp.vocab)
    add_matcher_patterns(matcher)
    matches = matcher(doc)

    clausulas = {
        "prazo_cancelamento": None,
        "inadimplencia": None,
        "fidelidade": None,
        "reajuste": None,
        "multa_rescisoria": None
    }

    for match_id, start, end in matches:
        span = doc[start:end].sent
        label = nlp.vocab.strings[match_id]
        if clausulas.get(label) is None:
            clausulas[label] = span.text.strip()

    # Observações automatizadas
    observacoes = []
    if duracao:
        observacoes.append(f"Contrato com duração mínima de {duracao} meses.")
    if valor:
        observacoes.append(f"Valor total identificado: R$ {valor}.")
    if clausulas.get("fidelidade"):
        observacoes.append("Cláusula de fidelidade detectada.")
    if clausulas.get("multa_rescisoria"):
        observacoes.append("Penalidade por rescisão antecipada detectada.")
    if clausulas.get("reajuste"):
        observacoes.append("Cláusula de reajuste identificada.")
    if clausulas.get("prazo_cancelamento"):
        observacoes.append("Cláusula de aviso prévio para cancelamento detectada.")

    return {
        "duracao_meses": duracao,
        "valor_total": valor,
        "vigencia": clausulas.get("fidelidade"),
        "prazo_cancelamento": clausulas.get("prazo_cancelamento"),
        "inadimplencia": clausulas.get("inadimplencia"),
        "fidelidade": clausulas.get("fidelidade"),
        "reajuste": clausulas.get("reajuste"),
        "multa_rescisoria": clausulas.get("multa_rescisoria"),
        "snippet": build_snippet(text, duracao_context or valor_context),
        "observacoes_finais": observacoes
    }

def add_matcher_patterns(matcher):
    matcher.add("prazo_cancelamento", [[{"LOWER": {"IN": ["aviso", "notificação"]}}, {"LOWER": "prévio"}]])
    matcher.add("inadimplencia", [[{"LOWER": "inadimplência"}], [{"LOWER": "inadimplemento"}]])
    matcher.add("fidelidade", [[{"LOWER": "reduzidos"}], [{"LOWER": "redução"}], [{"LOWER": "fidelidade"}]])
    matcher.add("reajuste", [[{"LOWER": "reajuste"}], [{"LOWER": "igp-m"}], [{"LOWER": "índice"}]])
    matcher.add("multa_rescisoria", [
        [{"LOWER": "multa"}, {"LOWER": "não"}, {"LOWER": "compensatória"}],
        [{"LOWER": "multa"}, {"IS_DIGIT": True}, {"LOWER": "%"}],
        [{"LOWER": "rescisão"}, {"LOWER": "antes"}, {"LOWER": "do"}],
        [{"LOWER": "incorrerá"}, {"LOWER": "em"}, {"LOWER": "multa"}]
    ])

def extract_duracao(text):
    padroes = [
        r"(?:vig[eê]ncia|dura[cç][aã]o|prazo).*?(\d{1,2})\s*(?:meses|mês|mes)",
        r"(\d{1,2})\s*(?:meses|mês|mes).*?(?:vig[eê]ncia|dura[cç][aã]o|prazo)",
        r"antes dos (\d{1,2}) primeiros meses",
        r"durante os (\d{1,2}) primeiros meses"
    ]
    for padrao in padroes:
        match = re.search(padrao, text, flags=re.IGNORECASE)
        if match:
            return int(match.group(1)), match.group(0)
    return None, None

def extract_valor(text):
    padroes = [
        r"(?:valor\s*(?:total)?|R\$|ANUIDADE FIXA)\s*[:\-]?\s*(R\$)?\s?(\d{1,3}(?:[\.,]\d{3})*[\.,]\d{2})",
        r"(R\$)?\s?(\d{1,3}(?:[\.,]\d{3})*[\.,]\d{2})\s*(?:reais|BRL)?"
    ]
    for padrao in padroes:
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
