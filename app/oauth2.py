from jose import jwt,JWTError
from . import database,schemas
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from sqlalchemy.orm import Session
from . import database,models,config
from fastapi import Depends,HTTPException,status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.jwt_algorithm
TOKEN_EXPIRE_TIME_MINUTES = config.settings.token_expire_minutes


def create_access_token(data : dict):
  data_to_encode = data.copy()
  expiration_date = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_TIME_MINUTES)
  data_to_encode['exp'] = expiration_date
  jwt_token = jwt.encode(data_to_encode,SECRET_KEY,algorithm=ALGORITHM)
  return jwt_token


def verify_access_token(token : str,credentials_exception):
  try:
    decoded_token = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM,])
    user_id  = decoded_token.get('user_id')

    if user_id is None:
      raise credentials_exception
    token_data = schemas.TokenData(id = user_id)
  except JWTError:
    raise credentials_exception
  return token_data


def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
  credentials_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Could not validate Credentials",headers={"WWW-Authenticate": "Bearer"})

  token = verify_access_token(token,credentials_exception)

  user_id = token.id 
  
  user = db.query(models.User).filter(models.User.id == user_id).first()

  return user

  