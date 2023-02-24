import models
from database import engine, SessionLocal


def get_db():
    models.Base.metadata.create_all(bind=engine)
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
