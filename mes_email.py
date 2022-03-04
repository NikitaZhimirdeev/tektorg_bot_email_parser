#https://www.google.com/settings/security/lesssecureapps
import settings
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#
def get_email(filename):
    # Объявляем елемент сообщения
    msg = MIMEMultipart()

    msg['From'] = settings.msg_From    # Адрес отправителя
    password = settings.password # Пароль
    msg['To'] = settings.msg_To # Адрес получателя
    msg['Subject'] = "Сводка по закупкам РН"    # Тема сообщения
    msg_text = 'Сводка по закупкам РН'  # Текст Сообщения
    # Прикрепляем текст к сообщению
    msg.attach(MIMEText(msg_text, 'plain'))
    # Объявляем общий тип сообщения
    ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    # Открываем файл в байтовом виде
    with open(filename, 'rb') as fp:
        file = MIMEBase(maintype, subtype)
        file.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(file)
    # Добавляем файл в сообщение
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)
    # Объявляем элемент сервера
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Запускаемсервер
    server.starttls()
    # Входим в аккаунт отправителя
    server.login(msg['From'], password)
    # Отправляем сообщение
    server.send_message(msg)
    # Закрываем соединение с сервером
    server.quit()
