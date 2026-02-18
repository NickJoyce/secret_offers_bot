import logging.config
from datetime import datetime, timezone, date
from enum import Enum
from app.database.queries.tg_deeplink_requests import acreate_deeplink_request
import json





logger = logging.getLogger(__name__)


class ParseModes:
    MARKDOWN_V2 = 'MarkdownV2'
    MARKDOWN = 'Markdown'
    HTML = 'HTML'
    

def escape_markdown_v2(text: str) -> str:
    """ Экранирует специальные символы в строке для использования в режиме ParseMode.MARKDOWN_V2."""
    reserved_chars = '}{[]()>#+=.:,!@/_-'
    for char in reserved_chars:
        text = text.replace(char, f'\\{char}')
    return text




class RegistrationSteps(Enum):
    def __new__(cls, code: str, description: str):
        obj = object.__new__(cls)
        obj._value_ = code          
        obj.description = description
        return obj
    
    START_COMMAND_RECEIVED = 'START_COMMAND_RECEIVED', 'Выполена команда /start'
    NAME_INPUT = 'NAME_INPUT_RECEIVED', 'Имя получено'
    PHONE_INPUT = 'PHONE_INPUT_RECEIVED', 'Номер телефона получен'
    CITY_FIRST_LETTER_RECEIVED = 'CITY_FIRST_LETTER_RECEIVED', 'Первая буква города выбрана'
    CITY_RECEIVED = 'CITY_RECEIVED', 'Город выбран'
    WRITTEN_TO_DB = 'WRITTEN_TO_DB', 'Данные записаны в базу'
    LINK_SENT = 'LINK_SENT', 'Ссылка отправлена'
    SUBSCRIBED_TO_CHANNEL = 'SUBSCRIBED_TO_CHANNEL', 'Подписан на канал'


async def create_deeplink_request(deeplink_id, tg_id, received_at, registration_steps: dict, is_registred: bool):
    item = {
            "deeplink_id": deeplink_id,
            "tg_id": tg_id,
            "received_at": received_at,
            "registration_steps": registration_steps,
            "is_registred": is_registred
            }
    return await acreate_deeplink_request(item=item)   

    

    
CITIES = [
    "Архангельск",
    "Астрахань",
    "Балашиха",
    "Барнаул",
    "Белгород",
    "Брянск",
    "Великий Новгород",
    "Владивосток",
    "Владимир",
    "Волгоград",
    "Вологда",
    "Воронеж",
    "Геленджик",
    "Екатеринбург",
    "Иваново",
    "Ижевск",
    "Иркутск",
    "Казань",
    "Калининград",
    "Калуга",
    "Кемерово",
    "Киров",
    "Кострома",
    "Краснодар",
    "Красноярск",
    "Курган",
    "Курск",
    "Липецк",
    "Люберцы",
    "Москва",
    "Мурманск",
    "Набережные Челны",
    "Нефтеюганск",
    "Нижневартовск",
    "Нижний Новгород",
    "Нижний Тагил",
    "Новороссийск",
    "Новосибирск",
    "Обнинск",
    "Одинцово",
    "Омск",
    "Орел",
    "Оренбург",
    "Орск",
    "Пенза",
    "Пермь",
    "Петрозаводск",
    "Подольск",
    "Псков",
    "Ростов-на-Дону",
    "Рязань",
    "Самара",
    "Санкт-Петербург",
    "Саранск",
    "Саратов",
    "Севастополь",
    "Симферополь",
    "Смоленск",
    "Сочи",
    "Ставрополь",
    "Старый Оскол",
    "Стерлитамак",
    "Сургут",
    "Сыктывкар",
    "Таганрог",    
    "Тамбов",
    "Тверь",
    "Тольятти",
    "Томск",
    "Тула",
    "Тюмень",
    "Улан-Удэ",
    "Ульяновск",
    "Уфа",
    "Хабаровск",
    "Ханты-Мансийск",
    "Химки",
    "Чебоксары",
    "Челябинск",
    "Череповец",
    "Чита",
    "Энгельс",
    "Ялта",
    "Ярославль",
    "Нью-Йорк",
]


unique_first_letters = sorted(list(set([city[0].upper() for city in CITIES])))

