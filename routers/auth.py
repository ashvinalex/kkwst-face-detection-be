import sys

sys.path.append("..")
from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
import yaml

credentials = yaml.load(open('credentials.yml'), Loader=yaml.Loader)
SECRET_KEY = credentials['secret']['secret_key']
ALGORITHM = credentials['secret']['algorithm']

router = APIRouter(prefix='/auth',
                   tags=["Authentication"],
                   responses={401: {"user": "Not Authorized"}}
                   )


class CreateUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    phones: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashedpassword):
    return bcrypt_context.verify(plain_password, hashedpassword)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + expires_delta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


@router.post('/create/user')
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.User()
    create_user_model.username = create_user.username
    create_user_model.email = create_user.email
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    hashedpassword = get_password_hash(create_user.password)
    create_user_model.hashed_password = hashedpassword
    create_user_model.phone_numbers = create_user.phones
    create_user_model.is_active = True
    db.add(create_user_model)
    db.commit()
    return {"status": 200}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.user_id, expires_delta=token_expires)
    return {
        'expires_at': token_expires,
        'token': token
    }


# Exceptions
def get_user_exception():
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})
    return credential_exception


def token_exception():
    token_exception_response = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Incorrect username or password",
                                             headers={"WWW-Authenticate": "Bearer"})
    return token_exception_response
