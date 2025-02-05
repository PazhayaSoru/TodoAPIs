from fastapi import FastAPI
from .routers import users,tasks,auth




app = FastAPI()

@app.get('/')
def root():
  return {'hi macha':'epdi iruka'}

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(auth.router)