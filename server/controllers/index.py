#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import template, request
from server import app
from server.services import Iritrack

@app.route('/')
def index(db):
  return template('index.html')

@app.post('/')
def uploadDrivers():
  return template('index.html')
