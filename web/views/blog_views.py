import os
import readtime
from typing import Optional
from PIL import Image
import markdown
from fastapi import APIRouter, status, Request, Depends, Form, UploadFile, File
from pydantic.types import UUID
from sqlmodel import Session

from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from api.blog_apis import get_blogpost_by_id_api, create_blogpost_api, update_blogpost_api, delete_blogpost_by_id_api
from config.settings import settings
from db.db import get_session_db
from db.schemas.blog_schemas import BlogPostIn

router = APIRouter()

templates = Jinja2Templates('web/templates')


@router.get('/blog/create', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def blogpost_create_get_view(*, request: Request):
    context = {
        "page": "create"
    }

    return templates.TemplateResponse(
        'blog_create.html',
        {'request': request, 'context': context},
    )


@router.post('/blog/create', response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def blogpost_create_post_view(*,
                                    title: str = Form(...),
                                    teaser: str = Form(...),
                                    content: str = Form(...),
                                    cover_image: UploadFile,
                                    published: bool = Form(False),
                                    session: Session = Depends(get_session_db)):
    image = await cover_image.read()

    with open(settings.CONF_IMAGE_UPLOADS_FILE_PATH + cover_image.filename, 'wb') as file:
        file.write(image)

    # Resize images with Pillow
    img = Image.open(settings.CONF_IMAGE_UPLOADS_FILE_PATH + cover_image.filename)
    img_resize = img.resize((1900, 600))
    img_resize.save(settings.CONF_IMAGE_UPLOADS_FILE_PATH + "resized_" + cover_image.filename)
    os.remove(settings.CONF_IMAGE_UPLOADS_FILE_PATH + cover_image.filename)

    cover_image_file_path = settings.CONF_MAIN_DOMAIN + \
                            settings.CONF_IMAGE_UPLOADS_CONTEXT_PATH + \
                            "resized_" + \
                            cover_image.filename

    new_blogpost = BlogPostIn(title=title, teaser=teaser, content=content, cover_image=cover_image_file_path,
                              published=published)

    await create_blogpost_api(blogpost_in=new_blogpost, session=session)

    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)


@router.get('/blog/update/{id}', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def blogpost_update_get_view(*, id: UUID, request: Request, session: Session = Depends(get_session_db)):
    post = await get_blogpost_by_id_api(id=id, session=session)

    context = {
        "page": "blog_update",
        "post": post
    }

    return templates.TemplateResponse(
        'blog_update.html',
        {'request': request, 'context': context},
    )


@router.post('/blog/update', response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def update_blogpost_post_view(*,
                                    id: str = Form(...),
                                    title: str = Form(...),
                                    teaser: str = Form(...),
                                    content: str = Form(...),
                                    cover_image: Optional[UploadFile] = File(None),
                                    current_image: str = Form(...),
                                    published: bool = Form(False),
                                    session: Session = Depends(get_session_db)):
    if not cover_image.filename:
        cover_image_file_path = current_image
    else:
        image = await cover_image.read()

        with open(settings.CONF_IMAGE_UPLOADS_FILE_PATH + cover_image.filename, 'wb') as file:
            file.write(image)

        # Resize images with Pillow
        img = Image.open(settings.CONF_IMAGE_UPLOADS_FILE_PATH + cover_image.filename)
        img_resize = img.resize((1900, 600))
        img_resize.save(settings.CONF_IMAGE_UPLOADS_FILE_PATH + "resized_" + cover_image.filename)
        os.remove(settings.CONF_IMAGE_UPLOADS_FILE_PATH + cover_image.filename)

        cover_image_file_path = settings.CONF_MAIN_DOMAIN + \
                                settings.CONF_IMAGE_UPLOADS_CONTEXT_PATH + \
                                "resized_" + \
                                cover_image.filename

    blogpost_updates = BlogPostIn(title=title, teaser=teaser, content=content, cover_image=cover_image_file_path,
                                  published=published)

    await update_blogpost_api(id=id, data=blogpost_updates, session=session)

    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)


@router.get('/blog/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blogpost_get_view(*, id: UUID, session: Session = Depends(get_session_db)):
    await delete_blogpost_by_id_api(id=id, session=session)

    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)


@router.get('/blog/{id}', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def blogpost_get_view(*, id: UUID, request: Request, session: Session = Depends(get_session_db)):

    post = await get_blogpost_by_id_api(id=id, session=session)
    markdown_content = markdown.markdown(post.content)
    blogpost_readtime = readtime.of_markdown(markdown_content)

    context = {
        "page": "blog",
        "post": post,
        "markdown": markdown_content,
        "blogpost_readtime": blogpost_readtime
    }

    return templates.TemplateResponse(
        'blogpost.html',
        {'request': request, 'context': context},
    )
