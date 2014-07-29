#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, Sequence, String
from server import Base

class Stage(Base):
    __tablename__ = 'stage'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    stage_id = Column(String(50))
    zone = Column(String(50))

    def __repr__(self):
        return "<Stage: '%s' (stage_id:'%s', zone:'%s')>" % (self.id, self.stage_id, self.zone)