from operator import attrgetter


def valid_color_assignment(vertex, color):
    for neighbor in vertex.neighbors:
        if neighbor.color != -1 and neighbor.color == color:
            return False
    return True


def unset_conflict_set_latest_assignment(vertex):
    last_set_neighbor = max(vertex.neighbors, key=attrgetter('set_order'))
    last_set_neighbor.set_order = -1
    last_set_neighbor.color = -1
    print("Un-setting assignment for vertex " + str(last_set_neighbor.number) + " due to vertex " + str(vertex.number))

