import uvicorn
from app.routers import state
from app.routers.tg_bot import webhook
from app.routers.talk_me import webhooks
from fastapi import FastAPI, Request
import logging.config
from settings import LOGGING, ADMIN_SECRET, BASE_WEBHOOK_URL, WEBHOOK_PATH, WEBHOOK_SECRET
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import traceback
from starlette.middleware.sessions import SessionMiddleware
from app.admin.admin import Admin
from app.database.conn import async_engine
from app.admin.auth.provider import MyAuthProvider
from starlette_admin.i18n import I18nConfig
from starlette.middleware import Middleware
from app.database.models.test import Test
from app.admin.views.test_views import TestView
from app.database.models.tg_bot import TgClient, TgManager, Newsletter, Assignment, GreetingOffer, TalkMeMessageFromClient, ChannelPost, Promocode, BlackList
from app.admin.views.tg_bot import TgClientView, TgManagerView, TgNewsletterView, AssignmentView, MyCustomView, GreetingOfferView, TalkMeMessageFromClientView, ChannelPostView, PromocodeView, BlackListView
from app.admin.auth import auth_router
from app.bot.main import bot, dp, start_bot, stop_bot
from contextlib import asynccontextmanager


from app.bot.modules.handlers.registration2 import router as reg_router
from app.bot.modules.handlers.managers import router as manager_router


from app.bot.modules.handlers.clients import router as client_router
from app.bot.modules.handlers.channels import router as channel_router
from app.bot.modules.handlers.chats import router as chat_router

from starlette_admin.views import Link
from settings.base import TEMPLATES_DIR, IS_BLACK_LIST
from jinja2 import FileSystemLoader
from fastapi.templating import Jinja2Templates
from starlette_admin.views import CustomView
import os
import time
from app.bot.modules.middlewares.general import BlackListMiddleware




# logging init
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    dp.include_router(reg_router)
    dp.include_router(manager_router)
    dp.include_router(client_router)
    dp.include_router(channel_router)
    dp.include_router(chat_router)
    
    # Black List Middleware
    if IS_BLACK_LIST:
        dp.message.middleware(BlackListMiddleware())

    
    await start_bot()
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", 
                          secret_token=WEBHOOK_SECRET, 
                          allowed_updates=["message", "callback_query", "channel_post", "chat_member"],
                          drop_pending_updates=True)
    logging.info(f"Webhook set to {BASE_WEBHOOK_URL}{WEBHOOK_PATH}")
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logging.info("Webhook deleted")



app = FastAPI(lifespan=lifespan, title='tg bot', docs_url=None)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next, ):
    try:
        return await call_next(request)
    except Exception as exc:
        # логируем исключение
        logger.error(f"{traceback.format_exc()}")
        return JSONResponse(status_code=500, content={'reason': 'Internal server error'})


    
# Add static
app.mount("/static", StaticFiles(directory="static", check_dir=False), name="static")




# Create admin
admin = Admin(
    engine=async_engine,
    title="Admin panel",
    base_url="/admin",
    route_name="admin",
    statics_dir=f"static",
    templates_dir=f"{TEMPLATES_DIR}/admin",
    auth_provider=MyAuthProvider(),
    i18n_config=I18nConfig(default_locale="ru"),
    middlewares=[Middleware(SessionMiddleware, secret_key=ADMIN_SECRET),],
    debug=os.getenv('ENV_TYPE') == 'dev',  # Debug только в dev режиме
)




# Add views
# admin.add_view(TestView(Test))
admin.add_view(ChannelPostView(ChannelPost, identity="channel_post"))
admin.add_view(PromocodeView(Promocode, identity="promocode"))
admin.add_view(TgClientView(TgClient, identity="tg_client"))
admin.add_view(BlackListView(BlackList, identity="black_list"))

admin.add_view(TgManagerView(TgManager, identity="tg_manager"))
admin.add_view(TgNewsletterView(Newsletter, identity="tg_newsletter"))
admin.add_view(GreetingOfferView(GreetingOffer, identity="greeting_offer"))
admin.add_view(TalkMeMessageFromClientView(TalkMeMessageFromClient, identity="talk_me_message_from_client"))
admin.add_view(AssignmentView(Assignment, identity="assignment"))
admin.add_view(MyCustomView(label="Кастомная страница", 
                            icon="fa fa-star",
                            path="/my-page",
                            name="Кастомная страница",
                            template_path=f"custom/my-page.html",
                            methods=["GET", "POST"]
                            ))
admin.add_view(Link(label="Home Page", icon="fa fa-link", url="/admin"))





# Mount admin to app
admin.mount_to(app)


# Add routers
app.include_router(state.router)
app.include_router(webhook.router)
app.include_router(webhooks.router)


# Add admin routers
app.include_router(auth_router)







if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8432, reload=True)