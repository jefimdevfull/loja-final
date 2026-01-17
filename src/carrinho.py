from typing import List
from produto import Produto
from excecoes import EstoqueInsuficienteErro

class ItemCarrinho:
    """Representa um item dentro do carrinho (Produto + Quantidade)."""
    
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade

    @property
    def total(self) -> float:
        """Calcula o subtotal deste item (preço x quantidade)."""
        return self.produto.preco * self.quantidade

class Carrinho:
    """Gerencia a lista de produtos que o cliente quer comprar."""
    
    def __init__(self):
        self.itens: List[ItemCarrinho] = []

    def adicionar_item(self, produto: Produto, quantidade: int):
        """
        Adiciona um produto ao carrinho.
        Lança EstoqueInsuficienteErro se não houver disponibilidade.
        """
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        # Validação de Estoque (Requisito Crítico)
        if produto.estoque < quantidade:
            raise EstoqueInsuficienteErro(
                f"Estoque insuficiente para '{produto.nome}'. "
                f"Disponível: {produto.estoque}, Solicitado: {quantidade}"
            )

        # Verifica se o item já existe no carrinho para somar a quantidade
        for item in self.itens:
            if item.produto.sku == produto.sku:
                novo_total = item.quantidade + quantidade
                if produto.estoque < novo_total:
                    raise EstoqueInsuficienteErro(
                        f"Estoque insuficiente ao somar. Máximo: {produto.estoque}"
                    )
                item.quantidade = novo_total
                print(f"Quantidade de '{produto.nome}' atualizada para {item.quantidade}.")
                return

        # Se não existe, cria novo item
        novo_item = ItemCarrinho(produto, quantidade)
        self.itens.append(novo_item)
        print(f"'{produto.nome}' adicionado ao carrinho!")

    def remover_item(self, sku: str):
        """Remove um item do carrinho pelo SKU."""
        self.itens = [item for item in self.itens if item.produto.sku != sku]

    @property
    def total(self) -> float:
        """Soma o valor de todos os itens no carrinho."""
        return sum(item.total for item in self.itens)

    def __len__(self) -> int:
        return len(self.itens)