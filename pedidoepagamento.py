class Pedido:
    def _init_(self, cliente_nome: str, frete: float):
        # Atributos protegidos (Encapsulamento)
        self._cliente = cliente_nome
        self._frete = frete
        self._itens = []
        self._pagamentos = []
        self._status = StatusPedido.PENDENTE

    @property
    def status(self):
        """Getter para permitir leitura do status, mas não alteração direta."""
        return self._status

    def adicionar_item(self, item: 'ItemPedido'):
        if self._status != StatusPedido.PENDENTE:
            print("❌ Erro: Não é possível alterar pedidos já processados.")
            return
        self._itens.append(item)

    def calcular_total(self) -> float:
        # Soma os subtotais dos itens + frete
        total_produtos = sum(item.subtotal() for item in self._itens)
        return total_produtos + self._frete

    def registrar_pagamento(self, pagamento_obj: 'Pagamento'):
        if self._status == StatusPedido.CANCELADO:
            print("❌ Erro: Pedido cancelado não aceita pagamentos.")
            return

        # Polimorfismo: o pagamento_obj sabe como se processar
        if pagamento_obj.processar():
            self._pagamentos.append(pagamento_obj)
            # AQUI: Usando o atributo interno correto com underline
            self._status = StatusPedido.PAGO
            print(f"✅ Pagamento de R$ {self.calcular_total():.2f} registrado!")