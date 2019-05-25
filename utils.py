def choose_color(vertex):
    for neighbor in vertex.neighbors:
        if neighbor.color != -1 and neighbor.color in vertex.colors_domain:
            vertex.colors_domain.remove(neighbor.color)
    if not vertex.colors_domain:
        return None
    return vertex.colors_domain[0]
