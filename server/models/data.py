#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

from server import Base

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    alpha = Column(String(50))
    date = Column(String(50))
    lat = Column(String(50))
    lon = Column(String(50))
    speed = Column(String(50))
    altitud = Column(String(50))
    event = Column(String(50))
    zone = Column(String(50))
    vehicle = Column(String(50))

    def __init__(self, alpha, lat, lon):
        self.alpha = alpha
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return "<Data('%d', lat:'%s', lon:'%s')>" % (self.id, self.lat, self.lon)

