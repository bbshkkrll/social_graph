import json
import os
import requests

from time import sleep

from social_graph.modules.partition import get_partition as parts
from social_graph.modules.enums import VkApiMethods as api_methods
from social_graph.modules.enums import VkApiKeys as api_keys
from social_graph.modules.enums import VkApiFields as api_fields
from social_graph.modules.enums import VkApiError as api_err
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

    def get_access_token(self, code):
        url = self.get_request_url(api_methods.OUAUTH_URL.value, api_methods.ACCESS_TOKEN.value, fields={
            api_keys.CLIENT_ID.value: os.environ['CLIENT_ID'],
            api_keys.CLIENT_SECRET.value: os.environ['CLIENT_SECRET'],
            api_keys.REDIRECT_URI.value: os.environ['REDIRECT_URI'],
            api_keys.CODE.value: code
        }, token=False)

        response = requests.get(url).json()
        if api_err.ERROR.value in response.api_keys():
            raise VkException(response[api_err.ERROR.value])

        return response['access_token']

    def get_user_base_info(self, id, fields=None):
        """Возвращает базовую информацию о пользователе"""
        if fields is None:
            fields = [api_fields.UID.value, api_fields.FIRST_NAME.value, api_fields.LAST_NAME.value,
                      api_fields.PHOTO.value,
                      api_fields.SEX.value]
        response = requests.get(self.get_request_url(api_methods.METHOD_URL.value, api_methods.USERS_GET.value,
                                                     {api_keys.USER_IDS.value: id,
                                                      api_keys.FIELDS.value: ','.join(fields)})).json()

        if api_err.ERROR.value in response.api_keys():
            raise VkException(response['error']['error_msg'])

        return response['response'][0]

    def prepare_data(self, id=None, delay=0.35):
        if id is None:
            id = self.get_current_user_id()
        friends = requests.get(
            self.get_request_url(api_methods.METHOD_URL.value, api_methods.FRIENDS_GET.value,
                                 {'fields': ','.join([api_fields.UID.value, api_fields.FIRST_NAME.value,
                                                      api_fields.LAST_NAME.value]),
                                  'user_id': id})).json()

        if 'error' in friends.api_keys():
            raise VkException(friends['error']['error_msg'])

        active_friends = list(filter((lambda x: 'deactivated' not in x.api_keys()),
                                     friends['response']['items']))
        banned_friends = list(filter((lambda x: 'deactivated' in x.api_keys()), friends['response']['items']))
        friends_id = [friend['id'] for friend in active_friends]

        common_friends = []

        for sublist in parts(friends_id, size=100):
            res = requests.get(
                self.get_request_url(api_methods.METHOD_URL.value, api_methods.FRIENDS_GET_MUTUAL.value, {
                    'source_uid': id,
                    'target_uids': ','.join(map(str, sublist))

                })).json()

            sleep(delay)

            if 'error' in res.api_keys():
                raise VkException(res['error']['error_msg'])

            common_friends.extend(res['response'])

        friends_base_info = requests.get(
            self.get_request_url(api_methods.METHOD_URL.value, api_methods.USERS_GET.value,
                                 {'fields': 'uid,first_name,last_name,photo,sex',
                                  'user_ids': ','.join(map(str, friends_id))})).json()

        if 'error' in friends_base_info.api_keys():
            raise VkException(friends_base_info['error']['error_msg'])

        friends_base_info = friends_base_info['response']
        return active_friends, common_friends, friends_base_info, self.get_user_base_info(id), banned_friends
