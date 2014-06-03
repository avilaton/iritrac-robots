#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import template, request
from server import app
from server.services import Iritrack
from server.models import Data

@app.get('/')
def index(db):
  results = db.query(Data).all()
  print results
  return template('index.html')

@app.post('/')
def updateDB(db):
  dateFrom = request.forms.get('from')
  dateFrom = request.forms.get('to')
  return template('index.html')
