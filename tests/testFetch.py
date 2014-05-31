#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from server.models import Driver
from server import Base


DATABASE_URL = 'sqlite:///:memory:'

engine = create_engine(DATABASE_URL)

from server.models import *

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
print dir(session)

def setup():
    session.configure(bind=engine)
    # You probably need to create some tables and 
    # load some test data, do so here.

    # To create tables, you typically do:
    Base.metadata.create_all(engine)

def teardown():
    session.remove()


def test_something():
    instances = session.query(model.SomeObj).all()
    eq_(0, len(instances))
    session.add(model.SomeObj())
    session.flush()