import os

from vk_api import VkApi

user = VkApi(login='89512517109', password='P0lina2025', token=os.environ['VK_API_TOKEN'])

user.auth()


