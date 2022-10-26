from json import JSONEncoder


class GraphEncoder(JSONEncoder):
    def default(self, o):
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
                             'value': 1} for target_id in o.mutual_friends[friend['id']] if
                            (target_id, friend['id']) not in require_links]

            for friend_id in o.mutual_friends[friend['id']]:
                require_links.add((friend['id'], friend_id))

            nodes.append(node)
            links.extend(friend_links)

        nodes.append({
            'id': o.vk_user_id,
            'group': o.sex,
            'name': f'{o.first_name} {o.last_name}',
        })
        links.extend([{'source': o.vk_user_id,
                       'target': friend_id,
                       'value': 1} for friend_id in o.friends_ids])

        return {
            'nodes': nodes,
            'links': links,
        }
