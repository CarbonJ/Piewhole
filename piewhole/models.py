import datetime
from sqlalchemy import  Column, Integer, Text, Float, ForeignKey, Date
from  . database  import Base, engine

class Ranks(Base):
    __tablename__ = "Ranks"
    id = Column(Integer, primary_key=True, unique=True)
    rank = Column(Text(15), unique=True)


class Weight(Base):
    __tablename__ = "Weight"
    id = Column(Integer, primary_key=True, unique=True)
    weight = Column(Float)
    weight_date = Column(Date)
    weight_delta = Column(Float)
    user_id = Column(Integer, ForeignKey('User.id'))


class Food(Base):
    __tablename__ = "Food"
    id = Column(Integer, primary_key=True, unique=True)
    food = Column(Text)
    food_date = Column(Date)
    rank_id = Column(Integer, ForeignKey('Ranks.id'))
    user_id = Column(Integer, ForeignKey('User.id'))


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(Text)
    email = Column(Text, unique=True)
    password = Column(Text)


class Goals(Base):
    __tablename__ = "Goals"
    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    weight_goal = Column(Text)

Base.metadata.create_all(engine)