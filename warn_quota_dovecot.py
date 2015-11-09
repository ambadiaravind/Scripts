#!/usr/bin/python

import sys
import smtplib
import ldap
import os

server='127.0.0.1'
domain='linuz.in'
postmaster='mailadmin@linuz.in'
auth_user='mailadmin'
auth_pw='********'

warn_msg = '''\
From: Mailadministrator <mailadmin@%(domain)s>
To: %(mailbox)s <%(mailbox)s@%(domain)s>
Subject: WARNING! You are nearing the end of your usage limit
Dear %(mailbox)s,

You are using %(usage)d%% of your available quota. You are advised to
free up some space in your mailbox to avoid mails coming to you from
getting bounced.

Mailadministrator
'''

def warn(mailbox, usage, domain):
    s = smtplib.SMTP(server)
    s.login(auth_user,auth_pw)
    s.set_debuglevel(1)
    # List of mail id's to which email needs to be send, by default admin
    # and user will get the mail
    tolist=["aravind@linuz.in",'%s@%s' %(mailbox,domain)]
    s.sendmail(postmaster, tolist, warn_msg % {'mailbox': mailbox,'usage': usage,'domain':domain})
    s.close()

a = 1
try:
    while a>=0:
        l = ldap.initialize('ldap://localhost:389')
        mailbox = l.search_s('ou=People,dc=linuz,dc=in',ldap.SCOPE_SUBTREE,'(objectClass=*)'['mail'])[a][1]['mail'][0].split('@')[0]
        domain = l.search_s('ou=People,dc=linuz,dc=in',ldap.SCOPE_SUBTREE,'(objectClass=*)',['mail'])[a][1]['mail'][0].split('@')[1]
        file = os.path.exists('/home/vmail/%s/%s/maildirsize'%(domain,mailbox))
        if file == 1:
            f = open('/home/vmail/%s/%s/maildirsize'%(domain,mailbox))
            b = f.readlines()
            n = 1
            quota = int(b[0].split('S')[0])
            used = 0
            try:
                while n>=0:
          	    c = int(b[n].split(' ')[0])
          	    used += c
          	    n = n + 1
      	    except (IndexError):
                pass
    	else:
      	    print 'file is not present for %s'%(mailbox)

    	usage = float(used)/quota * 100
    	if usage > 80 and usage < 100:
      	    print '%s \t\t\t %d' % (mailbox,usage)
      	    warn(mailbox, usage, domain)
    	    a = a + 1

except (IndexError):
    pass
