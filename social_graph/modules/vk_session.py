import json
import os
import requests
from time import sleep

from modules.user_data import UserData
from modules.partition import get_partition as parts


class VkException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code


class VkSession(Exception):
    FRIENDS_GET = 'friends.get'
    USERS_GET = 'users.get'
    FRIENDS_GET_MUTUAL = 'friends.getMutual'
    EXECUTE_GET_MUTUAL_FRIENDS = 'execute.get_mutual_friends'
    BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, version=os.environ['VK_API_VERSION'], token=os.environ['VK_API_TOKEN']):
        self.v = version
        self.token = token

    def get_request_url(self, method: str, fields: dict):
        request_url = f'{self.BASE_URL}{method}?'
        for name, value in fields.items():
            request_url += f'{name}={value}&'

        return request_url + f'access_token={self.token}&v={self.v}'

    def get_user_base_info(self, id):
        response = requests.get(self.get_request_url(VkSession.USERS_GET,
                                                     {'user_ids': id,
                                                      'fields': 'uid,first_name,last_name,photo,sex'})).json()

        if 'error' in response.keys():
            raise VkException(response['error']['error_msg'], response['error']['error_code'])

        return response['response'][0]

    def prepare_data(self, main_id, delay=0.98):

        friends = requests.get(self.get_request_url(self.FRIENDS_GET, {'fields': 'uid,first_name,last_name',
                                                                       'user_id': main_id})).json()

        if 'error' in friends.keys():
            raise VkSession(friends['error']['error_msg'], friends['error']['error_code'])

        active_friends = list(filter((lambda x: 'deactivated' not in x.keys()),
                              friends['response']['items']))
        banned_friends = list(filter((lambda x: 'deactivated' in x.keys()), friends['response']['items']))
        friends_id = [friend['id'] for friend in active_friends]

        common_friends = []
        req_count = 0
        for sublist in parts(friends_id, size=100):
            if req_count == 3:
                req_count = 0
                sleep(delay)
            res = requests.get(self.get_request_url(VkSession.FRIENDS_GET_MUTUAL, {
                'source_uid': main_id,
                'target_uids': ','.join(map(str, sublist))

            })).json()

            req_count += 1

            if 'error' in res.keys():
                raise VkSession(res['error']['error_msg'], res['error']['error_code'])

            common_friends.extend(res['response'])

        friends_base_info = requests.get(
            self.get_request_url(VkSession.USERS_GET, {'fields': 'uid,first_name,last_name,photo,sex',
                                                       'user_ids': ','.join(map(str, friends_id))})).json()

        if 'error' in friends_base_info.keys():
            raise VkSession(friends_base_info['error']['error_msg'], friends_base_info['error']['error_code'])

        friends_base_info = friends_base_info['response']
        return active_friends, common_friends, friends_base_info, self.get_user_base_info(main_id), banned_friends


if __name__ == '__main__':
    # main_id = '324441199'
    # main_id = '745403617'
    main_id = '131553710'

    session = VkSession(
        token='vk1.a.bsCwOjdpJauKuhGXbztYNaeVwLkQOYNUYsvSP-MZBSJvQ8pGAGgY7jPdO9D-LYU28Gxx8139lAkhBaLHhmToRPZJ6YkKfq6-2IpytxS3bmkjBKN8WV9-RiuS-mN7A2ra9Qmic1phe-70-I6M6T_Ot4GdFWvCFDpq9KRmIPjAuN3JYIp7P92BEEHSdrzbKsDY')
    # session = VkSession(token='k0NBPBozTtW1om6I0yZ1')
    try:

        user_info = UserData(main_id, *session.prepare_data(main_id))
        user_info.initialize_friends()
        user_info.dump_data_to_json('../data/graph_data.json')
    except VkException as e:
        print(e.message, e.code)
