import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.templating import Jinja2Templates

from api import health_api, blog_apis, captcha_apis
from config.settings import settings
from web.views import home_view, blog_views, contact_view

main_app = FastAPI()


# To disable APIs
# main_app = FastAPI(openapi_url=None)


# Custom 404 page
@main_app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    templates = Jinja2Templates('web/templates')
    return templates.TemplateResponse("404.html", {"request": request, "context": "404"})


# CORS
origins = [
    "http://localhost:8000",
    "https://localhost:8000",
    "https://www.exampleforyou.net:8000",
    "https://www.exampleforyou.net",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Middleware
@main_app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


def configure():
    configure_routing()


def configure_routing():
    main_app.mount('/static', StaticFiles(directory='web/static'), name='static')
    main_app.mount('/uploads', StaticFiles(directory=settings.CONF_IMAGE_UPLOADS_FILE_PATH), name='uploads')
    main_app.mount('/captcha', StaticFiles(directory=settings.CONF_CAPTCHA_FILE_PATH), name='captchas')
    main_app.include_router(health_api.router, prefix=settings.CONF_API_V1_STR, tags=["health"])
    main_app.include_router(blog_apis.router, prefix=settings.CONF_API_V1_STR, tags=["blog_apis"])
    main_app.include_router(captcha_apis.router, prefix=settings.CONF_API_V1_STR, tags=["captcha_apis"])
    main_app.include_router(home_view.router, tags=["web_views"])
    main_app.include_router(blog_views.router, tags=["web_views"])
    main_app.include_router(contact_view.router, tags=["web_views"])


if __name__ == '__main__':
    configure()
    uvicorn.run(main_app,
                host=settings.CONF_MAIN_APP_HOST,
                port=settings.CONF_MAIN_APP_PORT,
                log_level=settings.CONF_DEBUG_LEVEL,
                ssl_keyfile=settings.CONF_SSL_KEYFILE,
                ssl_certfile=settings.CONF_SSL_CERTFILE)
else:
    configure()
