# -*- coding: utf-8 -*-
__version__ = '0.1'
from bottle import Bottle, TEMPLATE_PATH
app = Bottle()

# TEMPLATE_PATH.append("./server/views/")
# TEMPLATE_PATH.remove("./views/")
DATABASE = './db.sqlite'

import sqlite3

db = sqlite3.connect(DATABASE)
db.row_factory = sqlite3.Row

from  controllers import *