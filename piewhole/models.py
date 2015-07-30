#import datetime
from flask.ext.login import UserMixin
from sqlalchemy import  Column, Integer, String, Float, ForeignKey, Date
from  . database  import Base, engine

class Ranks(Base):
    __tablename__ = 'Ranks'
    id = Column(Integer, primary_key=True, unique=True)
    # rank 1,2,3 (1 best)
    # desc 1 = good, 2 = ok, 3 = bad
    rank = Column(Integer, unique=True)
    rankdesc = Column(String(15), unique=True)


class Weight(Base):
    __tablename__ = 'Weight'
    id = Column(Integer, primary_key=True, unique=True)
    weight = Column(Float)
    weight_date = Column(Date)
    user_id = Column(Integer, ForeignKey('User.id'))


class Food(Base):
    __tablename__ = 'Food'
    id = Column(Integer, primary_key=True, unique=True)
    food = Column(String)
    food_date = Column(Date)
    rank_id = Column(Integer, ForeignKey('Ranks.id'))
    user_id = Column(Integer, ForeignKey('User.id'))


class User(Base, UserMixin):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Goals(Base):
    __tablename__ = 'Goals'
    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    weight_goal = Column(Float)
    health_goal = Column(Float)

Base.metadata.create_all(engine)