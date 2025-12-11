#!/bin/bash

echo "=== Диагностика pgbouncer ==="
echo ""

echo "1. Проверка, слушает ли pgbouncer на всех интерфейсах:"
sudo netstat -tlnp 2>/dev/null | grep 6432 || sudo ss -tlnp | grep 6432
echo ""

echo "2. Проверка статуса службы pgbouncer:"
sudo systemctl status pgbouncer --no-pager -l | head -20
echo ""

echo "3. Проверка версии pgbouncer:"
sudo pgbouncer -V 2>&1 || echo "pgbouncer не найден в PATH"
echo ""

echo "4. Проверка синтаксиса конфигурации pgbouncer:"
sudo pgbouncer -C /etc/pgbouncer/pgbouncer.ini 2>&1
echo ""

echo "5. Проверка содержимого userlist.txt (первые 3 строки):"
sudo head -3 /etc/pgbouncer/userlist.txt 2>/dev/null || echo "Файл не найден"
echo ""

echo "6. Проверка последних 20 строк логов pgbouncer:"
sudo tail -20 /var/log/postgresql/pgbouncer.log 2>/dev/null || echo "Лог не найден"
echo ""

echo "7. Проверка firewall (ufw):"
sudo ufw status 2>/dev/null | grep 6432 || echo "Порт 6432 не найден в правилах ufw"
echo ""

echo "8. Проверка iptables для порта 6432:"
sudo iptables -L -n 2>/dev/null | grep 6432 || echo "Правил для порта 6432 не найдено"
echo ""

echo "9. Проверка подключения pgbouncer к PostgreSQL (локально):"
psql -h localhost -p 5432 -U secret_offers_bot_admin -d secret_offers_bot_db -c "SELECT 1;" 2>&1 | head -5
echo ""

echo "10. Проверка подключения через pgbouncer (локально):"
psql -h localhost -p 6432 -U secret_offers_bot_admin -d secret_offers_bot_db -c "SELECT 1;" 2>&1 | head -5
echo ""

echo "11. Проверка конфигурации pgbouncer.ini (auth_type и listen_addr):"
sudo grep -E "^(auth_type|listen_addr|auth_file)" /etc/pgbouncer/pgbouncer.ini 2>/dev/null || echo "Конфиг не найден"
echo ""

echo "12. Проверка секции [databases] в pgbouncer.ini:"
sudo grep -A 5 "^\[databases\]" /etc/pgbouncer/pgbouncer.ini 2>/dev/null || echo "Секция не найдена"
echo ""

echo "13. Проверка pg_hba.conf для подключения pgbouncer -> PostgreSQL:"
sudo grep -E "127\.0\.0\.1|localhost" /etc/postgresql/14/main/pg_hba.conf 2>/dev/null | head -5 || echo "Файл не найден"
echo ""

echo "14. Проверка, может ли внешний IP подключиться (тест с telnet):"
timeout 2 telnet 5.129.242.211 6432 2>&1 | head -3 || echo "Telnet не доступен или порт закрыт"
echo ""

echo "=== Критические проверки ==="
echo ""
echo "15. Проверка, что pgbouncer запущен:"
if pgrep -x pgbouncer > /dev/null; then
    echo "✓ pgbouncer запущен (PID: $(pgrep -x pgbouncer))"
else
    echo "✗ pgbouncer НЕ запущен!"
fi
echo ""

echo "16. Проверка, что PostgreSQL запущен:"
if pgrep -x postgres > /dev/null; then
    echo "✓ PostgreSQL запущен"
else
    echo "✗ PostgreSQL НЕ запущен!"
fi
echo ""

echo "=== Рекомендации ==="
echo ""
echo "Если подключение не работает извне, проверьте:"
echo "1. Firewall: sudo ufw allow 6432/tcp"
echo "2. pgbouncer слушает на 0.0.0.0:6432 (не только 127.0.0.1)"
echo "3. Логи pgbouncer при попытке подключения: sudo tail -f /var/log/postgresql/pgbouncer.log"
echo "4. Формат userlist.txt правильный (кавычки, префикс md5 или SCRAM)"
echo "5. pgbouncer может подключиться к PostgreSQL локально"
echo "6. В pg_hba.conf разрешено подключение для pgbouncer (127.0.0.1)"



