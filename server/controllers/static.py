# -*- coding: utf-8 -*-
from server import app
from bottle import static_file


@app.route('/:file#(favicon.ico|humans.txt)#')
def favicon(file):
  return static_file(file, root='project/static/misc')

@app.get('/static/<filepath:path>')
def index(filepath):
  return static_file(filepath, root='./static/')
