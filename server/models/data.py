#!/usr/bin/python
# -*- coding: utf-8 -*-

from server import db
import sqlite3

class Data(object):
  """represents a data row from the iritrack db"""
  db = db
  tablename = "data"

  def __init__(self, dict=None):
    self.store = {}
    if dict is not None: self.store.update(dict)

  def __repr__(self):
    return self.store.__repr__()

  @classmethod
  def getRowsByDriverId(cls, driver_id):
    cursor = cls.db.cursor()
    cursor.execute("SELECT * FROM "+cls.tablename+" WHERE Alpha=$1",
      (driver_id,))
    return [Data(dict(r)) for r in cursor.fetchall()]

  @classmethod
  def drop(cls):
    cursor = cls.db.cursor()
    try:
      cursor.execute("DROP TABLE IF EXISTS"+cls.tablename)
      print "Droped table"
      cls.db.commit()
    except sqlite3.IntegrityError:
      print "Error droping table"

  @classmethod
  def create(cls):
    cursor = cls.db.cursor()
    try:
      cursor.execute("CREATE TABLE "+cls.tablename+''' (
        Alpha TEXT,
        DATE TEXT,
        LATITUD TEXT,
        LONG  TEXT,
        SPEED TEXT,
        ALTITUD TEXT,
        EVENT TEXT,
        ZONE TEXT,
        VEHICLE TEXT)''')
      print "Table created"
      cls.db.commit()
    except sqlite.IntegrityError:
      print "Error creating table"



