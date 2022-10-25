import json

from social_graph.app import db
from social_graph.app.modules.graph_encoder import GraphEncoder
from social_graph.app import VkSession


class Token(db.Model):
    __tablename__ = 'token_table'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100))
    expires_in = db.Column(db.Integer)

    def __init__(self, user_id, access_token, expires_in):
        self.id = user_id
        self.token = access_token
        self.expires_in = expires_in


class Graph(db.Model):
    __tablename__ = 'graph_table'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON)

    def __init__(self, user):
        self.data = json.dumps(user, cls=GraphEncoder)


class User(db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    vk_user_id = db.Column(db.String(15))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    sex = db.Column(db.String(5))

    token_id = db.Column(db.Integer, db.ForeignKey('token_table.id'), nullable=False)
    token = db.relationship('Token', backref=db.backref('User'), lazy=True)

    graph_id = db.Column(db.Integer, db.ForeignKey('graph_table.id'), nullable=False)
    graph = db.relationship('Graph', backref=db.backref('User'), lazy=True)

    def __init__(self, access_token: Token):
        self.user_id = access_token.id
        self.access_token = access_token
        self.vk_session = VkSession(token=self.access_token.token)

        self.first_name, self.last_name, self.sex = self.get_base_info()

        self.all_friends = self.vk_session.get_friends()  # list of friends (uid, first_name, last_name, sex)
        self.active_friends = list(filter((lambda x: 'deactivated' not in x.keys()), self.all_friends))
        self.deactivated_friends = list(filter((lambda x: 'deactivated' in x.keys()), self.all_friends))
        self.friends_ids = [friend['id'] for friend in self.active_friends]  # ids of active friends
        self.mutual_friends = self.get_mutual_friends()  # dict id : mutual friends with this user and id

        self.graph = Graph(self)

    def get_mutual_friends(self):
        return {item['id']: item['common_friends']
                for item in self.vk_session.get_mutual_friends(self.friends_ids)}

    def get_active_friends_as_dict(self):
        if self.active_friends is not None:
            return {friend['id']: friend for friend in self.active_friends}

    def get_graph(self):
        return Graph(self)

    def get_base_info(self):
        info = self.vk_session.get_current_user_base_info()
        return info['first_name'], info['last_name'], info['sex']
