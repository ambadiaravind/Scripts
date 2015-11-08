#!/usr/bin/env python

""" This takes the nagios realtime status dada and outputs as XML. """

import re
import sys
import datetime
import math

a = []

# no of content to display in output
ar=sys.argv[1]

# Nagios status file
status_file="/usr/local/nagios/var/status.log"

# fixme - the following token change dependiong on the version of Nagios
hosttoken='hoststatus'
servicetoken='servicestatus'
programtoken='programstatus'

def GetDefinitions(filename,obj):
    """ Parse the status.dat file and extract matching object definitions """
    file=open(filename)
    content=file.read().replace("\t"," ")
    file.close
    pat=re.compile(obj +' \{([\S\s]*?)\}',re.DOTALL)
    finds=pat.findall(content)
    return finds

def GetDirective(item,directive):
    """ parse an object definition, return the directives """
    pat=re.compile(' '+directive + '[\s= ]*([\S, ]*)\n')
    m=pat.search(item)
    if m:
      return m.group(1)

services=GetDefinitions(status_file,servicetoken)

for servicedef in services:
    host_name=GetDirective(servicedef,"host_name").strip()
    serv_desc=GetDirective(servicedef,"service_description").strip()
    check_exec=GetDirective(servicedef,"check_execution_time").strip()
    check_latn=GetDirective(servicedef,"check_latency").strip()
    actv_enb=GetDirective(servicedef,"active_checks_enabled").strip()
    a.append((float(check_exec),float(check_latn),host_name,serv_desc))

b=sorted(a, key=lambda k: k[0], reverse=True)

print ''.join([s.center(20) for s in \
    ('Check_Execution_Time', 'Check_Latency', 'Hostname', 'Service_Description')])

f=1

for c in b:
    if f <= int(ar):
      print ''.join([str(d).center(20) for d in c])
    else:
      pass
    f=f+1
