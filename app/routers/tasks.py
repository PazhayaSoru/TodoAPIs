from fastapi import Depends,HTTPException,status,APIRouter
from app import models,schemas,oauth2
from app.database import get_db
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
  prefix='/tasks',
  tags=['Tasks'],
)


@router.get('/',response_model=List[schemas.Task],status_code=status.HTTP_200_OK)
def get_tasks(db : Session = Depends(get_db),user : dict = Depends(oauth2.get_current_user)):
  count = db.query(models.Task).filter(models.Task.user_id == user.id).all()
  tasks = db.query(models.Task).filter(models.Task.user_id == user.id).all()
  print(count)
  return (tasks)

@router.post('/',response_model=schemas.Task,status_code=status.HTTP_200_OK)
def create_task(input_task : schemas.TaskBase,db : Session = Depends(get_db),user : dict = Depends(oauth2.get_current_user)):
  print(user.id)
  task_dict = dict(input_task)
  task_dict['task'] = input_task.task
  task_dict['user_id'] = user.id
  task_model = models.Task(**task_dict)
  try:
    db.add(task_model)
    db.commit()
    db.refresh(task_model)
  except:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Unable to Register the Task")
  return task_model

@router.delete('/{task_id}',status_code=status.HTTP_200_OK)
def delete_task(task_id : int,db : Session = Depends(get_db), user  : dict = Depends(oauth2.get_current_user)):
  found_task_query  = db.query(models.Task).filter(models.Task.id == task_id)
  found_task = found_task_query.first()

  if not found_task:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The Task with TaskID: {task_id} does not exist')
  if found_task.user_id != user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not Authorized to perform the requested action")
  try:
    found_task_query.delete(synchronize_session=False)
    db.commit()
  except:
    raise HTTPException(status_code=409,detail="Unable to Perform the Requested Action")
  
  return {"delete":"success"}

@router.put('/{task_id}',response_model=schemas.Task,status_code=status.HTTP_202_ACCEPTED)
def update_task(task_id : int,task : schemas.TaskBase,user : dict = Depends(oauth2.get_current_user), db : Session = Depends(get_db)):
  found_task_query  = db.query(models.Task).filter(models.Task.id == task_id)
  found_task = found_task_query.first()

  if not found_task:
    raise HTTPException(status_code=404,detail=f"Task with TaskID: {task_id} does not exist")
  if found_task.user_id!= user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
  
  task_dict = dict(task)
  found_task_query.update(task_dict,synchronize_session=False)
  db.commit()
  db.refresh(found_task)

  return found_task