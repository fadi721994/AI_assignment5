import sys
import utils
import random
from edge import Edge
from vertex import Vertex
from operator import attrgetter


class Graph:
    def __init__(self, name, file_lines):
        self.name = name
        self.edges_num = 0
        self.vertices_num = 0
        self.setting_number = 0
        self.edges = []
        self.vertices = []
        self.vertices_numbers = []
        self.colors_domain = []
        self.create_graph(file_lines)
        self.create_unconnected_vertices()
        self.vertices.sort()
        assert(self.edges_num == len(self.edges))

    def create_graph(self, file_lines):
        for line in file_lines:
            line = line.strip()
            if len(line) == 0:
                continue
            first_char = line[0]
            if first_char == 'c':
                continue
            elif first_char == 'p':
                words = line.split()
                self.vertices_num = int(words[2])
                self.edges_num = int(words[3])
            elif first_char == 'e':
                words = line.split()
                if int(words[1]) == int(words[2]):
                    self.edges_num = self.edges_num - 1
                    continue
                vertex_1 = self.create_vertex(int(words[1]))
                vertex_2 = self.create_vertex(int(words[2]))
                edge = Edge(self.name, vertex_1, vertex_2)
                self.edges.append(edge)
                if vertex_2 not in vertex_1.neighbors:
                    vertex_1.neighbors.append(vertex_2)
                if vertex_1 not in vertex_2.neighbors:
                    vertex_2.neighbors.append(vertex_1)

    def create_vertex(self, number):
        vertex = self.get_vertex(number)
        if vertex is None:
            vertex = Vertex(self.name, number)
            self.vertices.append(vertex)
            self.vertices_numbers.append(number)
        return vertex

    def get_vertex(self, number):
        for vertex in self.vertices:
            if vertex.number == number:
                return vertex
        return None

    def create_unconnected_vertices(self):
        if self.vertices_num == len(self.vertices):
            return
        for i in range(self.vertices_num):
            if i + 1 not in self.vertices_numbers:
                self.create_vertex(i + 1)

    def __lt__(self, other):
        return self.vertices_num < other.vertices_num

    def are_all_vertices_colored(self):
        for vertex in self.vertices:
            if vertex.color == -1:
                return False
        return True

    def validate_solution(self):
        if not self.are_all_vertices_colored():
            print("Not all vertices are colored")
            for vertex in self.vertices:
                if vertex.color == -1:
                    print("Vertex " + str(vertex.number) + " is not colored")
            sys.exit()
        for vertex in self.vertices:
            for neighbour in vertex.neighbors:
                if neighbour.color == vertex.color:
                    print("Incorrect solution: vertex " + str(vertex.number) + " and neighbor vertex " +
                          str(neighbour.number) + " have the same color " + str(vertex.color))
                    sys.exit()

    def set_domain(self, domain):
        self.colors_domain.clear()
        for i in range(domain):
            self.colors_domain.append(i)
        for vertex in self.vertices:
            vertex.colors_domain.clear()
            for color in self.colors_domain:
                vertex.colors_domain.append(color)

    def choose_vertex(self, prev_vertex):
        if prev_vertex is not None:
            for neighbor in prev_vertex.neighbors:
                if neighbor.color == -1:
                    return neighbor
        unassigned_vertices = []
        for vertex in self.vertices:
            if vertex.color == -1:
                unassigned_vertices.append(vertex)
        if unassigned_vertices:
            return random.choice(unassigned_vertices)
        return None

    def color_with_backtracking(self, prev_vertex=None):
        vertex = self.choose_vertex(prev_vertex)
        if vertex is None:
            return True
        color = self.choose_color(vertex)
        if color is None:
            return False
        vertex.color = color
        if self.color_with_backtracking(vertex):
            return True
        vertex.color = -1
        for color in self.colors_domain:
            if color not in vertex.colors_domain:
                vertex.colors_domain.append(color)
        vertex.colors_domain.sort()

    def color_with_back_jumping(self, prev_vertex=None):
        vertex = self.choose_vertex(prev_vertex)
        if vertex is None:
            return True
        color = self.choose_color_for_back_jumping(vertex, self.colors_domain)
        if color is None:
            return False
        vertex.color = color
        print("Giving vertex " + str(vertex.number) + " color " + str(vertex.color))
        if self.color_with_back_jumping(vertex):
            return True
        vertex.color = -1
        for color in self.colors_domain:
            if color not in vertex.colors_domain:
                vertex.colors_domain.append(color)
        vertex.colors_domain.sort()

    def print_solution(self):
        print("==============================================================")
        for vertex in self.vertices:
            print("Vertex " + str(vertex.number) + " colored " + str(vertex.color))
        print("\n")

    def reset_colors(self):
        for vertex in self.vertices:
            vertex.color = -1
            for color in self.colors_domain:
                if color not in vertex.colors_domain:
                    vertex.colors_domain.append(color)
            vertex.colors_domain.sort()

    def choose_color(self, vertex):
        for neighbor in vertex.neighbors:
            if neighbor.color != -1 and neighbor.color in vertex.colors_domain:
                vertex.colors_domain.remove(neighbor.color)
        if not vertex.colors_domain:
            return None
        vertex.set_order = self.setting_number
        self.setting_number = self.setting_number + 1
        return vertex.colors_domain[0]

    def choose_color_for_back_jumping(self, vertex, original_colors_domain):
        for neighbor in vertex.neighbors:
            if neighbor.color != -1 and neighbor.color in vertex.colors_domain:
                vertex.colors_domain.remove(neighbor.color)
        if not vertex.colors_domain:
            last_set_neighbor = max(vertex.neighbors, key=attrgetter('set_order'))
            print("Removing from vertex " + str(last_set_neighbor.number) + " color " + str(last_set_neighbor.color))
            last_set_neighbor.color = -1
            first_set_neighbor = min(vertex.neighbors, key=attrgetter('set_order'))
            last_set_neighbor.set_order = first_set_neighbor.set_order - 1
            for color in original_colors_domain:
                if color not in last_set_neighbor.colors_domain:
                    last_set_neighbor.colors_domain.append(color)
                if color not in vertex.colors_domain:
                    vertex.colors_domain.append(color)
            return self.choose_color_for_back_jumping(vertex, original_colors_domain)
        return vertex.colors_domain[0]
