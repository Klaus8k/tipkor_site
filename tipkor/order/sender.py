import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText

import datetime

from loguru import logger

HI = 'Спасибо за заказ.\n\n'

MAIL_HOST = 'smtp.mail.ru'
MAIL_LOGIN = os.getenv('EMAIL_U')
MAIL_PASS = os.getenv('EMAIL_PASS')
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
    client_name = order.client.name
    tel = order.client.tel
    email = order.client.email
    client_str = f'Имя: {client_name}\nТелефон: {tel}\nE-mail: {email}\n'
        
    comment = order.comment
    file = order.file
       
    create_date = order.create_date
    ready_date = order.ready_date
    
    product = get_product_str(order.product, order_id=order.id, dates=[create_date, ready_date])
    
    return HI + product # TODO вставить дату создания и дату готовности


def get_product_str(product: object, order_id, dates: list):
    product_str = ''
    type_production = product['type_production']
    cost = product['cost']
    create_date = dates[0].strftime('%d %B %Y   %H:%M')
    
    if 'paper' in product.keys():
        if product['duplex']:
            duplex = 'Двухсторонняя печать'
        else: duplex = 'Односторонняя печать'
        
        product_str += f"{type_production} \
                            \rНомер заказа № {order_id} от {create_date} \
                            \rФормат: {product['format_p']} \
                            \rБумага: {product['paper']}г/м \
                            \rТираж: {product['pressrun']}шт. \
                            \r{duplex} \
                            \rПостобработка: {product['post_obr']} \
                            \r\rЦена тиража: {cost} руб."
        return product_str
    
    elif 'material' in product.keys():
        
        product_str += f"{type_production} \
                            \rНомер заказа № {order_id} от {create_date} \
                            \rМатериал: {product['material']} \
                            \rРазмер: {product['x']}х{product['x']}м \
                            \rПостобработка: {product['post_obr']} \
                            \r\rЦена тиража: {cost} руб."
        return product_str
    else:
        if product['new_or_no'] == 'new':
            new_or_no = 'Первичное изготовление'
        else: new_or_no = 'Изготовление по оттиску'
        if product['express']:
            express = 'Срочное изготовление'
        else: express = 'Стандартное изготовление'
        
        product_str += f"{type_production} \
                            \rНомер заказа № {order_id} от {create_date} \
                            \r{new_or_no} \
                            \r{express} \
                            \rОснастка: {product['snap']} \
                            \rКоличество: {product['count']}шт. \
                            \r\rЦена тиража: {cost} руб."
        return product_str
    
# {'id': 107, 'new_or_no': 'repeat', 'express': True, 'snap': 'Д40 обычная', 'count': 1, 'cost': 1050, 'type_production': 'Штамп'}






PHONE_SEND = 'PAY SERVICE'
# Платная услуга, когда буду ближе к завершению - протестим. Ссылки для мануала и сервиса рассылок.
# http://python-3.ru/page/send-sms-python
# https://smsc.ru/tariffs/

TELEGRAM_SEND = 'throw tho bot'

WhatsApp_SEND = 'WhatsApp_business_api'


