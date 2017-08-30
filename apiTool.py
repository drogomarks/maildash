#!/usr/bin/env python
import base64
import hashlib
import time
import requests
import json
import config

# Set vars from args
mbx_type = 'rs'
mbx_key = 'rsMailboxes'

# Pull Keys and Customer ID from config
cst_id = config.cst_id
domain = config.domain
usrkey = config.usrkey
scrtkey = config.scrtkey
usr_agent  = config.usr_agent

# Get Date/Time: YYYYMMDDHHmmss
tm_stmp = time.strftime("%Y%m%d%H%M%S")
# Hash: <User Key><User Agent><Timestamp><Secret Key>
hash_str = usrkey + usr_agent + tm_stmp + scrtkey
# Get the hash
sha1 = base64.b64encode(hashlib.sha1(hash_str).digest())
# Create API Signature
api_sig = usrkey + ":" + tm_stmp + ":" + sha1
# Base URL/Headers
base_url  = "https://api.emailsrvr.com/v1/customers/"
headers = {"Accept":"application/json", "User-Agent" : usr_agent, "X-Api-Signature" : api_sig}


def mb_to_gb(size):
    gigabyte = 1.0/1024
    convert_gb = gigabyte * size
    convert_gb = round(convert_gb, 2)
    return convert_gb

def user_get(user):
    url = base_url + cst_id + "/domains/" + domain + "/" + mbx_type +  "/mailboxes/" + user
    request = requests.get(url, headers=headers)
    data = request.json()
    #data = json.dumps(data, indent=4, sort_keys=True)
    return data

def domain_get(domain):
    url = base_url + cst_id + "/domains/" + domain
    request = requests.get(url, headers=headers)
    data = request.json()
    #max_mailboxes = data['EmailMaxNumberMailboxes']
    #curr_mailboxes = data['rsEmailUsedStorage']
    #avail_mailboxes = max_mailboxes - curr_mailboxes
    #mailbox_stats = [max_mailboxes, curr_mailboxes, avail_mailboxes]
    return data

def mbx_get(domain):
    # offset value/url string
    off_val = 0
    off_str = "&offset=%s" % off_val
    # size value/url string
    sz_val= 50
    sz_str = "?size=%s" % sz_val

    url = base_url + cst_id + "/domains/" + domain + "/" + mbx_type +  "/mailboxes" + sz_str + off_str
    request = requests.get(url, headers=headers)
    data = request.json()
    mbx_total = data['total']
    # Empty list for mailboxes
    global mailboxes
    mailboxes = []
    # Offset Val variable to start at 0
    off_val = -50
    # While the offset value is less than the total mbx
    while mbx_total > off_val:
        # Set off value to self + the size value
        off_val += sz_val
        off_str = "&offset=%s" % off_val
        # Construct URL and make call
        url = base_url + cst_id + "/domains/" + domain + "/" + mbx_type +  "/mailboxes" + sz_str + off_str
        request = requests.get(url, headers=headers)
        data = request.json()
        # Add Users to Mailbox list
        for key in data[mbx_key]:
            mbx_usr = key['name']
            mailboxes.append(mbx_usr)
    data = json.dumps(mailboxes, indent=4, sort_keys=True)
    return mailboxes

def add_mbx(user, passwd, first_name, last_name, display_name):
    mbx_size = '25600'

    payload = {'password' : passwd, 'size' : mbx_size, 'firstName' : first_name, 'lastName' : last_name, 'displayName' : display_name}
    url = base_url + cst_id + "/domains/" + domain + "/" + mbx_type +  "/mailboxes/" + user
    request = requests.post(url, headers=headers, data=payload)
    status_code = request.status_code
    return status_code

def edit_mbx(user, new_username, passwd):
    payload = {'name' : new_username, 'password' : passwd}
    url = base_url + cst_id + "/domains/" + domain + "/" + mbx_type +  "/mailboxes/" + user
    request = requests.put(url, headers=headers, data=payload)
    status_code = request.status_code
    data = request.json()
    print data


def delete_mbx(user):
    url = base_url + cst_id + "/domains/" + domain + "/" + mbx_type +  "/mailboxes/" + user
    request = requests.delete(url, headers=headers)
    status_code = request.status_code
    return status_code

    data = request.json()
    data = json.dumps(data, indent=4, sort_keys=True)
    return data
