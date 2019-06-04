def valid_color_assignment(vertex, color):
    for neighbor in vertex.neighbors:
        if neighbor.color != -1 and neighbor.color == color:
            return False
    return True


def unset_conflict_set_assignment(vertex):
    for neighbor in vertex.neighbors:
        neighbor.set_order = -1
        neighbor.color = -1
        print("Un-setting assignment for vertex " + str(neighbor.number) + " due to vertex " + str(vertex.number))


def swap_colors(kempe_chain):
    if not kempe_chain:
        return
    color_1 = kempe_chain[0].color
    color_2 = -1
    for vertex in kempe_chain:
        if vertex.color != color_1:
            color_2 = vertex.color
            break
    for vertex in kempe_chain:
        if vertex.color == color_1:
            vertex.color = color_2
        else:
            vertex.color = color_1
