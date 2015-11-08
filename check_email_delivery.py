#!/usr/bin/python
#
# Script can be used for testing mail flow
# Sends a test mail with random string as subject
# Using IMAP identifies mail has been dellivered
#

import sys
import smtplib
import random
import string
import imaplib
import time
from optparse import OptionGroup
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-d', '--debug', action='store_true', 
		default=False)
parser.add_option('-w', '--wait', action='store', 
		dest = 'wait', type = 'int',
		help = 'Time to wait between send and recieve')
parser.add_option('-f', '--from', action='store', 
		dest = 'from_addr',
		help = 'Email from address')
parser.add_option('-t', '--to', action='store', 
		dest = 'to_addr',
		help = 'Email to address')

group = OptionGroup(parser, "SMTP Options")

group.add_option('--smtphost', action = 'store', 
		dest = 'smtphost',
		help = 'SMTP Server')
group.add_option('--smtpport', action = 'store', 
		dest = 'smtpport', type = 'int',
		help = 'SMTP Port', default = '25')		
group.add_option('--smtpuser', action = 'store', 
		dest = 'smtpuser', 
		help = 'SMTP Username')
group.add_option('--smtppass', action = 'store', 
		dest = 'smtppass',
		help = 'SMTP Password')

parser.add_option_group(group)

group = OptionGroup(parser, "IMAP Options")

group.add_option('--imaphost', action = 'store', 
		dest = 'imaphost',
		help = 'IMAP Server')
group.add_option('--imapport', action = 'store', 
		dest = 'imapport', type = 'int',
		help = 'IMAP Port', default = '143')
group.add_option('--imapuser', action = 'store', 
		dest = 'imapuser',
		help = 'IMAP Username')
group.add_option('--imappass', action = 'store', 
		dest = 'imappass',
		help = 'IMAP Password')
group.add_option('--imapdelete', action='store_true', 
		default=False,
		help = 'Delete mail from mailbox')

parser.add_option_group(group)

(options, args) = parser.parse_args()

subj = ''.join([random.choice(string.ascii_letters + string.digits)\
						 for n in xrange(32)])

msg = '''\
From: <%(from)s>
To: <%(to)s>
Subject: %(subj)s

This is a test mail

'''

if not options.to_addr:
    print "Critical: Please provide to address"
    sys.exit()
elif not options.from_addr:
    print "Critical: Please provide from address"
    sys.exit()

def send():
    try:
        s = smtplib.SMTP(options.smtphost,options.smtpport)
	if options.debug:
            s.set_debuglevel(1)
	if options.smtpuser and options.smtppass:
	    s.login(auth_user,auth_pw)
        s.sendmail( options.from_addr, options.to_addr,  msg % \
		{'from': options.from_addr, 'to': options.to_addr, 'subj': subj})
        s.close()
    except smtplib.socket.error as e:
	print "Critical: SMTP",options.smtphost,e.args[1]
	sys.exit()

send()

time.sleep(options.wait)

def recv():
    try:
        m = imaplib.IMAP4(options.imaphost,options.imapport)
        if options.debug:
	    m.debug = 4
        m.login(options.imapuser, options.imappass)
        m.select()
        typ, data = m.search(None, '(SUBJECT %s)'%subj)
	if data[0]:
	    print "OK: Mail delivered"
	    if options.imapdelete:
 	        m.store(data[0], '+FLAGS', '\\Deleted')
	        m.expunge()
	else:
	    print "Critical: Mail not delivered"
        m.close()
        m.logout()
    except imaplib.socket.error as e:
	print "Critical: IMAP ",options.imaphost,e.args[1]

recv()
