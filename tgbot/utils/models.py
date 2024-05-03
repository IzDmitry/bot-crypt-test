from sqlalchemy import Column, Integer, Float, \
    String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CryptCurencys(Base):
    __tablename__ = 'cryptcurencys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price = Column(Float)


class TrackCurency(Base):
    __tablename__ = 'trackcurency'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer)
    name_crypt = Column(String, ForeignKey('cryptcurencys.name'))
    max_curency = Column(Float)
    min_curency = Column(Float)
    status = Column(Boolean)
