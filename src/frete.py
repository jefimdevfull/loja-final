import json
import os
from typing import Dict, Any

class Frete:
    """Calcula frete lendo a tabela do arquivo settings.json."""
    
    def __init__(self, cep: str, uf: str):
        self.cep = cep
        self.uf = uf.upper()
        self.valor: float = 0.0
        self.prazo: int = 0
        self._carregar_configuracoes()

    def _carregar_configuracoes(self) -> None:
        """Carrega tabela de fretes e valores padrão do arquivo JSON."""
        caminho = "settings.json"
        
        # Valores padrão de segurança
        self.tabela_frete: Dict[str, Any] = {}
        self.frete_padrao: Dict[str, Any] = {"preco": 60.00, "prazo": 15}

        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    # Navega no JSON para buscar frete -> tabela
                    frete_config = config.get("frete", {})
                    self.tabela_frete = frete_config.get("tabela", {})
                    self.frete_padrao = frete_config.get("padrao", self.frete_padrao)
            except Exception as e:
                print(f"Aviso: Erro ao ler settings.json ({e}). Usando padrão.")
        else:
            # Opcional: Avisar que não achou o arquivo
            pass

    def calcular(self) -> float:
        """
        Define o valor e o prazo com base na UF.
        Retorna o valor do frete.
        """
        # Busca a UF na tabela; se não achar, usa o padrão
        dados = self.tabela_frete.get(self.uf, self.frete_padrao)
        
        self.valor = float(dados["preco"])
        self.prazo = int(dados["prazo"])
        return self.valor

    def __str__(self) -> str:
        return f"Frete para {self.uf}: R$ {self.valor:.2f} ({self.prazo} dias úteis)"