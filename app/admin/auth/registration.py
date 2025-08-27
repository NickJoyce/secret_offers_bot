import requests
from settings import ADMIN_TOKEN

def register_superuser(email, password, config):
    TEST_ENV = False
    if TEST_ENV:
        url = "http://127.0.0.1:8000/users"
    else:
        url = "https://secret-offers-bot.podrugeapi.ru/users"
    headers = {'Authorization': f'{ADMIN_TOKEN}',
               'Content-Type': 'application/json'}
    data = {'email': email,
            'password': password,
            'config': config}
    response = requests.post(url=url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":


    print(register_superuser(email='smirnov.nikita@podruge.ru',
                             password='tLyT3wWh',
                             config={"name": "nikita",
                                     "avatar": "admin/avatar.jpeg",
                                     "company_logo_url": None,
                                     "roles": ["read", "create", "edit", "delete", "action_make_published"]}))
    
    
