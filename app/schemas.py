from pydantic import BaseModel
from datetime import datetime
from typing import Optional


#schemas for User
class UserBase(BaseModel):
  id : int
  username : str


class UserCreate(UserBase):
  password : str

class User(UserBase):
  created_at : datetime
  class Config():
    from_attributes = True

  

class TaskBase(BaseModel):
  task : str

class TaskCreate(TaskBase):
  user_id : int

class Task(TaskBase):
  id : int
  created_at : datetime

  class Config:
    from_attributes = True


class Token(BaseModel):
  token : str
  type : str

class TokenData(BaseModel):
  id : Optional[str] = None
