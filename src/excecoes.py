class LojaErro(Exception):
    """Classe base para erros da loja."""
    pass

class EstoqueInsuficienteErro(LojaErro):
    """Levantado quando tenta vender mais do que tem."""
    pass

class PagamentoRecusadoErro(LojaErro):
    """Levantado quando o pagamento falha."""
    pass