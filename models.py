from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    
    todos = relationship('Todo', back_populates='user')


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    description = Column(String)
    importance = Column(Integer, default=1)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='todos')
