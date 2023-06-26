import os
import smtplib

MAIL_HOST = 'smtp.mail.ru'
MAIL_LOGIN = os.getenv('EMAIL_U')
MAIL_PASS = os.getenv('EMAIL_PASS')
print(MAIL_PASS)
TO = 'tipkor@mail.ru'
text = 'test message'


# mail_sender = smtplib.SMTP_SSL(MAIL_HOST, 465)
# print(mail_sender.ehlo())
# mail_sender.login(MAIL_LOGIN, MAIL_PASS)
# mail_sender.sendmail(MAIL_LOGIN, TO, text)
# mail_sender.quit()

# С почтового сервера после аутенитфикации отправляется на почту письм. Пародля для мейла нужен для приложений а не обычный
# Отправка емейла с вложениями и верстой https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development



def send_email(adress, subject):
    mail_sender = smtplib.SMTP_SSL(MAIL_HOST, 465)
    print(mail_sender.ehlo())
    mail_sender.login(MAIL_LOGIN, MAIL_PASS)
    mail_sender.sendmail(MAIL_LOGIN, TO, subject)
    mail_sender.quit()





PHONE_SEND = 'PAY SERVICE'
# Платная услуга, когда буду ближе к завершению - протестим. Ссылки для мануала и сервиса рассылок.
# http://python-3.ru/page/send-sms-python
# https://smsc.ru/tariffs/

TELEGRAM_SEND = 'throw tho bot'

WhatsApp_SEND = 'WhatsApp_business_api'
