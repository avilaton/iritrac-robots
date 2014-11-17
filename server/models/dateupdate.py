from sqlalchemy import create_engine, Column, Integer, Sequence, String
from server import Base

class DateUpdate(Base):
    __tablename__ = 'dateupdate'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    firstDate= Column(String(50))
    secondDate= Column(String(50))
    lastId= Column(Integer)