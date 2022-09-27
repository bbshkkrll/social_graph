import requests

import vk_session
from social_graph.modules.enums import VkApiMethods as api_methods
s = vk_session.VkSession()

# token = s.get_access('20e20278a46f4d2eb6')
# print(token)
us = vk_session.VkSession(token='vk1.a.4muYL5LeGulaEHI2bipICCAcur-mfcVDHaj1dxln0Qf6Eeau1TKt6b6lcE08nolFBPtj_WU1AJExIP6kJCGZ9i0dL2uLoe0Yco5FWi2Es6XhwsS_KMP78jpKqzXnz9Ty4iLb8bQ83n-fzCL9U5kD2H3xY4pQuksPb11Z24-fQxAErukUF4WkCxp0XHgqSTok')

print(us.get_current_user_base_info())

