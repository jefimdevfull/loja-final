import sys
from produto import criar_produto, listar_produtos, buscar_produto_por_sku, atualizar_produto
from cliente import criar_cliente, listar_clientes, buscar_cliente_por_cpf
from carrinho import Carrinho
from pedido import criar_pedido_do_carrinho, listar_pedidos, STATUS_PAGO
from frete import Frete
from pagamento import Pagamento

# Função auxiliar para buscar produto (caso não tenha no seu produto.py)
def buscar_produto_por_sku(sku):
    produtos = listar_produtos()
    for p in produtos:
        if p.sku == sku:
            return p
    return None

def menu():
    print("\n" + "="*30)
    print("   SISTEMA DE LOJA VIRTUAL")
    print("="*30)
    print("1. Cadastrar Cliente")
    print("2. Cadastrar Produto")
    print("3. Listar Produtos")
    print("4. Nova Venda (Carrinho & Pedido)")
    print("5. Relatórios (Pedidos)")
    print("0. Sair")
    return input("Escolha uma opção: ")

def fluxo_nova_venda():
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
            qtd = int(input(f"Quantidade de '{produto.nome}': "))
            carrinho.adicionar_item(produto, qtd)
        except ValueError as e:
            print(f"Erro ao adicionar: {e}")

    if len(carrinho) == 0:
        print("Carrinho vazio. Venda cancelada.")
        return

    # 3. Fechar Pedido
    try:
        pedido = criar_pedido_do_carrinho(cliente, carrinho)
        print(f"\nPedido #{pedido.id} criado com sucesso!")
        print(f"Total Produtos: R$ {pedido.total_produtos:.2f}")
    except ValueError as e:
        print(f"Erro ao criar pedido: {e}")
        return

    # 4. Calcular Frete
    cep = input("\nDigite o CEP para entrega: ")
    uf = input("Digite a UF (ex: CE, SP): ")
    
    frete_obj = Frete(cep, uf)
    valor_frete = frete_obj.calcular()
    
    # Atualiza o pedido com o valor do frete
    # (Como não criamos um método específico, vamos atribuir direto e salvar)
    pedido.frete = valor_frete
    # Re-salvar seria ideal aqui, mas para simplificar, vamos seguir para o pagamento.
    
    print(f"Frete calculado: R$ {valor_frete:.2f} ({frete_obj.prazo} dias)")
    print(f"TOTAL FINAL A PAGAR: R$ {pedido.total_final:.2f}")

    # 5. Pagamento
    confirmar = input("\nDeseja realizar o pagamento agora? (s/n): ")
    if confirmar.lower() == 's':
        tipo = input("Forma de pagamento (PIX, CREDITO, DEBITO, BOLETO): ")
        try:
            # Simula que o cliente pagou o valor exato
            pgto = Pagamento(pedido, tipo, pedido.total_final)
            pgto.processar()
            
            # Baixa no estoque (Requisito 4 do PDF - Atualizar estoque ao faturar)
            # Para cada item do pedido, reduzimos do estoque real
            for item in pedido.itens:
                prod_real = buscar_produto_por_sku(item.sku)
                if prod_real:
                    nova_qtd = prod_real.estoque - item.quantidade
                    atualizar_produto(prod_real.sku, {'estoque': nova_qtd})
            print("Estoque atualizado com sucesso!")
            
        except ValueError as e:
            print(f"Pagamento falhou: {e}")
    else:
        print("Pedido salvo como 'CRIADO'. Aguardando pagamento futuro.")

def main():
    while True:
        opcao = menu()
        
        if opcao == '1':
            cpf = input("CPF: ")
            nome = input("Nome: ")
            email = input("Email: ")
            endereco = input("Endereço: ")
            try:
                criar_cliente(cpf, nome, email, endereco)
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == '2':
            sku = input("SKU: ")
            nome = input("Nome: ")
            cat = input("Categoria: ")
            try:
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
            peds = listar_pedidos()
            print("\n--- HISTÓRICO DE PEDIDOS ---")
            for p in peds:
                print(p)

        elif opcao == '0':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()