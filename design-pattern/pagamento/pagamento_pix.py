from pagamento import Pagamento


class PagamentoPIX(Pagamento):
    def processar(self, valor):
        print(f"Processando pagamento de R$ {valor:.2f} via PIX.")
