import os
import smtplib

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
    print(get_order_dict(order)) # Print to stdIO
    # mail_sender = smtplib.SMTP_SSL(MAIL_HOST, 465)
    # mail_sender.login(MAIL_LOGIN, MAIL_PASS)
    # text = get_order_dict(order).encode('utf-8')
    # mail_sender.sendmail(MAIL_LOGIN, adress, text)
    # mail_sender.quit()

def get_order_dict(order):
    client = order.client.name
    tel = order.client.tel
    email = order.client.email
    product = order.product
    create_date = order.create_date
    ready_date = order.ready_date
    return 'Клиент: {} {} {} \nЗаказано: {} \nСоздан: {} /nГотовность: {}'.format(client, tel, email, product, create_date, ready_date)
    



PHONE_SEND = 'PAY SERVICE'
# Платная услуга, когда буду ближе к завершению - протестим. Ссылки для мануала и сервиса рассылок.
# http://python-3.ru/page/send-sms-python
# https://smsc.ru/tariffs/

TELEGRAM_SEND = 'throw tho bot'

WhatsApp_SEND = 'WhatsApp_business_api'
