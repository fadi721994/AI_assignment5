class Vertex:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.neighbors = []
        self.color = -1
        self.colors_domain = []

    def __lt__(self, other):
        return self.number < other.number
