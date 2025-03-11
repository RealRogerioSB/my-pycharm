from pagamento_pix import PagamentoPIX
from pagamento_cartao import PagamentoCartao


class PagamentoFactory:
    @staticmethod
    def criar_pagamento(tipo):
        if tipo == "pix":
            return PagamentoPIX()
        elif tipo == "cartao":
            return PagamentoCartao()
        else:
            raise ValueError(f"Tipo de pagamento '{tipo}' não suportado")
