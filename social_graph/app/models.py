import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Text, JSON
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Integer, String
from social_graph.app.modules.graph_encoder import GraphEncoder
from social_graph.app import VkSession
from sqlalchemy.types import TypeDecorator

Base = declarative_base()


class Token(Base):
    __tablename__ = 'token_table'

    id = Column(Integer, primary_key=True)
    token = Column(String(300))
    expires_in = Column(Integer)

    def __init__(self, user_id, access_token, expires_in, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = user_id
        self.token = access_token
        self.expires_in = expires_in


class Graph(Base):
    __tablename__ = 'graph_table'
    id = Column(Integer, primary_key=True)
    data = Column(Text)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = json.dumps(user, cls=GraphEncoder)


class User(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True)
    vk_user_id = Column(String(15))
    first_name = Column(String(30))
    last_name = Column(String(30))
    sex = Column(String(5))

    token_id = Column(Integer, ForeignKey('token_table.id'), nullable=False)
    token = relationship('Token', backref=backref('User'), lazy=True)

    graph_id = Column(Integer, ForeignKey('graph_table.id'), nullable=False)
    graph = relationship('Graph', backref=backref('User'), lazy=True)

    def __init__(self, access_token: Token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = access_token
        self.token_id = self.token.id
        self.vk_session = VkSession(token=self.token.token)

        self.first_name, self.last_name, self.sex, self.vk_user_id = self.get_base_info()

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
        return info['first_name'], info['last_name'], info['sex'], info['id']
