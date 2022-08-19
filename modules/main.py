import json

import requests

from person import Person
from vk_request import main_id, get_url

persons = None

with open('base_info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    persons = {person['id']: Person(person) for person in data}
    persons[main_id] = Person(
        requests.get(get_url('users.get', {'fields': 'uid,first_name,last_name,photo,sex',
                                           'user_id': main_id})).json()['response'][0])
    # Добавление главного id
    persons[main_id].sex = 45

with open('mutual_friends.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    common_friends_ids = {person['id']: person['common_friends'] for person in data}

    with open('friends.json', 'r', encoding='utf-8') as f:
        friends = [person['id'] for person in json.load(f)['items']]
        common_friends_ids[main_id] = friends
    for id, person in persons.items():
        common_friends = []
        for common_friend_id in common_friends_ids[id]:
            common_friends.append(persons[common_friend_id])

        person.set_friends(common_friends)

with open('graph_data.json', 'w', encoding='utf-8') as f:
    links = []
    nodes = []
    for person in persons.values():
        json_person = person.to_json()
        links.extend(json_person['links'])
        nodes.append(json_person['nodes'])
    json.dump(
        {
            'nodes': nodes,
            'links': links
        },
        f, ensure_ascii=False)

# TODO:
# 1. Add main_id to graph. DONE
# 2. Reformat the project structure
# 3. Remove the second connection between nodes. DONE
# 4. Create authentication with any vk user.
