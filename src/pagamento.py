from pedido import STATUS_PAGO

class Pagamento:
    TIPOS_ACEITOS = ["PIX", "CREDITO", "DEBITO", "BOLETO"]

    def __init__(self, pedido, tipo, valor):
        self.pedido = pedido
        self.tipo = tipo.upper()
        self.valor = valor

    def processar(self):
        """Registra o pagamento e atualiza o status do pedido se o valor for suficiente."""
        
        # 1. Valida o tipo de pagamento
        if self.tipo not in self.TIPOS_ACEITOS:
            raise ValueError(f"Tipo de pagamento inválido. Aceitos: {', '.join(self.TIPOS_ACEITOS)}")

        # 2. Valida o valor (Regra do PDF: total pago >= total pedido)
        if self.valor < self.pedido.total_final:
            raise ValueError(f"Valor insuficiente. Total do pedido é R$ {self.pedido.total_final:.2f}")

        # 3. Confirma o pagamento e muda status do pedido
        self.pedido.status = STATUS_PAGO
        print(f"Pagamento de R$ {self.valor:.2f} confirmado via {self.tipo}!")
        print(f"Pedido #{self.pedido.id} atualizado para: {STATUS_PAGO}")
        return True