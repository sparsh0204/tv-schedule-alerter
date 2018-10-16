import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sub,msg,emailto):
    ''' function to form a connection and send a mail '''
    try:
        server = smtplib.SMTP('smtp.gmail.com' , 587)
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL, config.PASSWORD)
        # message = 'Subject: {}\n\n{}'.format(sub,msg)
        server.sendmail(config.EMAIL, emailto, msg.as_string())
        server.quit()
        print('Mail sent')
    except:
        pass
