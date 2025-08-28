from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
import logging
from fastapi.templating import Jinja2Templates
from settings.base import TEMPLATES_DIR
# from tasks.monitoring import test_task

logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/state", include_in_schema=False)
async def health_check(request: Request):
    test_task.delay()
    return {"Status": "OK"}