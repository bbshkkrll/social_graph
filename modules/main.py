import json
from person import Person

persons = None

with open('base_info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    persons = {person['id']: Person(person) for person in data}

with open('mutual_friends.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    common_friends_ids = {person['id']: person['common_friends'] for person in data}

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
