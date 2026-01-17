import sys
from typing import Optional

# Imports das classes do sistema
from produto import criar_produto, listar_produtos, buscar_produto_por_sku, atualizar_produto
from cliente import criar_cliente, listar_clientes, buscar_cliente_por_cpf
from carrinho import Carrinho
from pedido import criar_pedido_do_carrinho, listar_pedidos, STATUS_PAGO
from frete import Frete
from pagamento import Pagamento

# Import das exceções para tratamento correto (Critério 1)
from excecoes import LojaErro, EstoqueInsuficienteErro, PagamentoRecusadoErro

# --- Função de Relatórios (Requisito 9 do PDF) ---
def exibir_relatorios() -> None:
    pedidos = listar_pedidos()
    if not pedidos:
        print("\nNenhum pedido registrado para gerar relatórios.")
        return

    print("\n" + "="*30)
    print("   RELATÓRIOS GERENCIAIS")
    print("="*30)

    # 1. Faturamento Total (Apenas pedidos PAGOS)
    pedidos_pagos = [p for p in pedidos if p.status == STATUS_PAGO]
    faturamento = sum(p.total_final for p in pedidos_pagos)
    
    # 2. Contagem por Status
    contagem = {}
    for p in pedidos:
        contagem[p.status] = contagem.get(p.status, 0) + 1

    # 3. Ticket Médio
    ticket_medio = faturamento / len(pedidos_pagos) if pedidos_pagos else 0.0

    print(f"💰 Faturamento Total (Pagos): R$ {faturamento:.2f}")
    print(f"🎫 Ticket Médio: R$ {ticket_medio:.2f}")
    print("\n📊 Pedidos por Status:")
    for status, qtd in contagem.items():
        percentual = (qtd / len(pedidos)) * 100
        print(f"   - {status}: {qtd} ({percentual:.1f}%)")
    print("="*30)
    input("Pressione Enter para voltar...")

# --- Funções do Menu e Fluxo ---

def menu() -> str:
    print("\n" + "="*30)
    print("   SISTEMA DE LOJA VIRTUAL")
    print("="*30)
    print("1. Cadastrar Cliente")
    print("2. Cadastrar Produto")
    print("3. Listar Produtos")
    print("4. Nova Venda (Carrinho & Pedido)")
    print("5. Relatórios e Estatísticas")
    print("0. Sair")
    return input("Escolha uma opção: ")

def fluxo_nova_venda() -> None:
    print("\n--- INICIANDO NOVA VENDA ---")
    
    # 1. Identificar o Cliente
    cpf_cliente = input("Digite o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf_cliente)
    if not cliente:
        print("Erro: Cliente não encontrado. Cadastre-o antes.")
        return

    print(f"Cliente identificado: {cliente.nome}")
    
    # 2. Encher o Carrinho
    carrinho = Carrinho()
    while True:
        sku = input("\nDigite o SKU do produto (ou 'fim' para encerrar): ")
        if sku.lower() == 'fim':
            break
        
        produto = buscar_produto_por_sku(sku)
        if not produto:
            print("Produto não encontrado!")
            continue
            
        try:
            qtd_str = input(f"Quantidade de '{produto.nome}': ")
            qtd = int(qtd_str)
            carrinho.adicionar_item(produto, qtd)
            
        except EstoqueInsuficienteErro as e:
            print(f"❌ Erro de Estoque: {e}")
        except ValueError as e:
            print(f"❌ Erro de Valor: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")

    if len(carrinho) == 0:
        print("Carrinho vazio. Venda cancelada.")
        return

    # 3. Fechar Pedido
    try:
        pedido = criar_pedido_do_carrinho(cliente, carrinho)
        print(f"\nPedido #{pedido.id} criado com sucesso!")
        print(f"Subtotal Produtos: R$ {pedido.total_produtos:.2f}")
    except ValueError as e:
        print(f"Erro ao criar pedido: {e}")
        return

    # 4. Calcular Frete
    cep = input("\nDigite o CEP para entrega: ")
    uf = input("Digite a UF (ex: CE, SP): ")
    
    frete_obj = Frete(cep, uf)
    valor_frete = frete_obj.calcular()
    
    pedido.frete = valor_frete
    
    print(f"Frete calculado ({uf}): R$ {valor_frete:.2f} ({frete_obj.prazo} dias)")
    print(f"TOTAL FINAL A PAGAR: R$ {pedido.total_final:.2f}")

    # 5. Pagamento
    confirmar = input("\nDeseja realizar o pagamento agora? (s/n): ")
    if confirmar.lower() == 's':
        tipo = input("Forma de pagamento (PIX, CREDITO, DEBITO, BOLETO): ")
        try:
            pgto = Pagamento(pedido, tipo, pedido.total_final)
            pgto.processar()
            
            # Baixa no estoque
            for item in pedido.itens:
                prod_real = buscar_produto_por_sku(item.sku)
                if prod_real:
                    nova_qtd = prod_real.estoque - item.quantidade
                    atualizar_produto(prod_real.sku, {'estoque': nova_qtd})
            
            print("✅ Estoque atualizado e pagamento confirmado!")
            
        except PagamentoRecusadoErro as e:
            print(f"❌ Pagamento Recusado: {e}")
        except ValueError as e:
            print(f"❌ Erro nos dados: {e}")
    else:
        print("Pedido salvo como 'CRIADO'. Aguardando pagamento futuro.")

def main() -> None:
    while True:
        opcao = menu()
        
        if opcao == '1':
            try:
                criar_cliente(input("CPF: "), input("Nome: "), input("Email: "), input("Endereço: "))
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == '2':
            try:
                sku = input("SKU: ")
                nome = input("Nome: ")
                cat = input("Categoria: ")
                preco = float(input("Preço: "))
                estoque = int(input("Estoque Inicial: "))
                criar_produto(sku, nome, cat, preco, estoque)
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == '3':
            prods = listar_produtos()
            print("\n--- PRODUTOS CADASTRADOS ---")
            for p in prods:
                status = "Ativo" if p.ativo else "Inativo"
                print(f"[{p.sku}] {p.nome} - R$ {p.preco:.2f} ({p.estoque} un) - {status}")

        elif opcao == '4':
            fluxo_nova_venda()

        elif opcao == '5':
            exibir_relatorios()

        elif opcao == '0':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()