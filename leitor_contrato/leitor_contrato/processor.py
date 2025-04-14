
from leitor_contrato.hubspot_client import get_file_download_url
from leitor_contrato.pdf_reader import download_and_read_pdf
from leitor_contrato.extractor import extract_contract_info

def process_contract_from_deal(deal):
    file_id = deal["properties"].get("contrato")
    if not file_id:
        print("⚠️ Deal não possui file_id no campo 'contrato'")
        return None

    print(f"🔗 file_id encontrado: {file_id}")

    url = get_file_download_url(file_id)
    if not url:
        print(f"⚠️ Falha ao obter URL do arquivo para file_id: {file_id}")
        return None

    print(f"📥 Baixando PDF de: {url}")

    text = download_and_read_pdf(url)
    if not text:
        print(f"⚠️ Falha ao extrair texto do PDF do file_id: {file_id}")
        return None

    return extract_contract_info(text)
