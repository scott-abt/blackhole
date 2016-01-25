#!/usr/bin/env python3

from datetime import datetime as DT
from urllib import request
import re
import ipcalc
import sqlite3
from sqlite3 import IntegrityError

now = str(DT.now())

req = request.Request(
        'http://www.spamhaus.org/drop/drop.txt',
        headers={ 'User-Agent': 'Mozilla/5.0' } )

html = request.urlopen(req)
html_response = html.read().decode('utf-8')
split_html = html_response.split("\n")

ip_db = sqlite3.connect('ip_addrs.db')
c = ip_db.cursor()

current_table = c.execute("SELECT ip FROM ip_addrs_found WHERE valid = '1'")

inserted = 0
updated = 0

for line in split_html:
    if re.match('^;', line):
        continue
    splitLine = line.split()
    if splitLine and ipcalc.Network(splitLine[0]):
        insert_string = "INSERT INTO ip_addrs_found VALUES (?, ?, ?, ?)"
        try:
            c.execute(insert_string, (splitLine[0], now, now, 1))
            inserted += 1
        except IntegrityError as e:
            try:
                c.execute("UPDATE ip_addrs_found set last_seen = ? \
                           WHERE ip = ?", (now, splitLine[0]))
                updated += 1
            except:
                raise
if c.rowcount and (updated > 0 or inserted > 0):
    print("Updating: {0}\nInserting: {1}".format(updated, inserted))
    ip_db.commit()
