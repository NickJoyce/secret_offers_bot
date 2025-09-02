from app.database.conn import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession
from typing import Annotated
from fastapi import Header, HTTPException, Request
import json


async def get_body(request: Request):
    body = await request.body()
    return json.loads(body)

# verify token passed in header parameter Authorization
async def verify_token(authorization: Annotated[str, Header()] = None):
    if authorization != 'SOME_TOKEN':
        raise HTTPException(status_code=403, detail="Forbidden")

# async database session
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# async http session
async def get_http_session() -> ClientSession:
    async with ClientSession() as session:
        yield session