# Решение проблем с подключением к pgbouncer извне

## Основные причины "password authentication failed" при внешнем подключении

### 1. **Проблема с auth_query вместо auth_file**

Если в `pgbouncer.ini` используется `auth_query`, pgbouncer запрашивает пароли из PostgreSQL. 
Проверьте, что в конфиге нет строки `auth_query`.

**Решение:** Используйте `auth_file`:
```ini
auth_type = md5  # или scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
# НЕ используйте auth_query для внешних подключений
```

### 2. **База данных не указана в секции [databases]**

Если используется `* = host=localhost port=5432`, это должно работать для всех баз.
Но лучше указать явно:

```ini
[databases]
secret_offers_bot_db = host=localhost port=5432 dbname=secret_offers_bot_db
```

### 3. **Проблема с версией pgbouncer и SCRAM**

Старые версии pgbouncer (< 1.17) не поддерживают SCRAM-SHA-256.

**Проверка версии:**
```bash
pgbouncer -V
```

**Решение:** 
- Обновите pgbouncer до версии 1.17+
- Или используйте MD5 вместо SCRAM

### 4. **pgbouncer не может подключиться к PostgreSQL**

Если pgbouncer сам не может подключиться к PostgreSQL, внешние клиенты тоже не смогут.

**Проверка:**
```bash
# Проверить логи pgbouncer
sudo tail -f /var/log/postgresql/pgbouncer.log

# Проверить, может ли pgbouncer подключиться
psql -h localhost -p 5432 -U secret_offers_bot_admin -d secret_offers_bot_db
```

**Решение:** В `pg_hba.conf` должна быть строка:
```
host    all             all             127.0.0.1/32          md5
```

### 5. **Проблема с форматом userlist.txt**

**Для MD5:**
```
"secret_offers_bot_admin" "md57976f0b67c8963ca8cba7c894e4fb1fb"
```

**Для SCRAM:**
```
"secret_offers_bot_admin" "SCRAM-SHA-256$4096:...$...:..."
```

**Важно:**
- Кавычки обязательны
- Для MD5: префикс `md5` перед хешем
- Для SCRAM: полный хеш из PostgreSQL (получить через `\password` с `--echo-hidden`)

### 6. **Firewall блокирует порт**

**Проверка:**
```bash
sudo ufw status
sudo iptables -L -n | grep 6432
```

**Решение:**
```bash
sudo ufw allow 6432/tcp
# или
sudo iptables -A INPUT -p tcp --dport 6432 -j ACCEPT
```

### 7. **pgbouncer слушает только на localhost**

**Проверка:**
```bash
sudo netstat -tlnp | grep 6432
# или
sudo ss -tlnp | grep 6432
```

Должно быть: `0.0.0.0:6432` или `:::6432`
Если только `127.0.0.1:6432` - это проблема.

**Решение:** В `pgbouncer.ini`:
```ini
listen_addr = *
listen_port = 6432
```

### 8. **Несоответствие auth_type в pgbouncer и pg_hba.conf**

**Проблема:** Если PostgreSQL использует `scram-sha-256`, а pgbouncer настроен на `md5`, или наоборот.

**Решение:** Привести в соответствие:
- В `pgbouncer.ini`: `auth_type = scram-sha-256`
- В `pg_hba.conf`: `host all all 127.0.0.1/32 scram-sha-256`
- В `userlist.txt`: формат SCRAM

### 9. **Проблема с правами доступа к файлам**

**Проверка:**
```bash
sudo ls -la /etc/pgbouncer/userlist.txt
sudo ls -la /etc/pgbouncer/pgbouncer.ini
```

**Решение:**
```bash
sudo chown postgres:postgres /etc/pgbouncer/userlist.txt
sudo chmod 600 /etc/pgbouncer/userlist.txt
```

### 10. **Проблема с pool_mode**

Если `pool_mode = session`, некоторые клиенты могут не работать правильно.

**Решение:** Используйте `pool_mode = transaction`:
```ini
pool_mode = transaction
```

## Пошаговая диагностика

1. Запустите скрипт диагностики:
   ```bash
   ./diagnose_pgbouncer.sh
   ```

2. Проверьте логи в реальном времени:
   ```bash
   sudo tail -f /var/log/postgresql/pgbouncer.log
   ```
   Затем попробуйте подключиться извне.

3. Проверьте, что pgbouncer может подключиться к PostgreSQL:
   ```bash
   psql -h localhost -p 5432 -U secret_offers_bot_admin -d secret_offers_bot_db
   ```

4. Проверьте подключение через pgbouncer локально:
   ```bash
   psql -h localhost -p 6432 -U secret_offers_bot_admin -d secret_offers_bot_db
   ```

5. Проверьте подключение извне:
   ```bash
   psql -h 5.129.242.211 -p 6432 -U secret_offers_bot_admin -d secret_offers_bot_db
   ```

## Быстрое решение

Если ничего не помогает, попробуйте:

1. Перезапустить pgbouncer:
   ```bash
   sudo systemctl restart pgbouncer
   ```

2. Перезагрузить PostgreSQL:
   ```bash
   sudo systemctl reload postgresql
   ```

3. Проверить, что все службы запущены:
   ```bash
   sudo systemctl status pgbouncer
   sudo systemctl status postgresql
   ```

4. Временно включить подробное логирование в pgbouncer:
   ```ini
   log_connections = 1
   log_disconnections = 1
   log_pooler_errors = 1
   ```



