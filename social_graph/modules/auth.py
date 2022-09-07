import os

from vk_api import VkApi

user = VkApi(login='89512517109', password='P0lina2025', token=os.environ['VK_API_TOKEN'])

user.auth()


'https://oauth.vk.com/authorize?client_id=51395060&display=page&redirect_uri=https://vk-social-graph.herokuapp.com/auth&scope=friends&response_type=code&v=5.131'