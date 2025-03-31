# mais informações: https://mailtrap.io/blog/python-send-email-gmail/
import smtplib
from email.mime.text import MIMEText

subject = "Teste de envio de E-mail"
body = "Esse é o corpo de mensagem de texto."
sender = "rogerioballoussier@icloud.com"
password = "<senha>"
recipients = ["rogerioballoussier@gmail.com", "eusourogeriosb@outlook.com", "rogerioballoussier@bb.com.br"]


def send_email(sub, bod, sen, pas, rec):
    msg = MIMEText(bod)
    msg["Subject"] = sub
    msg["From"] = sen
    msg["To"] = ", ".join(rec)

    with smtplib.SMTP_SSL("smtp.mail.me.com", 587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.login(sen, pas)

        try:
            smtp_server.sendmail(sen, rec, msg.as_string())
        except smtplib.SMTPException as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            print("Email enviado com sucesso!")


send_email(subject, body, sender, password, recipients)
