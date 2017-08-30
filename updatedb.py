#!/usr/bin/env python
from apiTool import *
import MySQLdb

mailboxes = mbx_get('iccenter.org')

#Set Connection Parameters
connection = MySQLdb.connect(
            host = 'X',
            user = 'X',
            passwd = 'X',)

for mbx in mailboxes:
    data = user_get(mbx)
    name = data['name']
    date_created = data['createdDate'][:9]
    usagemb = data['currentUsage']
    usagegb = mb_to_gb(usagemb)
    percentused = (float(usagemb) / float(25600)) * 100

    print "Updating %s.." % name
    print date_created
    print usagemb
    print usagegb
    print percentused

    #Establish connection
    cursor = connection.cursor()
    #Execute Queries
    cursor.execute("USE maildash;")
    #cursor.execute("INSERT INTO User (username, date_created, usagegb, usagemb, percentused) VALUES (%s, %s, %s, %s, %s);", (name, date_created, usagegb, usagemb, percentused))
    cursor.execute("UPDATE User SET date_created=%s, usagegb=%s, usagemb=%s, percentused=%s WHERE username=%s", (date_created, usagegb, usagemb, percentused, name))
    connection.commit()

connection.close()
