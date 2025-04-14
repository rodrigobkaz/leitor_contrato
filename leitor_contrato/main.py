from leitor_contrato.hubspot_client import (
    search_recent_closed_deals as get_deals,
    get_associated_company_id,
    create_note_for_company
)
from leitor_contrato.processor import process_contract_from_deal

def main():
    print("🔍 Buscando negócios fechados nas últimas 24h...")
    deals = get_deals()

    if not deals:
        print("⚠️ Nenhum negócio encontrado.")
        return

    print(f"📊 Encontrados {len(deals)} negócios fechados nas últimas 24h.")

    for deal in deals:
        print(f"\n📄 Processando deal ID {deal['id']}...")
        result = process_contract_from_deal(deal)

        if result:
            print_relatorio_contrato(deal["id"], result)

            company_id = get_associated_company_id(deal["id"])
            if company_id:
                print(f"🏢 Empresa associada ao deal: {company_id}")
                create_note_for_company(company_id, result)
            else:
                print("⚠️ Empresa associada não encontrada.")
        else:
            print("⚠️ Falha ao processar este contrato.")

def print_relatorio_contrato(deal_id, info):
    print(f"\n📄 Análise do Contrato (Deal ID: {deal_id})\n")
    print(f"✅ Valor total..............: R$ {info.get('valor_total') or 'não encontrado'}")
    print(f"✅ Duração do contrato......: {info.get('duracao_meses') or 'não encontrada'} meses")
    print(f"✅ Fidelidade...............: {info.get('fidelidade') or 'não encontrada'}")
    print(f"✅ Reajuste.................: {info.get('reajuste') or 'não encontrado'}")
    print(f"✅ Inadimplência............: {info.get('inadimplencia') or 'não encontrada'}")
    print(f"✅ Aviso prévio.............: {info.get('prazo_cancelamento') or 'não encontrado'}")
    print(f"✅ Multa rescisória.........: {info.get('multa_rescisoria') or 'não encontrada'}")

    print("\n📝 Trecho relevante:")
    print(info.get('snippet', '[sem trecho]'))

    print("\n📌 Observações finais:")
    observacoes = info.get("observacoes_finais", [])
    if observacoes:
        for obs in observacoes:
            print(f"- {obs}")
    else:
        print("Nenhuma observação automática gerada.")

    print("-" * 80)

if __name__ == "__main__":
    main()
