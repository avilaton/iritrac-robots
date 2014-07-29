#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, Sequence, String
from server import Base

class LastUpdate(Base):
    __tablename__ = 'lastupdate'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    time= Column(Integer,Sequence('id_seq'))
    

    #def __repr__(self):
    #   return "<StartTime: '%s' (name:'%s', starttime:'%s')>" % (self.id, self.name, self.start_time)
