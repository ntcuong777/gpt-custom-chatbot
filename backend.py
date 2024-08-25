from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv

from application.initializer import IncludeAPIRouter, SqlDatabaseInitializer
from common.config import settings

from application.main.scheduled_jobs.init_jobs import scheduler_thread


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app_shutdown()


def get_application():
    _app = FastAPI(
        title=settings.API_NAME, description=settings.API_DESCRIPTION, version=settings.API_VERSION
    )
    _app.include_router(IncludeAPIRouter())
    _app.add_middleware(
        CORSMiddleware,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


load_dotenv(find_dotenv())
SqlDatabaseInitializer.init_database()
app = get_application()


async def app_shutdown():
    # on app shutdown do something probably close some connections or trigger some event
    print("On App Shutdown i will be called.")
    # stop scheduler thread
    scheduler_thread.set()


# if settings.ENV_STATE == "prod":
#     import uvicorn
#     uvicorn.run("backend:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOG_LEVEL, use_colors=True, reload=False)
