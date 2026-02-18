from aiogram import Router
from aiogram.types import Message
import logging
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.types import ChatJoinRequest, ChatMemberUpdated
from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, KICKED, LEFT, RESTRICTED, MEMBER, ADMINISTRATOR, CREATOR, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated
from app.bot.main import send_message_to_admin
from app.tasks.monitoring import add_step_to_deeplink_request_task
from app.bot.modules.utils import RegistrationSteps
from app.database.queries.tg_deeplink_requests import aget_deeplink_request_by_invite_link

logger = logging.getLogger(__name__)


router = Router()

@router.chat_member()
async def on_chat_member(event: ChatMemberUpdated):
    chat_id = event.chat.id
    user_id = event.from_user.id
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status
    try:
        invite_link = event.invite_link.invite_link
    except AttributeError:
        invite_link = None
        
    if  old_status == 'left' and new_status == 'member':
        if  invite_link:
            # Получим запрос по диплинку по ссылке приглашению
            deeplink_request = await aget_deeplink_request_by_invite_link(invite_link=invite_link)
            if  deeplink_request:
                # Добавим новый шаг в запрос по диплинку
                add_step_to_deeplink_request_task.delay(id_=deeplink_request.id, step=RegistrationSteps.SUBSCRIBED_TO_CHANNEL.value)
                

        
        
    logger.info(f"on_chat_member: chat_id: {chat_id}, user_id: {user_id},  {old_status} -> {new_status}, invite_link: {invite_link}")

    await send_message_to_admin(f"chat_id: {chat_id}\n"
                          f"user_id: {user_id}\n"
                          f"{old_status} -> {new_status}\n"
                          f"invite_link: {invite_link}")
    
    
  





# @router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
# async def admin_promoted(event: ChatMemberUpdated):
#     logger.info(event, 'ADD NEW')










# # Это работает для получения данных пользователя при проходе по ссылке
# @router.chat_join_request()
# async def on_user_leave(update: ChatJoinRequest): 
#     logger.info(update.invite_link.invite_link, 'ССЫЛКА ПО КОТОРОЙ ПРОШЛИ')
#     logger.info(update.invite_link)
    
#     print(update.invite_link)

# # Срабатывает, когда отписывается пользователь
# @router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
# async def on_user_leave(event: ChatMemberUpdated):
#     print(event, 'LEAVE')

# # Срабатывает когда присоединяется новый пользователь
# @router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
# async def on_user_join(event: ChatMemberUpdated):
#     print(event, 'ADD NEW')