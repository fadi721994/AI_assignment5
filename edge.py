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

    def x_satisfies_y(self, x):
        can_be_satisfied = False
        self.vertex_1.color = x
        for y in self.vertex_2.colors_domain:
            self.vertex_2.color = y
            if self.is_assignment_valid():
                can_be_satisfied = True
                break
        if not can_be_satisfied:
            self.vertex_1.colors_domain.remove(x)
        self.vertex_1.color = -1
        self.vertex_2.color = -1
        return can_be_satisfied

    def remove_inconsistency_values(self):
        removed = False
        for x in self.vertex_1.colors_domain:
            if not self.x_satisfies_y(x):
                removed = True
        return removed
