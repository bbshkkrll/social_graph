import json

from social_graph.modules.graph import Graph
from social_graph.modules.vk_session import VkSession


class User:
    def __init__(self, expires_in, user_id, access_token):
        self.graph = None
        self.expires_in = expires_in
        self.user_id = user_id
        self.access_token = access_token
        self.vk_session = VkSession(token=self.access_token)

        self.all_friends = self.vk_session.get_friends()  # list of friends (uid, first_name, last_name, sex)
        self.active_friends = list(filter((lambda x: 'deactivated' not in x.keys()), self.all_friends))
        self.deactivated_friends = list(filter((lambda x: 'deactivated' in x.keys()), self.all_friends))
        self.friends_ids = [friend['id'] for friend in self.active_friends]  # ids of active friends
        self.mutual_friends = self.get_mutual_friends()  # dict id : mutual friends with this user and id

    def get_mutual_friends(self):
        return {item['id']: item['common_friends']
                for item in self.vk_session.get_mutual_friends(self.friends_ids)}

    def get_active_friends_as_dict(self):
        if self.active_friends is not None:
            return {friend['id']: friend for friend in self.active_friends}

    def save_graph(self, filename=None):
        if filename is None:
            filename = f'./static/data/graph_data_{self.user_id}.json'
        if self.graph is not None:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.graph.graph, f, ensure_ascii=False)
        else:
            self.graph = Graph(self)
            self.save_graph()

        return filename
