from pedido import Pedido


class PedidoDelivery(Pedido):
    def __init__(self, cliente, itens, taxa_entrega):
        super().__init__(cliente, itens)
        self.taxa_entrega = taxa_entrega

    def calcular_total(self):
        total = sum(item.preco for item in self.itens) + self.taxa_entrega
        return total
