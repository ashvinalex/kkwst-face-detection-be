from fastapi import FastAPI, Depends, File, APIRouter
from sqlalchemy.orm import Session
from routers.auth import get_current_user, get_user_exception
from routers import auth, appmain
from utils.db_utils import get_db
from fastapi.responses import RedirectResponse

description='''
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

