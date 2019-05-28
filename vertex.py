class Vertex:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.neighbors = []
        self.color = -1
        self.set_order = -1
        self.colors_domain = []

    def __lt__(self, other):
        return self.number < other.number

    def reset_domain(self, domain):
        self.colors_domain.clear()
        for i in range(len(domain)):
            self.colors_domain.append(i)
        for neighbor in self.neighbors:
            if neighbor.color != -1 and neighbor.color in self.colors_domain:
                self.colors_domain.remove(neighbor.color)
