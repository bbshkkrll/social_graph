import requests

from modules.vk_request import get_url

app_id = 51395060
redirect_uri = 'https://oauth.vk.com/blank.html'

code_flow_url = f'https://oauth.vk.com/authorize?client_id={app_id}&display=page&redirect_uri=http://127.0.0.1&scope=friends&response_type=code&v=5.131'
print(code_flow_url)

print(requests.get(get_url('users.get', {'fields': 'uid'})).json()['response'][0])