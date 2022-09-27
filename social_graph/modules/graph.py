from social_graph.modules.user import User


class Graph:
    def __init__(self, user: User):
        self.user = user
        self.graph = self.initialize_graph()

    def initialize_graph(self):
        if self.graph is not None:
            return self.graph
        require_links = set()
        links = []
        nodes = []

        # dict_friends = self.user.get_active_friends_as_dict()

        for friend in self.user.active_friends:
            node = {
                'name': f'{friend["first_name"]} {friend["last_name"]}',
                'id': friend['id'],
                'group': friend['sex']
            }

            friend_links = [{'source': friend['id'],
                             'target': target_id,
                             'value': 1} for target_id in self.user.mutual_friends[friend['id']] if
                            (target_id, friend['id']) not in require_links]

            for friend_id in self.user.mutual_friends[friend['id']]:
                require_links.add((friend['id'], friend_id))

            nodes.append(node)
            links.extend(friend_links)

        return {
            'links': links,
            'nodes': nodes
        }
