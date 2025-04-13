
from leitor_contrato.hubspot_client import get_file_download_url
from leitor_contrato.pdf_reader import download_and_read_pdf
from leitor_contrato.extractor import extract_contract_info

def process_contract_from_deal(deal):
    file_id = deal["properties"].get("contrato")
    if not file_id:
        return None
    url = get_file_download_url(file_id)
    if not url:
        return None
    text = download_and_read_pdf(url)
    return extract_contract_info(text)
