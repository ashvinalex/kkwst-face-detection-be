from fastapi import FastAPI, Depends, File, APIRouter
from sqlalchemy.orm import Session
from routers.auth import get_current_user, get_user_exception
from routers import auth, appmain
from utils.db_utils import get_db
from fastapi.responses import RedirectResponse

description='''
--------------------
### This is part of an AI and ML Capstone project 
### 🥷🏼 Developers
* Ashvin Alex
* Bastian Castillo
* Darshan Ruparel
* Fadernel Bedoya
* Marcelo Munoz
--------------------
### Faculty supervisor:
* William Pourmajidi
--------------------
Version - 0.0.1
'''

app = FastAPI(title="KKWST Backend App",
              description=description,
              version="0.0.1")
db = get_db()

app.include_router(auth.router)
app.include_router(appmain.router)

@app.get("/")
async def home():
    return RedirectResponse("http://127.0.0.1:8001/docs")

