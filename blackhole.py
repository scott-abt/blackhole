#!/usr/bin/env python

import urllib2
import re

req = urllib2.Request(
        'http://www.spamhaus.org/drop/drop.txt', headers={ 'User-Agent': 
        'Mozilla/5.0' })

html = urllib2.urlopen(req).read()

for line in html.split("\n"):
    if not re.match('^;', line):
        splitLine = line.split()
        if splitLine:
            # check that its a valid IP or cidr mask.

            # Change this to insert the IP to a database
            print('set policy-options prefix-list blackhole ' + splitLine[0])

            # Check to see if the IP is already in the list
            # Remove IP's that have aged out
            # Add new IP's
            # Update routing
