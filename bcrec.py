import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from bs4 import BeautifulSoup
import requests
import os.path
from datetime import datetime

i = datetime.now()

#Email Credentials
fromaddr = "xxxx@gmail.com"  #Sender Email Address
toaddr = "yyyyyy@gmail.com"  #Receiver Email Address
sendpass = "zzzzzzzzzzzzzz" #Sender Email Account Password

url = 'http://bcrec.ac.in/'
resp = requests.get(url+'noticeboard.htm')
txt = resp.text
soup = BeautifulSoup(txt, 'lxml')
data = soup.find_all('table')[4]
tags = data.find_all('a')
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr

def attach(url, pdffile):
    print("Downloading Latest Notice File...")
    r = requests.get(url+pdffile, stream = True)
    with open(pdffile,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)


def checknotice():
    print('Notice Data Found!')

    fr = open('bcrecnotice', 'r')
    for lines in fr:
        pass
    last = lines
    fr.close()

    f = open('bcrecnotice', 'a+')

    for t in tags:
        line = ' '.join(t.text.split())
        pdffile= t.attrs['href']
        latest = line + ' >>>>> '+ url+pdffile

    msg['Subject'] = 'New Notice at BCREC >> '+line

    body = '''For details check this Notice '''+url+pdffile+" or download attachement from below."

    if (last == latest):
        pass
    else:
        attach(url, pdffile)

        msg.attach(MIMEText(body, 'plain'))

        filename = pdffile
        attachment = open(pdffile, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, sendpass)
    text = msg.as_string()
    print("Last Stored Notice: "+last)
    print("Latest Notice: "+latest)

    if (last == latest):
        print("No New Notice Found!")
    else:
        f.write('\n'+latest)
        print('Sending Email with Attachment...')
        server.sendmail(fromaddr, toaddr, text)
        print("Mail Sent!")
        print(latest)
    f.close()
    server.quit()


def downloadnotice():
    print('No Notice Found!')
    print('Downloading All Notices...')

    body = "List of all Notices: "

    f = open('bcrecnotice', 'a+')

    for t in tags:
        line = ' '.join(t.text.split())
        pdffile= t.attrs['href']
        latest = '\n'+line + ' >>>>> '+ url+pdffile
        f.write(latest)
        body = body+latest

    msg['Subject'] = 'All Notices at BCREC till %s/%s/%s' % (i.day, i.month, i.year)

    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, sendpass)
    text = msg.as_string()
    print('Sending Email...')
    server.sendmail(fromaddr, toaddr, text)
    print("Mail Sent!")
    print('Last Notice Added: '+latest)
    f.close()
    server.quit()


if(os.path.exists('bcrecnotice')):
    checknotice()
else:
    downloadnotice()
