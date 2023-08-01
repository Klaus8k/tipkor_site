import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText

MAIL_HOST = 'smtp.mail.ru'
MAIL_LOGIN = os.getenv('EMAIL_U')
MAIL_PASS = os.getenv('EMAIL_PASS')
print(MAIL_PASS)
TO = 'tipkor@mail.ru'
text = 'test message'

# С почтового сервера после аутенитфикации отправляется на почту письм. Пародля для мейла нужен для приложений а не обычный
# Отправка емейла с вложениями и верстой https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development


# Пока в спам улетают письма.
def send_email(adress, order):

    body = get_order_dict(order)
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(f'Заказ №{order.id}', 'utf-8')
    msg['From'] = MAIL_LOGIN
    msg['To'] = adress

    mail_sender = smtplib.SMTP_SSL(MAIL_HOST, 465)
    mail_sender.login(MAIL_LOGIN, MAIL_PASS)
    mail_sender.sendmail(MAIL_LOGIN, adress, msg.as_string())
    mail_sender.quit()

def get_order_dict(order):
    client = order.client.name
    tel = order.client.tel
    email = order.client.email
    product = order.product
    comment = order.comment
    create_date = order.create_date
    ready_date = order.ready_date
    return 'Клиент: {} {} \nЗаказано: {} \nСоздан: {} \nГотовность: {}\n Комментарий:'.format(client, tel, product, create_date, ready_date, comment)
    



PHONE_SEND = 'PAY SERVICE'
# Платная услуга, когда буду ближе к завершению - протестим. Ссылки для мануала и сервиса рассылок.
# http://python-3.ru/page/send-sms-python
# https://smsc.ru/tariffs/

TELEGRAM_SEND = 'throw tho bot'

WhatsApp_SEND = 'WhatsApp_business_api'
