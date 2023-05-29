from fastapi import APIRouter, status, Request, Depends
from sqlmodel import Session

from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from api.blog_apis import get_blogposts_api
from db.db import get_session_db

router = APIRouter()

templates = Jinja2Templates('web/templates')


@router.get('/', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def home_view(*, request: Request, session: Session = Depends(get_session_db)):

    blogposts = await get_blogposts_api(limit=3, session=session)

    context = {
        "page": "home",
        "blogposts": blogposts
    }

    return templates.TemplateResponse(
        'home.html',
        {'request': request, 'context': context},
    )
