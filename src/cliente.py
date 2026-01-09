from dados import ler_dados, salvar_dados, ARQUIVO_CLIENTES

class Cliente:
    def __init__(self, cpf, nome, email, endereco):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.endereco = endereco # Pode ser string ou dicionário (CEP, Cidade, UF)

    def to_dict(self):
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "email": self.email,
            "endereco": self.endereco
        }

    # Métodos Mágicos exigidos no PDF (comparação por CPF/Email)
    def __eq__(self, other):
        if isinstance(other, Cliente):
            return self.cpf == other.cpf or self.email == other.email
        return False

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf}) - {self.email}"

# --- Funções do CRUD ---

def listar_clientes():
    """Lê o JSON e retorna uma lista de OBJETOS Cliente."""
    dados_brutos = ler_dados(ARQUIVO_CLIENTES)
    lista_clientes = []
    
    for item in dados_brutos:
        c = Cliente(
            cpf=item['cpf'],
            nome=item['nome'],
            email=item['email'],
            endereco=item['endereco']
        )
        lista_clientes.append(c)
    return lista_clientes

def criar_cliente(cpf, nome, email, endereco):
    """Cria um cliente novo, validando duplicidade de CPF e Email."""
    clientes = listar_clientes()
    
    # Validação de duplicidade exigida no PDF
    for c in clientes:
        if c.cpf == cpf:
            raise ValueError(f"Já existe um cliente com o CPF {cpf}.")
        if c.email == email:
            raise ValueError(f"Já existe um cliente com o email {email}.")

    novo = Cliente(cpf, nome, email, endereco)
    clientes.append(novo)
    
    salvar_dados(ARQUIVO_CLIENTES, [c.to_dict() for c in clientes])
    print(f"Cliente '{nome}' cadastrado com sucesso!")

def buscar_cliente_por_cpf(cpf):
    """Função utilitária para vendas."""
    clientes = listar_clientes()
    for c in clientes:
        if c.cpf == cpf:
            return c
    return None