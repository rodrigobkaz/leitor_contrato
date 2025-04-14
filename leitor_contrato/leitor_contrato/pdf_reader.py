import pdfplumber
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
        text = []

        try:
            with pdfplumber.open(tmp.name) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text.append(extracted)
            
            full_text = "\n".join(text)
            return normalize_text(full_text) if full_text else None

        except Exception as e:
            print(f"⚠️ Erro ao ler PDF com pdfplumber: {e}")
            return None

        finally:
            os.unlink(tmp.name)

def normalize_text(text):
    """
    Remove espaços duplicados, quebra de linhas desnecessárias, e normaliza o texto.
    """
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(lines)
