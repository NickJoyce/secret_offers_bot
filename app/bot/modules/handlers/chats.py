from aiogram import Router
from aiogram.types import Message
import logging
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.types import ChatJoinRequest, ChatMemberUpdated
from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, KICKED, LEFT, RESTRICTED, MEMBER, ADMINISTRATOR, CREATOR, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated


logger = logging.getLogger(__name__)


router = Router()


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def admin_promoted(event: ChatMemberUpdated):
    logger.info(event, 'ADD NEW')










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