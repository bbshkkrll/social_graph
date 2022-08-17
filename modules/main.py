import json
import os
import requests


def get_url(method: str, fields: dict):
    version = '5.131'
    url = f'https://api.vk.com/method/{method}?'
    for name, value in fields.items():
        url += f'{name}={value}&'

    url += f'access_token={os.environ["VK_API_TOKEN"]}&v={version}'
    return url


if __name__ == '__main__':
    main_id = '324441199'

    response = requests.get(get_url('friends.get', {'fields': 'uid,first_name,last_name'})).json()['response']

    friends_ids = [friend['id'] for friend in response['items']]

    with open('friends.json', 'w', encoding='utf-8') as f:
        json.dump(response, f,
                  ensure_ascii=False)

    mutual_friends = requests.get(get_url('execute.get_mutual_friends', {
        'targets': ','.join(map(str, friends_ids)),
        'main_id': main_id
    })).json()['response']

    with open('mutual_friends.json', 'w', encoding='utf-8') as f:
        json.dump(mutual_friends, f,
                  ensure_ascii=False)

    base_info = requests.get(
        get_url('users.get', {'fields': 'uid,first_name,last_name,city,photo,bday,country,sex',
                              'user_ids': ','.join(map(str, friends_ids))})).json()[
        'response']
    with open('base_info.json', 'w', encoding='utf-8') as f:
        json.dump(base_info, f, ensure_ascii=False)
