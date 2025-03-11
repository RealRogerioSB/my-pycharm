from abc import ABC, abstractmethod


class Notificacao(ABC):
    @abstractmethod
    def enviar_notificacao(self, cliente, mensagem):
        pass
