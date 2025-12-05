from starlette_admin.contrib.sqla import ModelView
from starlette_admin.fields import StringField, BooleanField, IntegerField, DateTimeField, DecimalField, HasOne, HasMany, FileField, ImageField, TextAreaField
from starlette_admin.fields import FloatField, JSONField
from app.database.models.tg_bot import TgClient, TgManager, Newsletter, Assignment, ChannelPost, Promocode, BlackList, DeepLink
from fastapi import Request
from typing import Any
from fastapi.templating import Jinja2Templates
from settings.base import TEMPLATES_DIR
from starlette_admin.views import CustomView, BaseView
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.responses import Response
from app.database.queries.tg_clients import get_clients
from settings.base import BASE_DIR
import logging
from starlette.requests import Request
from app.database.conn import AsyncSessionLocal

logger = logging.getLogger(__name__)





# templates = Jinja2Templates(directory=f'{TEMPLATES_DIR}/admin/')


class MyCustomField(StringField):
    async def parse_obj(self, request: Request, obj: Any) -> Any:
        return f"{obj.surname} {obj.name}"  # Returns the full name of the user

class CityField(StringField):
    async def parse_obj(self, request: Request, obj: Any) -> Any:
        return f"{obj.city}" if obj.city else "-"  # Returns the full name of the user

  
class TgClientView(ModelView):
    label = 'Клиенты'
    name = 'Клиент'
    fields = [
        IntegerField("id", label="id"), 
        DateTimeField("created_at", label="Дата создания"),
        DateTimeField("updated_at", label="Дата обновления"),
        IntegerField("tg_id", label="id (tg)"), 
        StringField("reg_name", label="Имя (рег.)"),
        StringField("reg_phone", label="Телефон (рег.)"),
        StringField("tg_username", label="Имя пользователя (tg)"),
        StringField("tg_first_name", label="Имя (tg)"),
        StringField("tg_last_name", label="Фамилия (tg)"),
        BooleanField("is_active", label="Активен ли клиент"),
        CityField("city", label="Город"),
        IntegerField("talk_me_search_id", label="Уникальный идентификатор из Cookies (talk-me)"),
        StringField("talk_me_client_id", label="Уникальный идентификатор посетителя для поиска (talk-me)"),
        HasMany("promocodes", label="Промокоды", identity='promocode')
        ]
    exclude_fields_from_list = ["id", "updated_at", "talk_me_search_id", "talk_me_client_id"]
    exclude_fields_from_create = ["id", "created_at", "updated_at", "talk_me_search_id", "talk_me_client_id"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at", "talk_me_search_id", "talk_me_client_id"]
    exclude_fields_from_detail = []
    # Ограничиваем количество записей на странице
    list_per_page = 50  
    # Добавляем поиск
    searchable_fields = ["tg_id", "reg_name", "reg_phone",  "tg_username", "tg_first_name", "tg_last_name"]  
    # Добавляем сортировку
    sortable_fields = ["tg_id", "reg_name", "reg_phone",  "tg_username", "tg_first_name", "tg_last_name"]  
    
    # Оптимизация: показываем только активных пользователей по умолчанию
    def get_list_query(self, request: Request):
        query = super().get_list_query(request)
        # Можно добавить фильтр по умолчанию если нужно
        return query
    
class PromocodeView(ModelView):
    label = 'Промокоды'
    name = 'Промокод'
    fields = [
        IntegerField("id", label="id"), 
        DateTimeField("created_at", label="Дата создания"),
        DateTimeField("updated_at", label="Дата обновления"),
        IntegerField("client_id", label="ID клиента"),
        StringField("value", label="Промокод"),
        StringField("link", label="Ссылка на закрытый канал"),
        DateTimeField("expire_date", label="Дата истечения промокода (ссылки на закрытый канал)"),
        IntegerField("subscriber_tg_id", label="tg id пользователя который подписался на закрытый канал"),
        DateTimeField("date_of_join", label="Дата присоеденения к закрытому каналу"),
        HasMany("tg_client", label="Клиент", identity='tg_client', multiple=False)
    ]
    
    exclude_fields_from_list = ["id", "created_at", "updated_at", "subscriber_tg_id", "date_of_join", "tg_client"]
    exclude_fields_from_create = ["id", "created_at", "updated_at", "subscriber_tg_id", "date_of_join"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at", "subscriber_tg_id", "date_of_join", "tg_client"]
    exclude_fields_from_detail = ["tg_client", "tg_client"]
    # Ограничиваем количество записей на странице
    
    
    
    
    
    
    
    
class TgManagerView(ModelView):
    label = 'Менежеры'
    name = 'Менеджер'
    fields = [
        IntegerField("id", label="id"), 
        DateTimeField("created_at", label="Дата создания"),
        DateTimeField("updated_at", label="Дата обновления"),
        IntegerField("tg_id", label="id (tg)"), 
        StringField("first_name", label="Имя"),
        StringField("last_name", label="Фамилия"),
        BooleanField("is_active", label="Активен ли менеджер")
        ]
    exclude_fields_from_list = ["id", "updated_at"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]
    exclude_fields_from_detail = []
    # Ограничиваем количество записей на странице
    list_per_page = 50  
    # Добавляем поиск
    searchable_fields = ["tg_id", "first_name", "last_name"]  
    # Добавляем сортировку
    sortable_fields = ["tg_id", "first_name", "last_name"]  


class TgNewsletterView(ModelView):
    label = 'Рассылки'
    name = 'Рассылка'
    fields = [
        IntegerField("id", label="id"), 
        DateTimeField("created_at", label="Дата создания"),
        DateTimeField("updated_at", label="Дата обновления"),
        StringField("name", label="Имя"),
        TextAreaField("text", 
                      label="Текст рассылки"),
        BooleanField("is_active", label="Доступность рассылки"),
        FileField("files", label="Файлы", multiple=True),
        ImageField("images", label="Изображения", multiple=True),
        FileField("tg_ids", label="Файл эксель с id пользователей, котоорым будет отправлена рассылка"),
        HasMany("clients", label="Клиенты", identity='tg_client')
        ]
    
    
    exclude_fields_from_list = ["id", "updated_at", "files", "images", "tg_ids"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]
    exclude_fields_from_detail = []
    # Ограничиваем количество записей на странице
    list_per_page = 50  
    # Добавляем поиск
    searchable_fields = ["tg_id", "name"]  
    # Добавляем сортировку
    sortable_fields = ["tg_id", "name"] 
    
    
    
class AssignmentView(ModelView):
    label = "Рассылки-Клиенты (m2m)"
    name = "Рассылка-Клиент (m2m)"
    fields = [
        IntegerField(
            name="id",
            label="ID",
            help_text="ID of the record.",
            read_only=True,
        ),
        IntegerField(
            name="tgclient_id",
            label="Client ID",
            read_only=True,
        ),
        IntegerField(
            name="newsletter_id",
            label="Newsletter ID",
            read_only=True,
        ),
    ]



class GreetingOfferView(ModelView):
    label = 'Привественные предложения'
    name = 'Привественное предложение'
    fields = [
        IntegerField("id", label="id"), 
        StringField("name", label="Имя"),
        FloatField("old_price", label="Старая цена"),
        FloatField("new_price", label="Новая цена"),
        StringField("equipment", label="Аппараты"),
        BooleanField("is_active", label="Доступность предложения"),
        ]
    
    
    exclude_fields_from_list = ["id"]
    exclude_fields_from_create = ["id"]
    exclude_fields_from_edit = ["id"]
    exclude_fields_from_detail = []
    # Ограничиваем количество записей на странице
    list_per_page = 50  
    # Добавляем поиск
    searchable_fields = ["tg_id", "name"]  
    # Добавляем сортировку
    sortable_fields = ["tg_id", "name"] 



class TalkMeMessageFromClientView(ModelView):
    label = 'Сообщения от клиентов (webhook talk-me)'
    name = 'Сообщение от клиента (webhook talk-me)'
    fields = [
        IntegerField("id", label="id"),
        DateTimeField("created_at", label="Дата создания"),
        IntegerField("tg_id", label="ID пользователя в Telegram"),
        IntegerField("search_id", label="Уникальный идентификатор из Cookies (talk-me)"),
        StringField("client_id", label="Уникальный идентификатор посетителя для поиска (talk-me)"),
        JSONField("webhook_data", label="Данные из talk-me при возникновении события Новое сообщение от клиента")
    ]

    exclude_fields_from_list = ["id", "created_at", "webhook_data"]
    exclude_fields_from_create = ["id", "created_at"]
    exclude_fields_from_edit = ["id", "created_at"]
    exclude_fields_from_detail = []
    # Ограничиваем количество записей на странице
    list_per_page = 50  
    # Добавляем поиск
    searchable_fields = ["tg_id", "search_id"]  
    # Добавляем сортировку
    sortable_fields = ["tg_id", "search_id"] 



class MyCustomView(CustomView):
    async def render(self, request: Request, templates: Jinja2Templates) -> Response:
        tg_clients = await get_clients()
        if request.method == "POST":
            form = await request.form()
            excel_file = form.get("excelFile")
            if excel_file:
                # Сохраняем файл или обрабатываем его
                contents = await excel_file.read()
                # Например, сохраняем на диск:
                with open(f"{BASE_DIR}/{excel_file.filename}", "wb") as f:
                    f.write(contents)
                # Можно добавить обработку Excel-файла здесь
                logger.info(f"Файл {excel_file.filename} успешно загружен")
            
        return templates.TemplateResponse(
            request,
            name="custom/my-page.html",
            context={"tg_clients": tg_clients},

        )

class ChannelPostView(ModelView):
    label = 'Посты в канале'
    name = 'Пост в канале'
    fields = [
        IntegerField("id", label="id"),
        DateTimeField("created_at", label="Дата создания"),
        ImageField("photo", label="Фото"),
        TextAreaField("caption", label="Подпись под картинкой", rows=12),
        StringField("chat_id", label="ID чата"),
        IntegerField("message_id", label="ID сообщения"),
        DateTimeField("buttons_expiration", label="Дата истечения срока действия кнопок"),
        BooleanField("is_buttons_deleted", label="Флаг удаления кнопок"),
    ]
    exclude_fields_from_list = ["id", "caption", "photo"]
    exclude_fields_from_create = ["id", "created_at", "chat_id", "message_id", "is_buttons_deleted"]
    exclude_fields_from_edit = ["id", "created_at", "chat_id", "message_id", "is_buttons_deleted"]
    
class BlackListView(ModelView):
    label = 'Черный список'
    name = 'Черный список'
    fields = [
        IntegerField("id", label="id"),
        DateTimeField("created_at", label="Дата создания"),
        DateTimeField("updated_at", label="Дата обновления"),
        StringField("name", label="Призвольное имя"),
        IntegerField("tg_id", label="ID пользователя в Telegram"),
        StringField("tg_username", label="Имя пользователя в Telegram"),
        TextAreaField("reason", label="Причина добавления в черный список"),
        BooleanField("is_active", label="Добавлен в черный список?")
    ]
    
    exclude_fields_from_list = ["id", "created_at", "updated_at"]
    exclude_fields_from_create = ["id", "created_at", "updated_at", "is_active"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]
    
class DeepLinkView(ModelView):
    label = 'Deep Links'
    name = 'Deep Link'
    fields = [
        IntegerField("id", label="id"),
        DateTimeField("created_at", label="Дата создания"),
        DateTimeField("updated_at", label="Дата обновления"),
        StringField("name", label="Имя"),
        JSONField("payload", label="Payload"),
        StringField("link", label="Ссылка"),
    ]
    exclude_fields_from_list = ["id", "created_at", "updated_at", "payload"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]
    exclude_fields_from_detail = []
    # Ограничиваем количество записей на странице
    list_per_page = 50  
    # Добавляем поиск
    searchable_fields = ["name", "link"]  
    # Добавляем сортировку
    sortable_fields = ["name", "link"] 
    
    

    async def after_create(self, request, obj):
        session = request.state.session
        obj.link = f"https://t.me/secret_offers_bot?start={obj.id}"
        await session.commit()
        return await super().after_create(request, obj)


