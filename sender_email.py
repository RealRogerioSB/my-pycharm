# mais informações: https://mailtrap.io/blog/python-send-email-gmail/
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException

subject = "Teste de envio de E-mail pelo Python"
body = "Esse é o corpo de mensagem de texto."
sender = "rogerioballoussier@gmail.com"
password = "tzdk mqxa ltxe qrha"
recipients = ["rogerioballoussier@gmail.com", "eusourogeriosb@outlook.com", "rogerioballoussier@bb.com.br"]


def send_email(sub, bod, sen, pas, rec):
    msg = MIMEMultipart()
    msg["Subject"] = sub
    msg["From"] = sen
    msg["To"] = ", ".join(rec)
    msg.attach(MIMEText(bod, "plain"))

    with SMTP("smtp.gmail.com", 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(sen, pas)

        try:
            smtp_server.sendmail(sen, rec, msg.as_string())
        except SMTPException as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            print("Email enviado com sucesso!")


send_email(subject, body, sender, password, recipients)
