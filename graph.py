import sys
import utils
import random
import math
from edge import Edge
from vertex import Vertex


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
        self.max_iter = 1000

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

    def validate_solution(self, print_data=True):
        if not self.are_all_vertices_colored():
            if print_data:
                print("Not all vertices are colored")
            for vertex in self.vertices:
                if vertex.color == -1 and print_data:
                    print("Vertex " + str(vertex.number) + " is not colored")
            sys.exit()
        for vertex in self.vertices:
            for neighbour in vertex.neighbors:
                if neighbour.color == vertex.color:
                    if print_data:
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

    def choose_vertex(self, prev_vertex, neighbors_first=True):
        if prev_vertex is not None and neighbors_first:
            unassigned_neighbors = []
            for neighbor in prev_vertex.neighbors:
                if neighbor.color == -1:
                    unassigned_neighbors.append(neighbor)
            if unassigned_neighbors:
                return random.choice(unassigned_neighbors)
        unassigned_vertices = []
        for vertex in self.vertices:
            if vertex.color == -1:
                unassigned_vertices.append(vertex)
        if unassigned_vertices:
            return random.choice(unassigned_vertices)
        return None

    def color_with_backtracking(self, prev_vertex=None):
        vertex = self.choose_vertex(prev_vertex, True)
        if vertex is None:
            return True
        for color in vertex.colors_domain:
            if utils.valid_color_assignment(vertex, color):
                vertex.color = color
                if self.color_with_backtracking(vertex):
                    return True
                vertex.color = -1
        return False

    def color_with_back_jumping(self, prev_vertex=None):
        vertex = self.choose_vertex(prev_vertex, True)
        if vertex is None:
            return True
        self.set_order_number(vertex)
        for color in self.colors_domain:
            if utils.valid_color_assignment(vertex, color):
                vertex.color = color
                if self.color_with_back_jumping(vertex):
                    return True
                vertex.color = -1
        self.unset_order_number(vertex)
        utils.unset_conflict_set_latest_assignment(vertex)
        if self.color_with_back_jumping(prev_vertex):
            return True
        return False

    def color_with_forward_checking(self, prev_vertex=None):
        vertex = self.choose_vertex(prev_vertex, True)
        if vertex is None:
            return True
        for color in vertex.colors_domain:
            if utils.valid_color_assignment(vertex, color):
                # print("Vertex " + str(vertex.number) + " colored " + str(color))
                vertex.color = color
                vertex.remove_color_from_neighbors()
                if self.color_with_forward_checking(vertex):
                    return True
                # print("Vertex " + str(vertex.number) + " uncolored " + str(color))
                vertex.color = -1
                vertex.update_neighbors_colors(color)
        return False

    def ac3_algorithm(self):
        for edge in self.edges:
            if edge.remove_inconsistency_values():
                for neighbor in edge.vertex_1.neighbors:
                    self.edges.append(Edge(self.name, edge.vertex_1, neighbor))

    def color_with_arc_consistency(self):
        self.ac3_algorithm()
        return self.color_with_backtracking(prev_vertex=None)

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

    def set_order_number(self, vertex):
        vertex.set_order = self.setting_number
        self.setting_number = self.setting_number + 1

    def unset_order_number(self, vertex):
        vertex.set_order = -1
        self.setting_number = self.setting_number - 1

    def used_colors_number(self):
        used_colors = []
        for vertex in self.vertices:
            if vertex.color not in used_colors and vertex.color != -1:
                used_colors.append(vertex.color)
        return len(used_colors)

    def get_largest_neighbors_num(self):
        neighbors_num = 0
        for vertex in self.vertices:
            if neighbors_num < len(vertex.neighbors):
                neighbors_num = len(vertex.neighbors)
        return neighbors_num

    def find_colors_num(self):
        colors_num = self.get_largest_neighbors_num()
        print("Setting domain to " + str(colors_num) + " colors (number of maximum neighbors)")
        self.set_domain(colors_num)
        self.color_with_forward_checking()
        used_colors = self.used_colors_number()
        print("Used colors number is " + str(used_colors) + "/" + str(colors_num))
        return used_colors

    def color_with_feasibility(self):
        colors_num = self.get_largest_neighbors_num()
        print("Setting domain to " + str(colors_num) + " colors (number of maximum neighbors)")
        self.set_domain(colors_num)
        self.greedy_coloring_algorithm()
        self.compress_colors()
        used_colors = self.used_colors_number()
        print("Used colors number is " + str(used_colors) + "/" + str(colors_num))
        success = True
        while success:
            self.replace_color()
            self.compress_colors(False)
            success = self.minimum_conflicts()
            if success:
                print("Color removed successfully and graph repainted. Down to " +
                      str(self.used_colors_number()) + " colors")
            else:
                print("Color cannot be removed, minimum number of colors is " + str(self.used_colors_number() + 1))
        used_colors = self.used_colors_number() + 1
        self.set_domain(used_colors)
        self.minimum_conflicts()

    def minimum_conflicts(self):
        curr_iter = 0
        while not self.is_solution_valid() and curr_iter < self.max_iter:
            curr_iter = curr_iter + 1
            vertex = self.get_problematic_vertex()
            color = self.get_least_problematic_color(vertex)
            vertex.color = color
        return self.is_solution_valid()

    def get_least_problematic_color(self, vertex):
        minimum_conflicts = math.inf
        best_color = -1
        for color in self.colors_domain:
            conflicts = 0
            for neighbor in vertex.neighbors:
                if neighbor.color == color:
                    conflicts = conflicts + 1
            if conflicts < minimum_conflicts:
                minimum_conflicts = conflicts
                best_color = color
        return best_color

    def get_problematic_vertex(self):
        problematic_vertices = []
        for vertex in self.vertices:
            for neighbor in vertex.neighbors:
                if vertex.color == neighbor.color and vertex not in problematic_vertices:
                    problematic_vertices.append(vertex)
        return random.choice(problematic_vertices)

    def is_solution_valid(self):
        for vertex in self.vertices:
            if vertex.color == -1:
                return False
            for neighbor in vertex.neighbors:
                if vertex.color == neighbor.color:
                    return False
        return True

    def compress_colors(self, validate=True):
        domain = []
        for i in self.colors_domain:
            domain.append(i)
        for color in domain:
            if not self.is_color_used(color):
                self.colors_domain.remove(color)
        self.colors_domain.sort()
        for i in range(len(self.colors_domain)):
            if i != self.colors_domain[i]:
                self.colors_domain.append(i)
                previous_color = self.colors_domain[i]
                self.colors_domain.remove(self.colors_domain[i])
                self.update_vertex_color(previous_color, i)
        if validate:
            self.validate_solution(False)

    def update_vertex_color(self, from_color, to_color):
        for vertex in self.vertices:
            if vertex.color == from_color:
                vertex.color = to_color

    def is_color_used(self, color):
        for vertex in self.vertices:
            if vertex.color == color:
                return True
        return False

    def replace_color(self):
        color = self.get_least_used_color()
        print("Trying to remove color " + str(color) + " and compressing assignments")
        self.colors_domain.remove(color)
        for vertex in self.vertices:
            if vertex.color == color:
                vertex.color = random.choice(self.colors_domain)

    def get_least_used_color(self):
        colors_num = {}
        min_color = math.inf
        chosen_color = -1
        for color in self.colors_domain:
            colors_num[color] = 0
        for vertex in self.vertices:
            colors_num[vertex.color] = colors_num[vertex.color] + 1
        for entry in colors_num:
            if 0 < colors_num[entry] < min_color:
                min_color = colors_num[entry]
                chosen_color = entry
        return chosen_color

    def greedy_coloring_algorithm(self, prev_vertex=None):
        vertex = self.choose_vertex(prev_vertex, False)
        if vertex is None:
            return True
        while True:
            color = random.choice(self.colors_domain)
            if utils.valid_color_assignment(vertex, color):
                vertex.color = color
                if self.greedy_coloring_algorithm(vertex):
                    return True
                vertex.color = -1
        return False
