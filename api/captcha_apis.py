import datetime
import os
import random
import string

from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from captcha.image import ImageCaptcha

from config.settings import settings
from db.db import get_session_db
from db.schemas.captcha_schemas import CaptchaIn, Captcha, CaptchaOut

router = APIRouter()


# Functions
async def generate_captcha_func():
    letters = string.ascii_lowercase
    random_letters = ''.join(random.choice(letters) for i in range(5))
    image = ImageCaptcha(width=280, height=90)
    data = image.generate(random_letters)
    timestamp = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f'{random_letters}_{timestamp}.png'
    image.write(random_letters, os.path.join(settings.CONF_CAPTCHA_FILE_PATH, filename ))
    new_captcha = CaptchaIn(id=random_letters, captcha_image=filename)
    return new_captcha, random_letters, timestamp, filename


# APIs
@router.post('/captcha/create', status_code=status.HTTP_201_CREATED)
async def create_captcha_text_api(captcha_in: CaptchaIn, session: Session = Depends(get_session_db)) -> Captcha:
    new_captcha = Captcha.from_orm(captcha_in)

    session.add(new_captcha)
    session.commit()
    session.refresh(new_captcha)

    return new_captcha


@router.get('/captcha/find_all', status_code=status.HTTP_200_OK)
async def find_all_captcha_text_api(limit: int | None = None, session: Session = Depends(get_session_db)) -> list:
    query = select(Captcha).limit(limit).order_by(Captcha.created.desc())
    return session.exec(query).all()


@router.get('/captcha/find_id', response_model=CaptchaOut, status_code=status.HTTP_200_OK)
async def get_captcha_by_id_api(id: str, session: Session = Depends(get_session_db)) -> Captcha:
    captcha = session.get(Captcha, id)
    if captcha:
        return captcha
    else:
        return "No captcha found."


@router.delete('/captcha/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_captcha_by_id_api(id: str, session: Session = Depends(get_session_db)) -> None:
    captcha = session.get(Captcha, id)
    if captcha:
        session.delete(captcha)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No captcha found with id {id}.")