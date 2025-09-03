#!/usr/bin/env python3
import base64
import json
import re
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import binascii

def analyze_string(encoded_string):
    """
    Анализирует строку и пытается декодировать её различными способами
    """
    print("=" * 60)
    print("АНАЛИЗ ЗАШИФРОВАННОЙ СТРОКИ")
    print("=" * 60)
    print(f"Исходная строка: {encoded_string}")
    print(f"Длина строки: {len(encoded_string)} символов")
    print("-" * 60)
    
    # 1. Разбор структуры
    print("1. СТРУКТУРНЫЙ АНАЛИЗ:")
    
    # ID пользователя (первые цифры)
    id_match = re.match(r'^(\d+)', encoded_string)
    if id_match:
        user_id = id_match.group(1)
        print(f"   ID пользователя: {user_id}")
        remaining = encoded_string[len(user_id):]
    else:
        print("   ID пользователя: не найден")
        remaining = encoded_string
    
    # Поиск разделителей
    if '-' in remaining:
        parts = remaining.split('-')
        print(f"   Найдено {len(parts)} частей, разделенных дефисом")
        
        for i, part in enumerate(parts):
            print(f"   Часть {i+1}: {part}")
            
        # Последняя часть - это base64
        if len(parts) >= 2:
            base64_part = parts[-1]
            print(f"   Base64 часть: {base64_part}")
            
            # 2. Декодирование base64
            print("\n2. ДЕКОДИРОВАНИЕ BASE64:")
            try:
                decoded_bytes = base64.b64decode(base64_part)
                print(f"   Декодированные байты: {decoded_bytes}")
                print(f"   Размер: {len(decoded_bytes)} байт")
                print(f"   Hex представление: {decoded_bytes.hex()}")
                
                # 3. Анализ декодированных данных
                print("\n3. АНАЛИЗ ДЕКОДИРОВАННЫХ ДАННЫХ:")
                
                # Пытаемся интерпретировать как JSON
                try:
                    decoded_json = json.loads(decoded_bytes.decode('utf-8'))
                    print("   JSON данные:")
                    print(json.dumps(decoded_json, indent=4, ensure_ascii=False))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    print("   Не является валидным JSON")
                
                # Пытаемся интерпретировать как текст
                try:
                    decoded_text = decoded_bytes.decode('utf-8')
                    print(f"   Текстовые данные: {decoded_text}")
                except UnicodeDecodeError:
                    print("   Не является валидным UTF-8 текстом")
                
                # Анализ как бинарных данных
                print(f"   Первые 16 байт: {decoded_bytes[:16]}")
                print(f"   Последние 16 байт: {decoded_bytes[-16:]}")
                
                # Проверка на известные форматы
                if decoded_bytes.startswith(b'\x89PNG'):
                    print("   Это PNG изображение")
                elif decoded_bytes.startswith(b'\xff\xd8\xff'):
                    print("   Это JPEG изображение")
                elif decoded_bytes.startswith(b'PK'):
                    print("   Это ZIP архив")
                elif decoded_bytes.startswith(b'\x1f\x8b'):
                    print("   Это GZIP архив")
                else:
                    print("   Неизвестный формат данных")
                
            except Exception as e:
                print(f"   Ошибка декодирования base64: {e}")
    
    # 4. Дополнительный анализ
    print("\n4. ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ:")
    
    # Проверка на хеш
    if len(encoded_string) == 64:
        print("   Возможно, это SHA-256 хеш")
    elif len(encoded_string) == 40:
        print("   Возможно, это SHA-1 хеш")
    elif len(encoded_string) == 32:
        print("   Возможно, это MD5 хеш")
    
    # Проверка на UUID
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if re.match(uuid_pattern, encoded_string.lower()):
        print("   Это UUID")
    
    # 5. Попытка дешифрования
    print("\n5. ПОПЫТКА ДЕШИФРОВАНИЯ:")
    
    # Попытка с различными ключами (если это Fernet)
    if len(decoded_bytes) > 32:  # Минимальный размер для Fernet
        print("   Попытка дешифрования как Fernet...")
        # Здесь можно попробовать известные ключи или методы
    
    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 60)

if __name__ == "__main__":
    # Ваша строка
    encoded_string = "0108027281101631215gVjLruMq9S-<9100BE92YvJc9bbSguRaesv7jBHNn7q4lH5j68OMbfSIzO6DvkySCZC65pH4Z+P3RWhoNJGE9jIB9f1TddUqiF4KjkgYuA=="
    
    analyze_string(encoded_string)
