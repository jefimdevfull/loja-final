from dados import ler_dados, salvar_dados, ARQUIVO_PRODUTOS

class Produto:
    def __init__(self, sku, nome, categoria, preco, estoque, ativo=True):
        self.sku = sku
        self.nome = nome
        self.categoria = categoria
        self._preco = 0
        self.preco = preco  # Setter valida se é > 0
        self._estoque = 0
        self.estoque = estoque # Setter valida se é >= 0
        self.ativo = ativo

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, valor):
        if valor <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        self._preco = valor

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, valor):
        if valor < 0:
            raise ValueError("O estoque não pode ser negativo.")
        self._estoque = valor

    def to_dict(self):
        return {
            "sku": self.sku,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "estoque": self.estoque,
            "ativo": self.ativo
        }

    # Métodos Mágicos exigidos no PDF
    def __str__(self):
        return f"{self.nome} (SKU: {self.sku}) - R$ {self.preco:.2f} [{self.estoque} un]"

    def __eq__(self, other):
        if isinstance(other, Produto):
            return self.sku == other.sku
        return False
    
    def __lt__(self, other):
        return self.preco < other.preco

# --- Funções do CRUD ---

def listar_produtos():
    """Lê o JSON e retorna uma lista de OBJETOS Produto."""
    dados_brutos = ler_dados(ARQUIVO_PRODUTOS)
    lista_produtos = []
    
    for item in dados_brutos:
        p = Produto(
            sku=item['sku'],
            nome=item['nome'],
            categoria=item['categoria'],
            preco=item['preco'],
            estoque=item['estoque'],
            ativo=item.get('ativo', True)
        )
        lista_produtos.append(p)
        
    return lista_produtos

def criar_produto(sku, nome, categoria, preco, estoque):
    """Cria um produto novo e salva no JSON."""
    produtos = listar_produtos()
    
    if any(p.sku == sku for p in produtos):
        raise ValueError(f"Já existe um produto com o SKU {sku}.")

    novo = Produto(sku, nome, categoria, preco, estoque)
    produtos.append(novo)
    
    salvar_dados(ARQUIVO_PRODUTOS, [p.to_dict() for p in produtos])
    print(f"Produto '{nome}' cadastrado com sucesso!")

def atualizar_produto(sku, novos_dados):
    """Atualiza dados de um produto existente."""
    produtos = listar_produtos()
    produto_encontrado = None
    
    for p in produtos:
        if p.sku == sku:
            produto_encontrado = p
            break
            
    if not produto_encontrado:
        raise ValueError("Produto não encontrado.")
        
    if 'nome' in novos_dados: produto_encontrado.nome = novos_dados['nome']
    if 'categoria' in novos_dados: produto_encontrado.categoria = novos_dados['categoria']
    if 'preco' in novos_dados: produto_encontrado.preco = novos_dados['preco']
    if 'estoque' in novos_dados: produto_encontrado.estoque = novos_dados['estoque']
    if 'ativo' in novos_dados: produto_encontrado.ativo = novos_dados['ativo']

    salvar_dados(ARQUIVO_PRODUTOS, [p.to_dict() for p in produtos])

def deletar_produto(sku):
    """Desativa um produto (Exclusão Lógica)."""
    atualizar_produto(sku, {'ativo': False})
    print(f"Produto {sku} desativado com sucesso.")

def buscar_produto_por_sku(sku):
    """Busca um produto pelo SKU e retorna o Objeto Produto."""
    produtos = listar_produtos()
    for p in produtos:
        if p.sku == sku:
            return p
    return None