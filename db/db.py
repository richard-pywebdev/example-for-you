from sqlmodel import create_engine, Session

from config.settings import settings

engine = create_engine(
    settings.CONF_MAIN_APP_SQLITE,
    connect_args={"check_same_thread": False},
    echo=True
)


def get_session_db():
    with Session(engine) as session:
        yield session