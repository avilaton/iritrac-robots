# -*- coding: utf-8 -*-
__version__ = '0.1'
from bottle import Bottle, TEMPLATE_PATH
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Bottle()

# TEMPLATE_PATH.append("./server/views/")
# TEMPLATE_PATH.remove("./views/")

IRITRACK_USER = 'ruta2'
IRITRACK_PASS = 'DESAFIO'

DATABASE_URL = 'sqlite:///db.sqlite'
# DATABASE_URL = 'sqlite:///:memory:'

Base = declarative_base()
# engine = create_engine(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=False)

from models import Data

Base.metadata.create_all(engine)

plugin = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    Base.metadata, # SQLAlchemy metadata, required only if create=True.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)

app.install(plugin)

from controllers import *


# from worker import updateDrivers

# updateDrivers()

import atexit
from apscheduler.scheduler import Scheduler

sched = Scheduler(daemon=True)
# sched = Scheduler()
# 	atexit.register(lambda: sched.shutdown(wait=False))

# sched.add_interval_job(updateDrivers, seconds=5)
