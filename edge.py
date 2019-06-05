class Edge:
    def __init__(self, name, vertex_1, vertex_2):
        self.name = name
        assert(vertex_1.number != vertex_2.number)
        if vertex_1.number > vertex_2.number:
            vertex_1, vertex_2 = vertex_2, vertex_1
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2

    def is_assignment_valid(self):
        for neighbor in self.vertex_1.neighbors:
            if neighbor.color == self.vertex_1.color:
                return False
        for neighbor in self.vertex_2.neighbors:
            if neighbor.color == self.vertex_2.color:
                return False
        return True

    def can_be_satisfied(self, x, y):
        for neighbor in self.vertex_1.neighbors:
            if neighbor.color == x:
                return False
        for neighbor in self.vertex_2.neighbors:
            if neighbor.color == y:
                return False
        return True

    def x_satisfies_y(self, x):
        can_be_satisfied = False
        for y in self.vertex_2.colors_domain:
            if self.can_be_satisfied(x, y):
                can_be_satisfied = True
                break
        return can_be_satisfied

    def remove_inconsistency_values(self):
        removed = False
        for x in self.vertex_1.colors_domain:
            if not self.x_satisfies_y(x):
                self.vertex_1.colors_domain.remove(x)
                removed = True
        return removed
