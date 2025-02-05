from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter,status,Depends,HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app import models,utils,oauth2


router  = APIRouter(
  tags=['Authentication'],
)


@router.post('/login',status_code=status.HTTP_202_ACCEPTED)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
  
  password = user_credentials.password

  username = user_credentials.username

  user = db.query(models.User).filter(models.User.username == username).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credentials')
  
  if not utils.verify_password(password,user.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credentials')
  
  access_token = oauth2.create_access_token({'user_id':str(user.id)})

  return {'token':access_token,'type':'bearer'}