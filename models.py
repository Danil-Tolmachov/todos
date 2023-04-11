from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, index=True)
    
    ###


class Todo(Base):

    __tablename__ = 'todos'
    id = Column('id', Integer, primary_key=True, index=True)

    ###
