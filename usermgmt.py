#!/usr/bin/env python
from apiTool import *
import MySQLdb

def useradd_db(user):
    #Set Connection Parameters
    connection = MySQLdb.connect(
                host = '10.209.128.62',
                user = 'mailman',
                passwd = 'WTFpassword1***',)

    data = user_get(user)
    name = data['name']
    date_created = data['createdDate'][:9]
    usagemb = data['currentUsage']
    usagegb = mb_to_gb(usagemb)
    percentused = (float(usagemb) / float(25600)) * 100

    #Establish connection
    cursor = connection.cursor()
    #Execute Queries
    cursor.execute("USE maildash;")
    cursor.execute("INSERT INTO User (username, date_created, usagegb, usagemb, percentused) VALUES (%s, %s, %s, %s, %s);", (name, date_created, usagegb, usagemb, percentused))
    connection.commit()

    connection.close()

def userdel_db(user):
    #Set Connection Parameters
    connection = MySQLdb.connect(
                host = '10.209.128.62',
                user = 'mailman',
                passwd = 'WTFpassword1***',)

    name = user
    #Establish connection
    cursor = connection.cursor()
    #Execute Queries
    query = "DELETE FROM maildash.User WHERE username = '%s';" % name
    cursor.execute(query)
    connection.commit()
    connection.close()

def user_update_db(user, new_user):
    #Set Connection Parameters
    connection = MySQLdb.connect(
                host = '10.209.128.62',
                user = 'mailman',
                passwd = 'WTFpassword1***',)

    #Establish connection
    cursor = connection.cursor()
    #Execute Queries
    query = "UPDATE maildash.User SET username = '%s' where username = '%s';" % (new_user, user)
    cursor.execute(query)
    connection.commit()
    connection.close()
