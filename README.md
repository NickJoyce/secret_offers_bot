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
##### gpt-bot.endospherebeauty.com (fastapi)  
/etc/nginx/sites-available/fastapi_gpt_bot
```
server {
    listen 80;
    # server_name gpt-bot.endospherebeauty.com;
    return 301 https://$host:443$request_uri;
}
```
/etc/nginx/sites-available/fastapi_gpt_bot_ssl
```
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name gpt-bot.endospherebeauty.com;

    #ssl on
    ssl_certificate /etc/letsencrypt/live/gpt-bot.endospherebeauty.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/gpt-bot.endospherebeauty.com/privkey.pem;

    # Обработка favicon.ico в корневой директории
    location = /favicon.ico {
        access_log off;
        log_not_found off;
        alias /home/main/fastapi_gpt_bot/static/favicon.ico;
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
sudo ln -s /etc/nginx/sites-available/fastapi_gpt_bot /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/fastapi_gpt_bot_ssl /etc/nginx/sites-enabled
```

##### gpt-bot-supervisor.endospherebeauty.com(supervisor)  
/etc/nginx/sites-available/gpt_bot_supervisor
```
server {
    listen 80;
    #server_name gpt-bot.endospherebeauty.com;
    return 301 https://$host:443$request_uri;
}

```
/etc/nginx/sites-available/gpt_bot_supervisor_ssl
```
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name gpt-bot-supervisor.endospherebeauty.com;

    #ssl on
    ssl_certificate /etc/letsencrypt/live/gpt-bot-supervisor.endospherebeauty.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/gpt-bot-supervisor.endospherebeauty.com/privkey.pem;

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
sudo ln -s /etc/nginx/sites-available/gpt_bot_supervisor_ssl /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/gpt_bot_supervisor /etc/nginx/sites-enabled
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