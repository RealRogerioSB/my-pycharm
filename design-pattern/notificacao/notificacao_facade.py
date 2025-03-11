from notificacao_email import NotificacaoEmail
from notificacao_sms import NotificacaoSMS


class NotificacaoFacade:
    def __init__(self):
        self.notificacoes = [NotificacaoEmail(), NotificacaoSMS()]

    def enviar_notificacoes(self, cliente, mensagem):
        for notificacao in self.notificacoes:
            notificacao.enviar_notificacao(cliente, mensagem)
