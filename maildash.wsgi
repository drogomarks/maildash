#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/vhosts/maildash.iccenter.org/")

from maildash import app as application
application.secret_key = 'development-key'
