#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_message(data_cntr,iter):
    msg = MIMEMultipart('alternative')
    s = smtplib.SMTP('localhost')

    toEmail = [ "aravind@linuz.in" ]
    fromEmail = "root@linuz.in"
    msg['Subject'] = 'Rollup data for %s'%iter
    msg['From'] = fromEmail
    msg['To'] = ', '.join(toEmail)
    body = '''hai 
    nasdnoad
    asdads	'''
 
    msg.attach(MIMEText(body))
    
    for type in [ "MT", "MA", "SOL"]:
	filename = "/share/data/%s-%s-%s.csv"%(data_cntr, iter, type)
    	f = file(filename)
    	attachment = MIMEText(f.read())
    	attachment.add_header('Content-Disposition', 'attachment', filename=filename.split('/')[4])           
    	msg.attach(attachment)
    
    s.sendmail(fromEmail, toEmail, msg.as_string())

send_message("LA","Week9")
