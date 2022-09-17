import json
import os
from enum import Enum

import requests
from time import sleep

from social_graph.modules.user_data import UserData
from social_graph.modules.partition import get_partition as parts


class VkException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code


class VkApiMethods(Enum):
    FRIENDS_GET = 'friends.get'
    USERS_GET = 'users.get'
    FRIENDS_GET_MUTUAL = 'friends.getMutual'
    EXECUTE_GET_MUTUAL_FRIENDS = 'execute.get_mutual_friends'
    AUTHORIZE = 'authorize'
    ACCESS_TOKEN = 'access_token'
    METHOD_URL = 'https://api.vk.com/method/'
    OUAUTH_URL = 'https://oauth.vk.com/'


class VkApiFields(Enum):
    UID = 'uid'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    SEX = 'sex'
    PHOTO = 'photo'
    PAGE = 'page'
    FRIENDS = 'friends'
    CODE = 'code'


class VkApiKeys(Enum):
    DISPLAY = 'display'
    USER_ID = 'user_id'
    USER_IDS = 'user_ids'
    CLIENT_ID = 'client_id'
    CLIENT_SECRET = 'client_secret'
    REDIRECT_URI = 'redirect_uri'
    CODE = 'code'
    SCOPE = 'scope'
    RESPONSE_TYPE = 'response_type'
    FIELDS = 'fields'


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
            return request_url + f'access_token={self.token}&v={self.v}'
        return f'{request_url}v={self.v}'

    def get_current_user_id(self):
        url = self.get_request_url(VkApiMethods.METHOD_URL.value, VkApiMethods.USERS_GET.value, fields={
            VkApiKeys.FIELDS.value: ''.join(['id'])
        }, token=True)
        print(url)
        response = requests.get(url).json()

        print(response)
        if 'error' in response.keys():
            raise VkException(response['error']['error_msg'], response['error']['error_code'])
        return response['response'][0]['id']

    def get_access_token(self, code):
        url = self.get_request_url(VkApiMethods.OUAUTH_URL.value, VkApiMethods.ACCESS_TOKEN.value, fields={
            VkApiKeys.CLIENT_ID.value: os.environ['CLIENT_ID'],
            VkApiKeys.CLIENT_SECRET.value: os.environ['CLIENT_SECRET'],
            VkApiKeys.REDIRECT_URI.value: os.environ['REDIRECT_URI'],
            VkApiKeys.CODE.value: code
        }, token=False)

        response = requests.get(url).json()

        if 'error' in response.keys():
            raise VkException(response['error'], response['error_description'])

        return response['access_token']

    def get_user_base_info(self, id, fields=None):
        """Возвращает базовую информацию о пользователе"""
        if fields is None:
            fields = [VkApiFields.UID.value, VkApiFields.FIRST_NAME.value, VkApiFields.LAST_NAME.value,
                      VkApiFields.PHOTO.value,
                      VkApiFields.SEX.value]
        response = requests.get(self.get_request_url(VkApiMethods.METHOD_URL.value, VkApiMethods.USERS_GET.value,
                                                     {VkApiKeys.USER_IDS.value: id,
                                                      'fields': ','.join(fields)})).json()

        if 'error' in response.keys():
            raise VkException(response['error']['error_msg'], response['error']['error_code'])

        return response['response'][0]

    def prepare_data(self, id=None, delay=0.35):
        if id is None:
            id = self.get_current_user_id()
        friends = requests.get(
            self.get_request_url(VkApiMethods.METHOD_URL.value, VkApiMethods.FRIENDS_GET.value,
                                 {'fields': ','.join([VkApiFields.UID.value, VkApiFields.FIRST_NAME.value,
                                                      VkApiFields.LAST_NAME.value]),
                                  'user_id': id})).json()

        if 'error' in friends.keys():
            raise VkException(friends['error']['error_msg'], friends['error']['error_code'])

        active_friends = list(filter((lambda x: 'deactivated' not in x.keys()),
                                     friends['response']['items']))
        banned_friends = list(filter((lambda x: 'deactivated' in x.keys()), friends['response']['items']))
        friends_id = [friend['id'] for friend in active_friends]

        common_friends = []

        for sublist in parts(friends_id, size=100):
            res = requests.get(
                self.get_request_url(VkApiMethods.METHOD_URL.value, VkApiMethods.FRIENDS_GET_MUTUAL.value, {
                    'source_uid': id,
                    'target_uids': ','.join(map(str, sublist))

                })).json()

            sleep(delay)

            if 'error' in res.keys():
                raise VkException(res['error']['error_msg'], res['error']['error_code'])

            common_friends.extend(res['response'])

        friends_base_info = requests.get(
            self.get_request_url(VkApiMethods.METHOD_URL.value, VkApiMethods.USERS_GET.value,
                                 {'fields': 'uid,first_name,last_name,photo,sex',
                                  'user_ids': ','.join(map(str, friends_id))})).json()

        if 'error' in friends_base_info.keys():
            raise VkException(friends_base_info['error']['error_msg'], friends_base_info['error']['error_code'])

        friends_base_info = friends_base_info['response']
        return active_friends, common_friends, friends_base_info, self.get_user_base_info(id), banned_friends


if __name__ == '__main__':
    main_id = '324441199'
    session = VkSession()
    try:

        user_info = UserData(main_id, *session.prepare_data(main_id))
        user_info.initialize_friends()
        user_info.dump_data_to_json('../static/data/graph_data.json')
    except VkException as e:
        print(e.message, e.code)
