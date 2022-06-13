from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, Text, PrimaryKeyConstraint, VARCHAR
from sqlalchemy.orm import relationship

Base = declarative_base()
   
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    firstName = Column(String(32), nullable=False)
    lastName = Column(String(32), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(32), nullable=False, unique=True)
    phone = Column(String(32), nullable=False, unique=True)

class Events(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    header = Column(String(32), nullable=False)
    description = Column(String(32), nullable=False)
    date = Column(Date, nullable=False)

class System(Base):
    __tablename__ = 'system'
    userId = Column(Integer, ForeignKey('users.id'))
    eventId = Column(Integer, ForeignKey('events.id'))
    users = relationship('User')
    events = relationship('Events')
    __table_args__ = (
        PrimaryKeyConstraint(userId, eventId),
        {},
    )