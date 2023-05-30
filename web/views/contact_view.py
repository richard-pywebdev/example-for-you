import datetime
import os

from fastapi import HTTPException, status, APIRouter, Form, Depends
from sqlmodel import Session

from starlette.requests import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from api.captcha_apis import generate_captcha_func, create_captcha_text_api, get_captcha_by_id_api, \
    delete_captcha_by_id_api
from config.settings import settings
from db.db import get_session_db
from mail.sendmail import send_message_or_500

router = APIRouter()
templates = Jinja2Templates('web/templates')


# Contact From
@router.get('/contact', response_class=HTMLResponse)
async def contact_get_view(request: Request, session: Session = Depends(get_session_db)):

    new_captcha, random_letters, timestamp, filename = await generate_captcha_func()
    await create_captcha_text_api(captcha_in=new_captcha, session=session)

    context = {
        "page": "contact",
        "captcha_image": settings.CONF_CAPTCHA_CONTEXT_PATH + filename
    }

    return templates.TemplateResponse(
        'contact_form.html',
        {'request': request, 'context': context},
    )


@router.post("/contact", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def contact_post_view(*, request: Request,
                            name: str = Form(...),
                            email: str = Form(...),
                            message: str = Form(...),
                            captcha_text_input: str = Form(...),
                            session: Session = Depends(get_session_db)):

    captcha_text = await get_captcha_by_id_api(id=captcha_text_input, session=session)

    if datetime.datetime.utcnow() > captcha_text.created + datetime.timedelta(minutes=10):
        expired = True
    else:
        expired = False

    if captcha_text == "No captcha found." or expired:
        new_captcha, random_letters, timestamp, filename = await generate_captcha_func()
        await create_captcha_text_api(captcha_in=new_captcha, session=session)

        error_message = "Captcha did not match."
        name = name
        email = email
        message = message
        context = {
            "page": "contact",
            "name": name,
            "email": email,
            "message": message,
            "captcha_image": settings.CONF_CAPTCHA_CONTEXT_PATH + filename,
            "error_message": error_message
        }

        return templates.TemplateResponse(
            'contact_form.html',
            {'request': request, 'context': context},
        )

    try:

        message = "You have a message from " \
                  + name \
                  + ".\n\n" \
                  + message \
                  + ".\n\n" \
                  + "Message from contact form at www.exampleforyou.net from " \
                  + email + "."

        await send_message_or_500(message=message)

        filename = settings.CONF_CAPTCHA_FILE_PATH + captcha_text.captcha_image
        os.remove(filename)

        await delete_captcha_by_id_api(id=captcha_text.id, session=session)

        context = {
            'page': 'contact'
        }

        return templates.TemplateResponse('message_sent.html', {'request': request, "context": context})

        context = {
            'page': 'contact'
        }

        return templates.TemplateResponse('message_sent.html', {'request': request, "context": context})

    except KeyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
