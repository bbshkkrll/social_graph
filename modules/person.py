class Person:
    DEFAULT_VALUE = 1
    MUTUAL_FRIENDS = set()

    def __init__(self, data: dict):
        self.uid: int = data['id']
        self.first_name: str = data['first_name']
        self.last_name: str = data['last_name']
        self.sex: int = data['sex']
        self.photo: str = data['photo']
        self.common_friends: [Person] = None

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
                        'source': f'{self.first_name} {self.last_name}',
                        'target': f'{friend.first_name} {friend.last_name}',
                        'value': self.DEFAULT_VALUE
                    })
                    Person.MUTUAL_FRIENDS.add((self.uid, friend.uid))
        node = {
            'id': f'{self.first_name} {self.last_name}',
            'group': self.sex
        }

        return {
            'links': links,
            'nodes': node
        }
