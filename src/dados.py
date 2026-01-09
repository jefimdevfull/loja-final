import json
import os

# Nomes dos arquivos onde os dados serão salvos
ARQUIVO_PRODUTOS = "produtos.json"
ARQUIVO_CLIENTES = "clientes.json"
ARQUIVO_PEDIDOS = "pedidos.json"

def ler_dados(nome_arquivo):
    """Lê os dados de um arquivo JSON. Retorna uma lista vazia se o arquivo não existir."""
    if not os.path.exists(nome_arquivo):
        return []
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

def salvar_dados(nome_arquivo, dados):
    """Salva uma lista de dados em um arquivo JSON."""
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)