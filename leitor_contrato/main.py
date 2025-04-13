
from leitor_contrato.processor import process_contract_from_deal

if __name__ == "__main__":
    fake_deal = {"properties": {"contrato": "123456"}}
    resultado = process_contract_from_deal(fake_deal)
    print("Resultado:", resultado)
