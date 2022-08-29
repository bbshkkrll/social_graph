class Person:
    DEFAULT_VALUE = 1
    MUTUAL_FRIENDS = set()

    def __init__(self, data: dict, common_friends=None):
        self.uid: int = int(data['id'])
        self.first_name: str = data['first_name']
        self.last_name: str = data['last_name']
        self.sex: int = int(data['sex'])
        self.photo: str = data['photo']
        self.common_friends: [Person] = common_friends
        self.color = self.sex

    def __str__(self):
        return f'Person: first_name={self.first_name} last_name={self.last_name}'

    def __repr__(self):
        return f'Person({self.uid}, {self.first_name}, {self.last_name}, {self.sex})'

    def set_friends(self, common_friends):
        self.common_friends = common_friends

    def to_json(self):
        links = []
        if self.common_friends is not None:
            for friend in self.common_friends:
                if (friend.uid, self.uid) not in Person.MUTUAL_FRIENDS:
                    links.append({
                        'source': self.uid,
                        'target': friend.uid,
                        'value': len(self.common_friends)
                    })
                    Person.MUTUAL_FRIENDS.add((self.uid, friend.uid))
        node = {
            'id': self.uid,
            'group': self.sex,
            'name': f'{self.first_name} {self.last_name}'
        }

        return {
            'links': links,
            'nodes': node
        }
