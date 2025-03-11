from notificacao import Notificacao


class NotificacaoSMS(Notificacao):
    def enviar_notificacao(self, cliente, mensagem):
        print(f"Enviando sms para {cliente.nome}: {mensagem}")
