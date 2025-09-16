import random
import string
from app.database.queries.promocodes import get_promocode_by_value




def generate_promocode(length):
    characters = string.ascii_uppercase + string.digits  
    promocode = ''.join(random.choices(characters, k=length))



async def get_unique_promocode(length):
    # генерируем промокод проверяем на уникальность
    max_attempts = 100
    attempts = 0
    while attempts < max_attempts:
        # генерируем промокод
        promocode = generate_promocode(length=10)
        # проверяем есть ли промокод в базе
        existing = await get_promocode_by_value(promocode)
        logger.info(f"existing: {existing}")
        # если промокода нет в базе, то выходим из цикла
        if not existing:
            break
        # если промокод есть в базе, то пробуем снова
        else:
            attempts += 1
            promocode = None
            continue
    return promocode








if __name__ == "__main__":
    print(generate_promocode(length=10))