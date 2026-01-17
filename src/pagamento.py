from pedido import Pedido, STATUS_PAGO
from excecoes import PagamentoRecusadoErro

class Pagamento:
    """Processa o pagamento de um pedido."""
    
    TIPOS_ACEITOS = ["PIX", "CREDITO", "DEBITO", "BOLETO"]

    def __init__(self, pedido: Pedido, tipo: str, valor: float):
        self.pedido = pedido
        self.tipo = tipo.upper()
        self.valor = valor

    def processar(self) -> bool:
        """
        Valida e confirma o pagamento.
        Lança PagamentoRecusadoErro se houver problemas.
        """
        
        # 1. Valida o tipo de pagamento
        if self.tipo not in self.TIPOS_ACEITOS:
            raise PagamentoRecusadoErro(
                f"Tipo de pagamento '{self.tipo}' inválido. "
                f"Aceitos: {', '.join(self.TIPOS_ACEITOS)}"
            )

        # 2. Valida o valor (Regra: Valor pago >= Total do Pedido)
        # Usamos uma pequena margem de erro para float (0.01)
        if self.valor < (self.pedido.total_final - 0.01):
            faltam = self.pedido.total_final - self.valor
            raise PagamentoRecusadoErro(
                f"Valor insuficiente. Total: R$ {self.pedido.total_final:.2f}. "
                f"Faltam: R$ {faltam:.2f}"
            )

        # 3. Confirma o pagamento e muda status do pedido
        self.pedido.status = STATUS_PAGO
        print(f"Pagamento de R$ {self.valor:.2f} confirmado via {self.tipo}!")
        print(f"Status do Pedido #{self.pedido.id} alterado para: {STATUS_PAGO}")
        return True