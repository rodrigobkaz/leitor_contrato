
from PyPDF2 import PdfReader
import tempfile
import os
import requests

def download_and_read_pdf(url):
    response = requests.get(url)
    if not response.ok:
        print(f"Erro ao baixar PDF: {response.status_code}")
        return None
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp.flush()
        try:
            reader = PdfReader(tmp.name)
            return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        finally:
            os.unlink(tmp.name)
