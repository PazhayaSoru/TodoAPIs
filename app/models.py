from .database import Base
from sqlalchemy import Column,TIMESTAMP,Integer,String,Boolean,text,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):

  __tablename__= "users"

  id = Column(Integer,nullable=False,primary_key=True)
  username = Column(String,nullable=False,unique=True)
  password = Column(String,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))



class Task(Base):

  __tablename__ = "tasks"

  id = Column(String,nullable=False,primary_key=True)
  task = Column(String,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))
  user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
  completed = Column(Boolean,nullable=False,server_default=text('false'))

  user = relationship("User")
