from sqlalchemy import Column,  String, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Test(Base):
    __tablename__ = 'table_test'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False, comment='Дата и время')
    str_field = Column(String(100), nullable=False, comment='строка')