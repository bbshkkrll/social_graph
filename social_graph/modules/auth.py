import requests

for_code = 'https://oauth.vk.com/authorize?client_id=51395060&display=page&redirect_uri=https://vk-social-graph.herokuapp.com/auth&scope=friends&response_type=code&v=5.131'
for_token = 'https://oauth.vk.com/access_token?client_id=51395060&client_secret=k0NBPBozTtW1om6I0yZ1&redirect_uri=https://vk-social-graph.herokuapp.com/auth&code='
code = '2e54f8f7c23d56ef79'

print(requests.get(for_token + code).json())
