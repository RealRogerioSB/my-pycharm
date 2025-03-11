from pedido import Pedido


class PedidoRetirada(Pedido):
    def calcular_total(self):
        return sum(item.preco for item in self.itens)
