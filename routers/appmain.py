from fastapi import Depends, File, APIRouter, HTTPException, status, Form, UploadFile
from sqlalchemy.orm import Session
from routers.auth import get_current_user, get_user_exception
from utils.db_utils import get_db
from utils.base_models import User
from utils.responses import successful_response
import models
import uuid
import os

router = APIRouter(prefix='/kkwst',
                   tags=["AppMain"],
                   responses={401: {"description": "Not Authorized"}}
                   )


@router.put("/update_user")
async def update_user(user: User, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user is None:
        raise get_user_exception()
    user_model = db.query(models.User).filter(models.User.username == current_user.get("username")).first()
    user_model.username = user.username
    user_model.email = user.email
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.phone = user.phone
    db.add(user_model)
    db.commit()
    return successful_response(200)


@router.get("/app/user_relation")
async def get_all_user_relation(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.User_Relation).filter(str(models.User_Relation.user_id) == user.get("id")).all()


@router.post("/app/user_relation/")
async def create_user_relation(firstname: str = Form(...),
                               lastname: str = Form(...),
                               relation: str = Form(...),
                               user: dict = Depends(get_current_user),
                               image: UploadFile = File(...),
                               db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_relation_model = models.User_Relation()
    user_relation_model.first_name = firstname
    user_relation_model.last_name = lastname
    user_relation_model.relation = relation
    user_relation_model.image_url = await upload_image(image)
    user_relation_model.user_id = user.get("id")
    db.add(user_relation_model)
    db.commit()
    return successful_response(201)


@router.put("/app/user_relation/{user_relation_id}")
async def update_user_relation(user_relation_id: int,
                               firstname: str = Form(...),
                               lastname: str = Form(...),
                               relation: str = Form(...),
                               user: dict = Depends(get_current_user),
                               image: UploadFile = File(...),
                               db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_relation_model = db.query(models.User_Relation).filter(
        models.User_Relation.user_relation_id == user_relation_id).first()
    if user_relation_model is None:
        raise get_user_relation_exception()

    file_path = user_relation_model.image_url
    filename = os.path.basename(file_path)
    uuid_str = os.path.splitext(filename)[0]
    file_id = uuid.UUID(uuid_str)
    await delete_image(file_path)
    user_relation_model.first_name = firstname
    user_relation_model.last_name = lastname
    user_relation_model.relation = relation
    user_relation_model.image_url = await upload_image(image, file_id)
    user_relation_model.user_id = user.get("id")
    db.add(user_relation_model)
    db.commit()
    return successful_response(200)


@router.delete("/app/user_relation/{user_relation_id}")
async def delete_user_relation(user_relation_id: int,
                               user: dict = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_relation_model = db.query(models.User_Relation).filter(
        models.User_Relation.user_relation_id == user_relation_id).first()

    if user_relation_model is None:
        raise get_user_relation_exception()
    db.query(models.User_Relation).filter(
        models.User_Relation.user_relation_id == user_relation_id).delete()
    db.commit()
    return successful_response(200)


async def upload_image(image: UploadFile, file_name: uuid):
    # Create the directory if it doesn't exist
    image_path = os.path.join(os.getcwd(), "resources/static/images/")
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    content = await image.read()
    if image.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    # Save the image to the directory with a new name
    file_name = file_name if file_name is not None else str(uuid.uuid1())
    image_path = os.path.join(image_path, f"{file_name}.jpg")
    with open(image_path, "wb") as f:
        f.write(content)

    return image_path


async def delete_image(image_path: str):
    os.remove(image_path)


async def get_file_name(filepath: str):
    filename = os.path.basename(filepath)
    uuid_str = os.path.splitext(filename)[0]
    file_id = uuid.UUID(uuid_str)
    return file_id


def get_user_relation_exception():
    user_relation_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail="User Relation Not Found")
    return user_relation_exception
