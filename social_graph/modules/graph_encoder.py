from json import JSONEncoder

from social_graph.modules.models import User


class GraphEncoder(JSONEncoder):
    def default(self, o: User):
        require_links = set()
        links = []
        nodes = []

        # dict_friends = self.user.get_active_friends_as_dict()

        for friend in o.active_friends:
            node = {
                'id': friend['id'],
                'group': friend['sex'],
                'name': f'{friend["first_name"]} {friend["last_name"]}',
            }

            friend_links = [{'source': friend['id'],
                             'target': target_id,
                             'value': 1} for target_id in o.user.mutual_friends[friend['id']] if
                            (target_id, friend['id']) not in require_links]

            for friend_id in o.user.mutual_friends[friend['id']]:
                require_links.add((friend['id'], friend_id))

            nodes.append(node)
            links.extend(friend_links)

        nodes.append({
            'id': o.user.user_id,
            'group': o.user.sex,
            'name': f'{o.user.first_name} {o.user.last_name}',
        })
        links.extend([{'source': o.user.user_id,
                       'target': friend_id,
                       'value': 1} for friend_id in o.user.friends_ids])

        return {
            'nodes': nodes,
            'links': links,
        }
