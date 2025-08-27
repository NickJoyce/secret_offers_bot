import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, index=True, comment='Email')
    hashed_password = Column(String(), comment='Хэш пароля')
    config = Column(JSONB, comment='Конфигурация пользователя')
    is_active = Column(Boolean,
                       server_default=sqlalchemy.sql.expression.true(),
                       nullable=False,
                       comment="Активен")

    def __str__(self):
        return f"User({self.id}, {self.email}, {self.config}, {self.is_active})"