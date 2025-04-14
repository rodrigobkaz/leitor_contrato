from leitor_contrato.hubspot_client import (
    search_recent_closed_deals,
    get_associated_company_id,
    create_note_for_company
)
from leitor_contrato.processor import process_contract_from_deal

def main():
    deals = search_recent_closed_deals()
    print(f"Encontrados {len(deals)} negócios fechados nas últimas 24h.")

    for deal in deals:
        deal_id = deal.get("id")
        print(f"📄 Processando deal ID {deal_id}...")

        result = process_contract_from_deal(deal)
        if not result:
            print(f"⚠️ Não foi possível extrair contrato do deal {deal_id}")
            continue

        company_id = get_associated_company_id(deal_id)
        if not company_id:
            print(f"⚠️ Nenhuma empresa associada ao deal {deal_id}")
            continue

        create_note_for_company(company_id, result)

if __name__ == "__main__":
    main()
