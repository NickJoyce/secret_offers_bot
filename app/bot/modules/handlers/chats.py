from aiogram import Router
from aiogram.types import Message
import logging
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.types import ChatJoinRequest, ChatMemberUpdated


logger = logging.getLogger(__name__)


router = Router()






# Это работает для получения данных пользователя при проходе по ссылке
@router.chat_join_request()
async def on_user_leave(update: ChatJoinRequest): 
    print(update.invite_link.invite_link, 'ССЫЛКА ПО КОТОРОЙ ПРОШЛИ')
    print(update.invite_link)

# # Срабатывает, когда отписывается пользователь
# @router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
# async def on_user_leave(event: ChatMemberUpdated):
#     print(event, 'LEAVE')

# # Срабатывает когда присоединяется новый пользователь
# @router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
# async def on_user_join(event: ChatMemberUpdated):
#     print(event, 'ADD NEW')