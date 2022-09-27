import requests

import vk_session
from social_graph.modules.enums import VkApiMethods as api_methods
s = vk_session.VkSession()

token = s.get_access('20e20278a46f4d2eb6')
print(token)
us = vk_session.VkSession(token=token)

print(us.get_mutual_friends([131553710]))

