#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, Sequence, String
from server import Base

class StartTime(Base):
    __tablename__ = 'starttime'
    gid = Column(Integer, Sequence('id_seq'), primary_key=True, autoincrement=True)
    id = Column(Integer)
    driver_group= Column(Integer,Sequence('id_seq'))
    name = Column(String(50))
    start_time = Column(String(50))
    stage_id = Column(String(20))
    def __repr__(self):
        return "<StartTime: '%s' (name:'%s', starttime:'%s')>" % (self.id, self.name, self.start_time)
