from fastapi import Depends,HTTPException,status,APIRouter
from app import models,schemas,utils
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app import oauth2


router = APIRouter(
  prefix='/users',
  tags=['Users'],
)

@router.get('/',response_model=List[schemas.User],status_code=status.HTTP_200_OK)
def get_users(db : Session = Depends(get_db)):
  users = db.query(models.User).all()
  return users

@router.post("/",response_model=schemas.User,status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db : Session = Depends(get_db)):

  hashed_pwd = utils.hash_password(user.password)
  user.password = hashed_pwd
  new_user = models.User(**user.model_dump())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return (new_user)

@router.delete('/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id : int,db : Session = Depends(get_db),user : dict = Depends(oauth2.get_current_user)):
  
  user_query = db.query(models.User).filter(models.User.id == user_id)

  found_user = user_query.first()
  if not found_user:
    raise HTTPException(status_code=404,detail=f'User with UserID:{user_id} not found')
  if found_user.id != user.id:
        raise HTTPException(status_code=404,detail=f'You are not Authorized to perform the requested action')
  user_query.delete(synchronize_session=False)
  db.commit()
  return {"success":"User successfully removed"}



@router.put('/{user_id}',response_model=schemas.User,status_code=200)
def update_user(user_id : int,user_update : schemas.UserCreate,db : Session = Depends(get_db),user : dict = Depends(oauth2.get_current_user)):
  found_user_query = db.query(models.User).filter(models.User.id == user_id)
  hashed_pwd = utils.hash_password(user_update.password)
  user_update.password = hashed_pwd
  found_user = found_user_query.first()
  if not found_user:
    raise HTTPException(status_code=404,detail=f'User with UserID: {user_id} not found')
  if found_user.id != user.id:
     raise HTTPException(status_code=404,detail=f'You are not Authorized to perform the requested action')
  try:
    user_update_dict = dict(user_update)
    user_update_dict['id'] = user_id
    user_update_dict['username'] = user.username
    user_update_dict['password'] = user.password
    user_update_dict['created_at'] = found_user.created_at
    found_user_query.update(user_update_dict,synchronize_session=False)
    db.commit()
  except:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Unable to Update the User with UserID: {user_id}")
  return (user_update_dict)

  