from sqlalchemy import Boolean, Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    phone_numbers = Column(String)
    is_active = Column(Boolean)
    user_relation = relationship("User_Relation", back_populates="user")


class User_Relation(Base):
    __tablename__ = "user_relation"
    user_relation_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    relation = Column(String)
    image_url = Column(String)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    user = relationship("User", back_populates="user_relation")
