from notificacao import Notificacao


class NotificacaoEmail(Notificacao):
    def enviar_notificacao(self, cliente, mensagem):
        print(f"Enviando email para {cliente.nome}: {mensagem}")