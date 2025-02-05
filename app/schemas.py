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

  
class TokenData(BaseModel):
  id : Optional[str] = None
