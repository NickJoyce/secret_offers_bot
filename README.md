### Comments
Из базового шабона библиотеки startlette_admin  
```path
/marketing_bot/venv/lib/python3.10/site-packages/starlette_admin/templates/base.html
```
Была удалена строка 15, так как ресурс был недоступен при загрузке страницы

```html
@import url('https://rsms.me/inter/inter.css');  
```



### nginx
##### secret-offers-bot.podrugeapi.ru 
sudo nano /etc/nginx/sites-available/secret_offers_bot
```
server {
    listen 80;
    # server_name secret-offers-bot.podrugeapi.ru;
    return 301 https://$host:443$request_uri;
}
```
sudo nano /etc/nginx/sites-available/secret_offers_bot_ssl
```
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name secret-offers-bot.podrugeapi.ru;

    #ssl on
    ssl_certificate /etc/letsencrypt/live/secret-offers-bot.podrugeapi.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/secret-offers-bot.podrugeapi.ru/privkey.pem;

    # Обработка favicon.ico в корневой директории
    location = /favicon.ico {
        access_log off;
        log_not_found off;
        alias /home/main/secret_offers_bot/static/favicon.ico;
    }


   location / {
       include proxy_params;
       proxy_pass http://127.0.0.1:8000;
   }

   location /static {
       include proxy_params;
       proxy_pass http://127.0.0.1:8000/static;
   }
}

```

```console
sudo ln -s /etc/nginx/sites-available/secret_offers_bot /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/secret_offers_bot_ssl /etc/nginx/sites-enabled
```

##### secret-offers-bot-supervisor.podrugeapi.ru (supervisor)  
sudo nano /etc/nginx/sites-available/supervisor
```
server {
    listen 80;
    #server_name secret-offers-bot-supervisor.podrugeapi.ru;
    return 301 https://$host:443$request_uri;
}

```
sudo nano /etc/nginx/sites-available/supervisor_ssl
```
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name secret-offers-bot-supervisor.podrugeapi.ru;

    #ssl on
    ssl_certificate /etc/letsencrypt/live/secret-offers-bot-supervisor.podrugeapi.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/secret-offers-bot-supervisor.podrugeapi.ru/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:9001/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

```

```console
sudo ln -s /etc/nginx/sites-available/supervisor_ssl /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/supervisor /etc/nginx/sites-enabled
```

### supervisor
/home/main/supervisor/fastapi_gpt_bot.conf
```
[program:fastapi_gpt_bot]
directory=/home/main/fastapi_gpt_bot
command=/home/main/fastapi_gpt_bot/venv/bin/gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app
user=main
process_name=%(program_name)s
numprocs=1
autostart=false
autorestart=true
startsecs=2
startretries=3
exitcodes=0
stopsignal=TERM
stopwaitsecs=10
```