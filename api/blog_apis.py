from pydantic.types import UUID

from fastapi import Depends, status, APIRouter, HTTPException
from sqlmodel import Session, select

from db.schemas.blog_schemas import BlogPostIn, BlogPost, BlogPostOut
from db.db import get_session_db

router = APIRouter()


# Create
@router.post('/blog/create', status_code=status.HTTP_201_CREATED)
async def create_blogpost_api(blogpost_in: BlogPostIn, session: Session = Depends(get_session_db)) -> BlogPost:
    new_blogpost = BlogPost.from_orm(blogpost_in)
    session.add(new_blogpost)
    session.commit()
    session.refresh(new_blogpost)
    return new_blogpost


# Read
@router.get('/blog', status_code=status.HTTP_200_OK)
async def get_blogposts_api(limit: int | None = None, session: Session = Depends(get_session_db)) -> list:
    query = select(BlogPost).limit(limit).order_by(BlogPost.created_date.desc())
    return session.exec(query).all()


@router.get('/blog/{id}', response_model=BlogPostOut, status_code=status.HTTP_200_OK)
async def get_blogpost_by_id_api(id: UUID, session: Session = Depends(get_session_db)) -> BlogPost:
    post = session.get(BlogPost, id)
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail=f"No blog post found with id {id}.")


# Update
@router.put('/blog/{id}', response_model=BlogPost, status_code=status.HTTP_202_ACCEPTED)
async def update_blogpost_api(id: UUID, data: BlogPostIn, session: Session = Depends(get_session_db)) -> BlogPost:
    post = session.get(BlogPost, id)
    if post:
        post.title = data.title
        post.teaser = data.teaser
        post.content = data.content
        post.cover_image = data.cover_image
        session.commit()
        return post
    else:
        raise HTTPException(status_code=404, detail=f"No blog post found with id {id}.")


# Delete
@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blogpost_by_id_api(id: UUID, session: Session = Depends(get_session_db)) -> None:
    post = session.get(BlogPost, id)
    if post:
        session.delete(post)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No blog post found with id {id}.")