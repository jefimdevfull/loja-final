import datetime
from dados import ler_dados, salvar_dados, ARQUIVO_PEDIDOS
from cliente import buscar_cliente_por_cpf
from produto import Produto # Apenas para tipagem, se necessário

# Estados do Pedido (conforme PDF)
STATUS_CRIADO = "CRIADO"
STATUS_PAGO = "PAGO"
STATUS_ENVIADO = "ENVIADO"
STATUS_ENTREGUE = "ENTREGUE"
STATUS_CANCELADO = "CANCELADO"

class ItemPedido:
    """Retrato do produto no momento da compra (Preço congelado)."""
    def __init__(self, sku, nome, preco_unitario, quantidade):
        self.sku = sku
        self.nome = nome
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade

    def to_dict(self):
        return {
            "sku": self.sku,
            "nome": self.nome,
            "preco_unitario": self.preco_unitario,
            "quantidade": self.quantidade
        }

class Pedido:
    def __init__(self, id_pedido, cliente, itens, total_produtos, frete=0.0, status=STATUS_CRIADO):
        self.id = id_pedido
        self.cliente = cliente  # Objeto Cliente
        self.itens = itens      # Lista de objetos ItemPedido
        self.total_produtos = total_produtos
        self.frete = frete
        self.status = status
        self.data_criacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def total_final(self):
        return self.total_produtos + self.frete

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_cpf": self.cliente.cpf, # Salvamos apenas o CPF para referenciar
            "itens": [i.to_dict() for i in self.itens],
            "total_produtos": self.total_produtos,
            "frete": self.frete,
            "status": self.status,
            "data_criacao": self.data_criacao
        }

    def __str__(self):
        return f"Pedido #{self.id} | Cliente: {self.cliente.nome} | Status: {self.status} | Total: R$ {self.total_final:.2f}"

# --- Funções do CRUD e Lógica de Pedido ---

def listar_pedidos():
    dados = ler_dados(ARQUIVO_PEDIDOS)
    pedidos = []
    
    for p in dados:
        # Reconstrói o objeto Cliente pelo CPF
        cliente = buscar_cliente_por_cpf(p['cliente_cpf'])
        
        # Reconstrói os itens
        itens_obj = []
        for i in p['itens']:
            itens_obj.append(ItemPedido(i['sku'], i['nome'], i['preco_unitario'], i['quantidade']))
            
        pedido = Pedido(
            id_pedido=p['id'],
            cliente=cliente,
            itens=itens_obj,
            total_produtos=p['total_produtos'],
            frete=p['frete'],
            status=p['status']
        )
        # Força a data original (já que o init pega a data atual)
        pedido.data_criacao = p['data_criacao'] 
        pedidos.append(pedido)
        
    return pedidos

def criar_pedido_do_carrinho(cliente, carrinho):
    """Transforma o Carrinho em um Pedido (snapshot)."""
    if len(carrinho) == 0:
        raise ValueError("O carrinho está vazio.")

    pedidos = listar_pedidos()
    novo_id = len(pedidos) + 1
    
    # Converter ItemCarrinho em ItemPedido (congelando o preço)
    itens_pedido = []
    total_produtos = 0.0
    
    for item_c in carrinho.listar_itens():
        item_p = ItemPedido(
            sku=item_c.produto.sku,
            nome=item_c.produto.nome,
            preco_unitario=item_c.produto.preco, # Preço atual do produto
            quantidade=item_c.quantidade
        )
        itens_pedido.append(item_p)
        total_produtos += item_p.subtotal

    # Cria o objeto Pedido
    # Obs: O frete será calculado depois (conforme regra do PDF)
    novo_pedido = Pedido(novo_id, cliente, itens_pedido, total_produtos)
    
    pedidos.append(novo_pedido)
    salvar_dados(ARQUIVO_PEDIDOS, [p.to_dict() for p in pedidos])
    
    return novo_pedido