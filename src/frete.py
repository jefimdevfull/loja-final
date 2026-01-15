import json
import os

class Frete:
    def __init__(self, cep, uf):
        self.cep = cep
        self.uf = uf.upper()
        self.valor = 0.0
        self.prazo = 0
        self._carregar_configuracoes()

    def _carregar_configuracoes(self):
        caminho = "settings.json"
        
        # Valores de segurança
        self.tabela_frete = {}
        self.frete_padrao = {"preco": 60.00, "prazo": 15}

        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.tabela_frete = config.get("frete", {}).get("tabela", {})
                    self.frete_padrao = config.get("frete", {}).get("padrao", self.frete_padrao)
            except Exception:
                pass # Usa o padrão se der erro

    def calcular(self):
        dados = self.tabela_frete.get(self.uf, self.frete_padrao)
        self.valor = dados["preco"]
        self.prazo = dados["prazo"]
        return self.valor