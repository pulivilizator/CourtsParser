import requests
import base64

def get_auth_cookie(config):
    login = config.bipium_login
    password = config.bipium_password
    bipium_domain = config.bipium_domain
    credentials = base64.b64encode(f'{login}:{password}'.encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': f'Basic {credentials}'
    }

    # Отправляем запрос на авторизацию
    response = requests.get(f'https://{bipium_domain}.bpium.ru/auth/login', headers=headers)

    # Получаем cookie sid из ответа
    cookie = f'connect.sid={response.cookies.get("connect.sid")}'
    headers = {
        'cookie': cookie
    }
    return headers