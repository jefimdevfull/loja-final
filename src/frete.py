class Frete:
    """Classe responsável por calcular preço e prazo de entrega."""
    
    # Tabela simples de preços por Estado (Simulação)
    TABELA_FRETE = {
        "CE": {"preco": 15.00, "prazo": 3},  # Ceará (Local)
        "PE": {"preco": 20.00, "prazo": 5},  # Pernambuco
        "SP": {"preco": 45.00, "prazo": 10}, # São Paulo
        "RJ": {"preco": 45.00, "prazo": 10}, # Rio de Janeiro
        "PADRAO": {"preco": 60.00, "prazo": 15} # Outros
    }

    def __init__(self, cep, uf):
        self.cep = cep
        self.uf = uf.upper()
        self.valor = 0.0
        self.prazo = 0

    def calcular(self):
        """Define o valor e o prazo com base na UF."""
        dados = self.TABELA_FRETE.get(self.uf, self.TABELA_FRETE["PADRAO"])
        self.valor = dados["preco"]
        self.prazo = dados["prazo"]
        return self.valor

    def __str__(self):
        return f"Frete para {self.uf}: R$ {self.valor:.2f} ({self.prazo} dias úteis)"