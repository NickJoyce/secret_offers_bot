from app.database.conn import AsyncSessionLocal
from app.database.conn import SyncSession
from app.database.models.tg_bot import DeeplinkRequest
from sqlalchemy import select, update, delete, insert
import json



async def aget_deeplink_request_by_invite_link(invite_link: str) -> DeeplinkRequest:
    async with AsyncSessionLocal() as session:
        deeplink_request = await session.scalar(select(DeeplinkRequest).where(DeeplinkRequest.invite_link == invite_link))
        return deeplink_request




async def acreate_deeplink_request(item: dict) -> DeeplinkRequest:
    async with AsyncSessionLocal() as session:
        stmt = insert(DeeplinkRequest).values(**item).returning(DeeplinkRequest)
        deeplink_request = await session.scalar(stmt)
        await session.commit()
        return deeplink_request
    
async def aupdate_deeplink_request(deeplink_request_id: int, update_data: dict):
    """
    Обновляет запрос по диплинку.
    """
    async with AsyncSessionLocal.begin() as session:
        stmt = update(DeeplinkRequest).where(DeeplinkRequest.id == deeplink_request_id).values(**update_data)
        await session.execute(stmt)    
    
    
    
def add_step_to_deeplink_request(id_: int, step: str):
    with SyncSession() as session:
        deeplink_request = session.get(DeeplinkRequest, id_)
        if deeplink_request:
            registration_steps = json.loads(deeplink_request.registration_steps)
            registration_steps['data'].append(step)
            deeplink_request.registration_steps = json.dumps(registration_steps)
            session.commit()
            
  
            

        
    
        
        
        
        # # 1. Создаем экземпляр модели из словаря
        # new_request = DeeplinkRequest(**item)
        
        # # 2. Добавляем в сессию
        # session.add(new_request)
        
        # # 3. Фиксируем изменения в БД
        # await session.commit()
        
        # # 4. Обновляем объект, чтобы подтянуть ID и другие поля, созданные БД
        # await session.refresh(new_request)
        
        # return new_request


def create_deeplink_request(items: list[dict]):
    with SyncSession.begin() as session:
        session.execute(insert(DeeplinkRequest), items)

        
        
