from produto import Produto

class ItemCarrinho:
    """Representa um item dentro do carrinho (Produto + Quantidade)."""
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade

    @property
    def subtotal(self):
        """Calcula o preço x quantidade deste item."""
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f"{self.produto.nome} | Qtd: {self.quantidade} | Sub: R$ {self.subtotal:.2f}"

class Carrinho:
    def __init__(self):
        self._itens = [] # Lista de objetos ItemCarrinho

    def adicionar_item(self, produto: Produto, quantidade: int):
        """Adiciona item ou atualiza quantidade se já existir."""
        
        # Validação básica de estoque antes de adicionar (opcional, mas recomendado)
        if quantidade > produto.estoque:
            raise ValueError(f"Estoque insuficiente. Disponível: {produto.estoque}")
        
        # Verifica se o produto já está no carrinho
        for item in self._itens:
            if item.produto.sku == produto.sku:
                item.quantidade += quantidade
                # Nova validação após somar
                if item.quantidade > produto.estoque:
                    item.quantidade -= quantidade # Desfaz
                    raise ValueError("A quantidade total excede o estoque disponível.")
                return

        # Se não existe, cria novo item
        novo_item = ItemCarrinho(produto, quantidade)
        self._itens.append(novo_item)
        print(f"Adicionado: {produto.nome} (x{quantidade})")

    def remover_item(self, sku_produto):
        """Remove um item do carrinho pelo SKU."""
        # Filtra a lista mantendo apenas os itens que NÃO são o SKU removido
        self._itens = [item for item in self._itens if item.produto.sku != sku_produto]

    def calcular_total(self):
        """Soma o subtotal de todos os itens."""
        return sum(item.subtotal for item in self._itens)

    def limpar(self):
        self._itens = []

    def listar_itens(self):
        return self._itens

    # Método Mágico __len__ exigido no PDF
    def __len__(self):
        """Retorna a quantidade total de itens (produtos distintos) no carrinho."""
        return len(self._itens)