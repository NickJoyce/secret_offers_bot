from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Boolean, Float, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from sqlalchemy import func, Column, Table
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum
from typing import List
from sqlalchemy_file import FileField, ImageField
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager
import os
from settings.base import BASE_DIR

# Configure Storage



# os.makedirs("./upload_dir/attachment", 0o777, exist_ok=True)
# container = LocalStorageDriver("./upload_dir").get_container("attachment")
# StorageManager.add_storage("default", container)

os.makedirs(f"{BASE_DIR}/app/uploads/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver(f"{BASE_DIR}/app/uploads").get_container("attachment")
StorageManager.add_storage("default", container)



class Base(AsyncAttrs, DeclarativeBase):
    pass


# tgclients_newsletters = Table(
#     "tgclients_newsletters",
#     Base.metadata,
    
#     Column("tgclient_id", ForeignKey("tg_clients.id")),
#     Column("newsletter_id", ForeignKey("tg_newsletters.id"))
# )








class TgClient(Base):
    __tablename__ = 'tg_clients'

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 nullable=False,
                                                 comment='Дата создания')
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False,
                                                 comment='Дата обновления')
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, comment="ID пользователя в Telegram")
    reg_name: Mapped[str] = mapped_column(String(255), comment="Имя указанное при регистрации")
    reg_phone: Mapped[str] = mapped_column(String(255), comment="Телефон указанный при регистрации")
    tg_username: Mapped[str] = mapped_column(String(255), default="", nullable=True, comment="Имя пользователя в Telegram")
    tg_first_name: Mapped[str] = mapped_column(String(255), default="", nullable=True, comment="Имя (tg)")
    tg_last_name: Mapped[str] = mapped_column(String(255), default="", nullable=True, comment="Фамилия (tg)")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="Флаг активности")
    newsletters = relationship(
       "Newsletter",
       secondary="tgclient_newsletter",
       back_populates="clients"
   )
    
    talk_me_search_id: Mapped[int] = mapped_column(BigInteger, nullable=True,comment="Уникальный идентификатор из Cookies (talk-me)")
    talk_me_client_id: Mapped[str] = mapped_column(String(255), nullable=True, comment="Уникальный идентификатор посетителя для поиска (talk-me)")


    def __str__(self):
        return self.reg_name


class TgManager(Base):
    __tablename__ = 'tg_managers'

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 nullable=False,
                                                 comment='Дата создания')
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False,
                                                 comment='Дата обновления')
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, comment="ID пользователя в Telegram")
    first_name: Mapped[str] = mapped_column(String(255), default="", comment="Имя")
    last_name: Mapped[str] = mapped_column(String(255), default="", comment="Фамилия")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="Флаг активности")


    def __str__(self):
        return self.first_name



class Newsletter(Base):
    __tablename__ = 'tg_newsletters'

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 nullable=False,
                                                 comment='Дата создания')
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False,
                                                 comment='Дата обновления')
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), default="", comment="Имя")
    text: Mapped[str] = mapped_column(String(4096), default="", nullable=True, comment="Текст")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="Флаг активности")
    files: Mapped[FileField] = mapped_column(FileField(multiple=True), nullable=True, comment="Файлы")
    images: Mapped[ImageField] = mapped_column(ImageField(multiple=True), nullable=True, comment="Изображения")
    tg_ids: Mapped[FileField] = mapped_column(FileField, nullable=True, comment="Файл эксель с id пользователей котоорым будет отправлена рассылка")
    clients: Mapped[list[TgClient]] = relationship(
       "TgClient",
       secondary="tgclient_newsletter",
       back_populates="newsletters"
    )

    def __str__(self):
        return self.name


class Assignment(Base):
    __tablename__ = "tgclient_newsletter"
    
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tgclient_id: Mapped[int] = mapped_column(ForeignKey(TgClient.id))
    newsletter_id: Mapped[int] = mapped_column(ForeignKey(Newsletter.id))



class GreetingOffer(Base):
    __tablename__ = "greeting_offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), comment="Имя")
    old_price: Mapped[float] = mapped_column(Float, default=0.00, comment="Старая цена")
    new_price: Mapped[float] = mapped_column(Float, default=0.00, comment="Новая цена")
    equipment: Mapped[str] = mapped_column(String(255), nullable=True, comment="Аппараты")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="Флаг активности")


    def __str__(self):
        return self.name
    
    
    

    
class TalkMeMessageFromClient(Base):
    __tablename__ = "talk_me_messages_from_client"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.timezone('Europe/Moscow', func.now()),
                                                 nullable=False,
                                                 comment='Дата создания')
    tg_id: Mapped[int] = mapped_column(BigInteger, comment="ID пользователя в Telegram", index=True)
    search_id: Mapped[int] = mapped_column(BigInteger, comment="Уникальный идентификатор из Cookies (talk-me)")
    client_id: Mapped[str] = mapped_column(String(255), comment="Уникальный идентификатор посетителя для поиска (talk-me)", index=True)
    webhook_data: Mapped[JSONB] = mapped_column(JSONB, comment="Данные из talk-me при возникновении события Новое сообщение от клиента")
    



class FirstStartMessage(Base):
    __tablename__ = "first_start_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.timezone('Europe/Moscow', func.now()),
                                                 nullable=False,
                                                 comment='Дата создания')
    tg_id: Mapped[int] = mapped_column(BigInteger, comment="ID пользователя в Telegram", unique=True)
    message: Mapped[JSON] = mapped_column(JSON, comment="Первое сообщение /start отпрвленное тг на вебхук")
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True, comment="Флаг отправки в talk-me")
 
    
    
    
class ChannelPost(Base):
    __tablename__ = "channel_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.timezone('Europe/Moscow', func.now()),
                                                 nullable=False,
                                                 comment='Дата создания')
    caption: Mapped[str] = mapped_column(String(1200), comment="Подпись под картинкой")
    photo: Mapped[ImageField] = mapped_column(ImageField(), nullable=True, comment="Фото")
    chat_id: Mapped[str] = mapped_column(String(255), nullable=True, comment="ID чата")
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="ID сообщения")
    buttons_expiration: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата истечения срока действия кнопок")
    
    

