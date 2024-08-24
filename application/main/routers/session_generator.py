import secrets
from fastapi.routing import APIRouter

from application.initializer import LoggerInstance

router = APIRouter(prefix='/user_session')
logger = LoggerInstance().get_logger(__name__)


def make_token():
    """
    Creates a cryptographically-secure, URL-safe string
    """
    return secrets.token_urlsafe(32)


@router.get("/")
async def conversational_chat():
    session_id = make_token()
    logger.debug("Session ID = %s has been connected", session_id)
    return {"session_id": session_id}
