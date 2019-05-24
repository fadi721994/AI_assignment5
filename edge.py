class Edge:
    def __init__(self, name, vertex_1, vertex_2):
        self.name = name
        assert(vertex_1.number != vertex_2.number)
        if vertex_1.number > vertex_2.number:
            vertex_1, vertex_2 = vertex_2, vertex_1
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2
