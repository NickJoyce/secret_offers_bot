#!/usr/bin/env python3
import base64
import json
import re
from datetime import datetime

def decode_string(encoded_string):
    """
    Декодирует строку в человекочитаемый вид
    """
    print(f"Исходная строка: {encoded_string}")
    print("-" * 50)
    
    # Разбиваем строку на части
    # Формат: [ID][TIMESTAMP][RANDOM][BASE64_DATA]
    
    # Извлекаем ID (первые цифры)
    id_match = re.match(r'^(\d+)', encoded_string)
    if id_match:
        user_id = id_match.group(1)
        print(f"ID пользователя: {user_id}")
        remaining = encoded_string[len(user_id):]
    else:
        print("Не удалось извлечь ID")
        remaining = encoded_string
    
    # Извлекаем timestamp (8 цифр после ID)
    timestamp_match = re.match(r'^(\d{8})', remaining)
    if timestamp_match:
        timestamp_str = timestamp_match.group(1)
        try:
            # Пытаемся преобразовать в дату
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d')
            print(f"Дата: {timestamp.strftime('%d.%m.%Y')}")
        except ValueError:
            print(f"Timestamp: {timestamp_str}")
        remaining = remaining[8:]
    else:
        print("Не удалось извлечь timestamp")
    
    # Извлекаем случайную часть (до первого дефиса)
    if '-' in remaining:
        random_part, base64_part = remaining.split('-', 1)
        print(f"Случайная часть: {random_part}")
        print(f"Base64 часть: {base64_part}")
        
        # Пытаемся декодировать base64
        try:
            decoded_bytes = base64.b64decode(base64_part)
            print(f"Декодированные байты: {decoded_bytes}")
            
            # Пытаемся интерпретировать как JSON
            try:
                decoded_json = json.loads(decoded_bytes.decode('utf-8'))
                print("Декодированный JSON:")
                print(json.dumps(decoded_json, indent=2, ensure_ascii=False))
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Пытаемся интерпретировать как текст
                try:
                    decoded_text = decoded_bytes.decode('utf-8')
                    print(f"Декодированный текст: {decoded_text}")
                except UnicodeDecodeError:
                    print(f"Декодированные байты (hex): {decoded_bytes.hex()}")
                    
        except Exception as e:
            print(f"Ошибка декодирования base64: {e}")
    else:
        print(f"Оставшаяся часть: {remaining}")

if __name__ == "__main__":
    # Ваша строка
    encoded_string = "0108027281101631215gVjLruMq9S-<9100BE92YvJc9bbSguRaesv7jBHNn7q4lH5j68OMbfSIzO6DvkySCZC65pH4Z+P3RWhoNJGE9jIB9f1TddUqiF4KjkgYuA=="
    
    decode_string(encoded_string)
