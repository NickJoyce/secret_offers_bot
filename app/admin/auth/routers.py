from fastapi import APIRouter, Depends
from fastapi import Request
import logging
from app.admin.auth.schemas import UserCreate, UserOutput
from app.utils.dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from settings import ADMIN_TOKEN
from secrets import compare_digest
from app.admin.auth.utils import create_user_instance
from app.admin.auth.utils import get_user_by_email


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/users", response_model=UserOutput)
async def create_user(user: UserCreate,
                      request: Request,
                      session: AsyncSession = Depends(get_session)):
    given_token = request.headers.get("Authorization", None)
    if compare_digest(given_token, ADMIN_TOKEN):
        su = await get_user_by_email(email=user.email, session=session)
        if su:
            raise HTTPException(status_code=400, detail="Email already registered")
        return await create_user_instance(user=user, session=session)
    else:
        raise HTTPException(status_code=403)