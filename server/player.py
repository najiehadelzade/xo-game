class Player:

    def __init__(self, name, connection, address):
        self.name = name
        self.connection = connection
        self.address = address
        self.room = None
        self.ready = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Player({self.name}, {self.connection}, {self.address})"
