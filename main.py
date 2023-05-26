import uvicorn
from fastapi import FastAPI
from api import health_api
from config.settings import settings

main_app = FastAPI()


def configure():
    configure_routing()


def configure_routing():
    main_app.include_router(health_api.router, prefix=settings.CONF_API_V1_STR, tags=["health"])


if __name__ == '__main__':
    configure()
    uvicorn.run(main_app,
                host=settings.CONF_MAIN_APP_HOST,
                port=settings.CONF_MAIN_APP_PORT)
else:
    configure()
