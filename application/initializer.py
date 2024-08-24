class LoggerInstance(object):
    def __new__(cls):
        from common.utility.logger.custom_logging import LogHandler
        return LogHandler()


class IncludeAPIRouter(object):
    def __new__(cls):
        from application.main.routers.chat_router import router as router_conversational_chat
        from application.main.routers.session_router import router as router_session_generator
        from fastapi.routing import APIRouter

        router = APIRouter()
        router.include_router(router_conversational_chat, prefix='/api/v1', tags=['conversational_chat'])
        router.include_router(router_session_generator, prefix='/api/v1', tags=['session_generator'])

        return router


class SqlDatabaseInitializer(object):
    @staticmethod
    def init_database():
        from application.main.database.sql import models
        from application.main.database.sql.sqlite import sqlite_engine
        models.Base.metadata.create_all(bind=sqlite_engine)


# instance creation
logger_instance = LoggerInstance()
