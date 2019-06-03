import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from home.apps.config.mail import *


def send_mail(email="", author="", name="", confirm=False, contact=False, code="", phone="", time_from="", time_to="", question="", recover_link="", unrecover_link=""):
    if confirm:
        msg = MIMEMultipart()
        msg['From'] = email_confirm
        msg['To'] = email
        msg['Subject'] = "Восстановление пароля Alpha Home"
        body = "Код подтверждения: <b>" + str(code) + "</b>. Или используйте ссылку " + recover_link + "<br>Код истекает через 24 " \
                                                                                 "часа.<br><br><br>Это сообщение было " \
                                                                                 "сгенерировано автоматически. На " \
                                                                                 "него не нужно отвечать. Это не вы? <br><br><br>" + unrecover_link + " ."
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP('smtp.yandex.com', 587)
        server.starttls()
        server.login(email_confirm, password)
        text = msg.as_string()
        server.sendmail(email_confirm, email, text)
        server.quit()
    elif contact:
        msg = MIMEMultipart()
        msg['From'] = email_contact
        msg['To'] = email_contact
        msg['Subject'] = "Просьба Позвонить " + name
        body = 'Прошу перезвонить.\nСвязаться по телефону: ' + phone + ". С " + str(time_from) + " до " + str(time_to) +  ". Имя пользователя в системе: \'" + author + "\'."
        msg.attach(MIMEText(body, 'text'))
        server = smtplib.SMTP('smtp.yandex.com', 587)
        server.starttls()
        server.login(email_contact, password)
        text = msg.as_string()
        server.sendmail(email_contact, email_contact, text)
        server.quit()
    else:
        msg = MIMEMultipart()
        msg['From'] = email_support
        msg['To'] = email_support
        msg['Subject'] = "Обращение от " + name
        body = '\nВопрос:\n---\n' + question + '\n---\nСвязаться по: ' + email + ". Имя пользователя в системе: \'" + author + "\'."
        msg.attach(MIMEText(body, 'text'))
        server = smtplib.SMTP('smtp.yandex.com', 587)
        server.starttls()
        server.login(email_support, password)
        text = msg.as_string()
        server.sendmail(email_support, email_support, text)
        server.quit()


if __name__ == '__main__':
    send_mail(email="sevavov.2004@gmail.com", confirm=True, code="2281337")