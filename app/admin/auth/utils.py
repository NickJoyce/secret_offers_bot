import hashlib
import random
import string
from sqlalchemy import select
from app.admin.auth.schemas import UserCreate
from app.admin.auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 100_000
        )
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_email(email: str, session: AsyncSession):
    statement = select(User).filter_by(email=email)
    return await session.scalar(statement)


async def create_user_instance(user: UserCreate, session: AsyncSession):
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    user_instance = User(email=user.email,
                         hashed_password=f"{salt}${hashed_password}",
                         config=jsonable_encoder(user.config))
    session.add(user_instance)
    await session.commit()
    await session.refresh(user_instance)
    return user_instance
