from jose import jwt,JWTError
from . import database
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone


SECRET_KEY = "35285324354d562c245b031232115124372e5242394f51301f62224e1e432910"
ALGORITHM = 'SH256'
TOKEN_EXPIRE_TIME_MINUTES = 60


def create_access_token(data : dict):
  data_to_encode = data.copy()
  expiration_date = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_TIME_MINUTES)
  data_to_encode['exp'] = expiration_date
  jwt_token = jwt.encode(data_to_encode,SECRET_KEY,algorithm=ALGORITHM)
  return jwt_token


def verify_access_token(data : dict,):
  data_to_decode = data.copy()
  decoded_data = jwt.decode(data_to_decode,SECRET_KEY,algorithms=[ALGORITHM,])
  pass