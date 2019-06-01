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

    def remove_color_from_neighbors(self):
        for neighbor in self.neighbors:
            if self.color in neighbor.colors_domain:
                neighbor.colors_domain.remove(self.color)

    def update_neighbors_colors(self, color):
        for neighbor in self.neighbors:
            add_color = True
            for neighbor_neighbor in neighbor.neighbors:
                if color == neighbor_neighbor.color:
                    add_color = False
            if add_color:
                neighbor.colors_domain.append(color)
                neighbor.colors_domain.sort()
