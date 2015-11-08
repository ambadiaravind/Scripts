#!/usr/bin/python

import os
import subprocess
import re

domn="linuz.in"
pattern="linuz"

p = subprocess.Popen("dig mx %s +noall +answer +short | awk '{ print $2 }'"\
                               %domn, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
for mx_r in output.splitlines(): 
    print mx_r
    if re.search(pattern, mx_r):
        print "matches"

