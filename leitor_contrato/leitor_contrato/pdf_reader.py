from PyPDF2 import PdfReader
import tempfile
import os
import requests

def download_and_read_pdf(url):
    response = requests.get(url, allow_redirects=True)
    
    # Valida se é um PDF
    content_type = response.headers.get("Content-Type", "")
    if "pdf" not in content_type.lower():
        print(f"❌ Resposta não é um PDF. Content-Type recebido: {content_type}")
        return None

    if not response.ok:
        print(f"Erro ao baixar PDF: {response.status_code}")
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp.flush()
        try:
            reader = PdfReader(tmp.name)
            return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        except Exception as e:
            print(f"⚠️ Erro ao ler PDF: {e}")
            return None
        finally:
            os.unlink(tmp.name)
