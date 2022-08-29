import json
from person import Person


class UserData:
    def __init__(self, main_id, friends: dict, common_friends: dict, friends_base_info: dict, main_id_info,
                 banned_friends: dict):
        self.main_id = main_id
        self.friends = friends
        self.common_friends = common_friends
        self.friends_base_info = friends_base_info
        self.main_person = Person(main_id_info, common_friends=[friend['id'] for friend in self.friends])
        self.banned_friends_ids = [friend['id'] for friend in banned_friends]

        self.persons = None

    def initialize_friends(self):
        self.persons = {person['id']: Person(person) for person in self.friends_base_info}
        self.persons[self.main_person.uid] = self.main_person

        common_friends_ids = {person['id']: person['common_friends'] for person in self.common_friends}
        common_friends_ids[self.main_person.uid] = self.main_person.common_friends

        for id, person in self.persons.items():
            common_friends = []
            for common_friend_id in common_friends_ids[id]:
                if common_friend_id in self.banned_friends_ids:
                    continue
                common_friends.append(self.persons[common_friend_id])

            person.set_friends(common_friends)

    def dump_data_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            links = []
            nodes = []
            for person in self.persons.values():
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
# 2. Reformat the project structure. DONE
# 3. Remove the second connection between nodes. DONE
# 4. Create authentication with any vk user.
