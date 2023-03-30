import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from typing import Union


def sendMail(whereto: Union[list, str], from_user: str, from_email: str, 
             subject: str, body: str, server="localhost", 
             ishtml=bool):
    msg = MIMEMultipart('alternative')

    if ishtml:
        stp = 'html'
    else:
        stp = 'plain'

    if isinstance(whereto, str):
        whereto = [whereto]
    
    msg['from'] = f'{from_user} <{from_email}>'
    msg['To'] = COMMASPACE.join(whereto)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, stp))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(from_user, whereto, msg.as_string())
    smtp.close()

# Example:
sendMail(whereto='lyteloli <yasha.reg@icloud.com>', from_user='lyteloli', 
         from_email='test@veratag.ru', subject='Kinda subject',
         body='<h1>Hello, <span style=\'color: cyan;\'>it works</span>!</h1>')
print("SENT")
