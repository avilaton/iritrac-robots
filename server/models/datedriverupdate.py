from sqlalchemy import create_engine, Column, Integer, Sequence, String
from server import Base

class DateDriverUpdate(Base):
    __tablename__ = 'datedriverupdate'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    lastdriverId= Column(Integer)