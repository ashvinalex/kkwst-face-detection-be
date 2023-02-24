from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    phone: int


class User_Relation(BaseModel):
    first_name: str
    last_name: str
    relation : str


