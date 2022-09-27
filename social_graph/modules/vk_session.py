import json
import os
import requests

from time import sleep

from social_graph.modules.partition import get_partition as parts
from social_graph.modules.enums import VkApiMethods as api_methods
from social_graph.modules.enums import VkApiKeys as api_keys
from social_graph.modules.enums import VkApiFields as api_fields
from social_graph.modules.response import VkApiResponse as resp
from social_graph.modules.vk_exception import VkException


class VkSession:
    def __init__(self, version=os.environ['VK_API_VERSION'], token=os.environ['VK_API_TOKEN']):
        self.v = version
        self.token = token

    def get_request_url(self, url: str, method: str, fields: dict, token=True):
        """Возвращает url для доступа к VKApi"""
        request_url = f'{url}{method}?'
        for name, value in fields.items():
            request_url += f'{name}={value}&'
        if token:
            return request_url + f'{api_keys.ACCESS_TOKEN.value}={self.token}&{api_keys.V.value}={self.v}'
        return f'{request_url}{api_keys.V.value}={self.v}'

    def get_current_user_id(self):
        url = self.get_request_url(api_methods.METHOD_URL.value, api_methods.USERS_GET.value, fields={
            api_keys.FIELDS.value: ''.join([api_fields.ID.value])
        }, token=True)

        response = resp(requests.get(url).json())
        return response['id']

    def get_access(self, code):
        url = self.get_request_url(api_methods.OUAUTH_URL.value, api_methods.ACCESS_TOKEN.value, fields={
            api_keys.CLIENT_ID.value: os.environ['CLIENT_ID'],
            api_keys.CLIENT_SECRET.value: os.environ['CLIENT_SECRET'],
            api_keys.REDIRECT_URI.value: os.environ['REDIRECT_URI'],
            api_keys.CODE.value: code
        }, token=False)

        response = resp(requests.get(url).json())
        return response

    def get_users_base_info(self, ids, fields=None):
        """Возвращает базовую информацию о пользователе"""
        if fields is None:
            fields = [api_fields.UID.value,
                      api_fields.FIRST_NAME.value,
                      api_fields.LAST_NAME.value,
                      api_fields.PHOTO.value,
                      api_fields.SEX.value]

        url = self.get_request_url(api_methods.METHOD_URL.value, api_methods.USERS_GET.value,
                                   {api_keys.USER_IDS.value: ','.join(ids),
                                    api_keys.FIELDS.value: ','.join(fields)})

        response = resp(requests.get(url).json())
        return response['response']

    def get_friends(self):
        url = self.get_request_url(api_methods.METHOD_URL.value,
                                   api_methods.FRIENDS_GET.value,
                                   fields={
                                       api_keys.FIELDS.value: ','.join(
                                           [api_fields.UID.value,
                                            api_fields.FIRST_NAME.value,
                                            api_fields.LAST_NAME.value,
                                            api_fields.SEX.value]),
                                       # без id, найдет по токену
                                   })

        response = resp(requests.get(url).json())
        return response['response']['items']

    def get_mutual_friends(self, friends, delay=0.35):
        """
        Example response
            {
                "response":[
                    0:{
                        "common_count":3
                        "common_friends":[
                            0:324441199
                            1:507388294
                            2:714374754
                        ]
                    "id":131553710
                }
                    1:{
                        "common_count":1
                        "common_friends":[
                            0:131553710
                        ]
                    "id": 507388294
                }
            }
        """
        common_friends = []

        for part in parts(friends):
            url = self.get_request_url(api_methods.METHOD_URL.value,
                                       api_methods.FRIENDS_GET_MUTUAL.value,
                                       fields={
                                           api_keys.TARGET_UIDS.value: ','.join(map(str, part))
                                       })
            try:
                response = resp(requests.get(url).json())
                common_friends.extend(response['response'])
            except VkException as e:
                print(e.message, 'In mutual friends')

            sleep(delay)

        return common_friends
