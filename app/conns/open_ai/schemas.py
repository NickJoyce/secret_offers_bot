from typing import Optional, List, Iterable
from pydantic import BaseModel, Field
from datetime import datetime

class CustomBaseModel(BaseModel):
    @classmethod
    def from_list(cls, data: Iterable):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), data)})



class Cost(BaseModel):
    input: float = Field(..., title='Цена за 1 млн исходящих токенов')
    cached_input: float = Field(..., title='Цена за 1 млн кешированных исходящих токенов')
    output: float = Field(..., title='Цена за 1 млн входящих токенов')


class Model(BaseModel):
    name: str = Field(..., title='Имя модели')
    short_name : str = Field(..., title='Короткое имя модели')
    cost: Cost


