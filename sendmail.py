import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def EnviarEmailPlain(dest,asu,msg):
    user = '365monitoreo@gmail.com'
    password = '20101733'

    #Cabeceras del Email
    destinatario = dest
    asunto = asu
    mensaje = msg

    #Host y Puerto SMTP Gmail
    gmail = smtplib.SMTP('smtp.gmail.com', 587)

    #Protocolo Cifrado Gmail
    gmail.starttls()

    #Credenciales
    gmail.login(user,password)

    header = MIMEMultipart()
    header['Subject'] = asunto
    header['From'] = user
    header['To'] = destinatario

    mensaje = MIMEText(mensaje, 'plain')
    header.attach(mensaje)

    #Enviar Email
    gmail.sendmail(user,destinatario,header.as_string())

    #Cerramos Conexion SMTP
    gmail.quit()

def EnviarEmailHTML(dest,asu,msg):
    user = '365monitoreo@gmail.com'
    password = '20101733'

    #Cabeceras del Email
    destinatario = dest
    asunto = asu
    mensaje = msg

    #Host y Puerto SMTP Gmail
    gmail = smtplib.SMTP('smtp.gmail.com', 587)

    #Protocolo Cifrado Gmail
    gmail.starttls()

    #Credenciales
    gmail.login(user,password)

    header = MIMEMultipart()
    header['Subject'] = asunto
    header['From'] = user
    header['To'] = destinatario

    mensaje = MIMEText(mensaje, 'html')
    header.attach(mensaje)

    #Enviar Email
    gmail.sendmail(user,destinatario,header.as_string())

    #Cerramos Conexion SMTP
    gmail.quit()    
