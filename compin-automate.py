from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from PIL import Image

#RUT sin puntos y con guion
rut = ''
#Folio con guion
folio = ''
#Correo electronico y clave del correo
correo = ''
passwordcorreo = ''
#Lista de destinarios que recibiran el correo
allListCorreos = [""]


driver = webdriver.Firefox()
driver.set_window_size(680, 1150)
driver.get("https://www.milicenciamedica.cl/")
driver.find_element_by_xpath('//*[@id="campo_rut_2"]').send_keys(rut)
driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[4]/form/div[2]/label').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="campo_folio_2"]').send_keys(folio)
time.sleep(2)
driver.find_element_by_xpath('//*[@id="boton_buscar_2"]').click()
time.sleep(10)
driver.save_screenshot("Imagen.png")
driver.close()

im = Image.open('Imagen.png')
rgb_im = im.convert('RGB')
rgb_im.save('Imagen.jpg')


fileToSend = "Imagen.jpg"

for arrayCorreos in  allListCorreos:
    msg = MIMEMultipart()
    message = "Correo generado automaticamente con python"
    password = passwordcorreo
    msg['From'] = correo
    msg['To'] = arrayCorreos
    msg['Subject'] = "Estado licencia compin"

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)

    msg.attach(attachment) 
    msg.attach(MIMEText(message))

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()




