import sys
import utils
import random
import time
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
        self.max_iter = 2000
        self.states = 0
        self.start_time = 0
        self.end_time = 0
        self.time_limit_reached = False

    # Build the graph
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

    # Build a vertex
    def create_vertex(self, number):
        vertex = self.get_vertex(number)
        if vertex is None:
            vertex = Vertex(self.name, number)
            self.vertices.append(vertex)
            self.vertices_numbers.append(number)
        return vertex

    # Given a vertex number, return the vertex
    def get_vertex(self, number):
        for vertex in self.vertices:
            if vertex.number == number:
                return vertex
        return None

    # If the graph is not a single component, add the remaining vertices
    def create_unconnected_vertices(self):
        if self.vertices_num == len(self.vertices):
            return
        for i in range(self.vertices_num):
            if i + 1 not in self.vertices_numbers:
                self.create_vertex(i + 1)

    def __lt__(self, other):
        return self.vertices_num < other.vertices_num

    # Check if all vertices are colored
    def are_all_vertices_colored(self):
        for vertex in self.vertices:
            if vertex.color == -1:
                return False
        return True

    # Make sure a solution is valid
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

    # Set a domain to the given domain
    def set_domain(self, domain):
        self.colors_domain.clear()
        for i in range(domain):
            self.colors_domain.append(i)
        for vertex in self.vertices:
            vertex.colors_domain.clear()
            for color in self.colors_domain:
                vertex.colors_domain.append(color)

    # Choose a vertex given a previous vertex. You can choose randomly or prefer the previous vertex neighbors
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

    # Color the graph using backtracking
    def color_with_backtracking(self, prev_vertex=None):
        if time.time() > self.end_time:
            self.time_limit_reached = True
            return True
        vertex = self.choose_vertex(prev_vertex, True)
        if vertex is None:
            return True
        for color in vertex.colors_domain:
            self.states = self.states + 1
            if utils.valid_color_assignment(vertex, color):
                vertex.color = color
                if self.color_with_backtracking(vertex):
                    return True
                vertex.color = -1
        return False

    # Color the graph using back jumping
    def color_with_back_jumping(self, prev_vertex=None):
        if time.time() > self.end_time:
            self.time_limit_reached = True
            return True
        vertex = self.choose_vertex(prev_vertex, True)
        if vertex is None:
            return True
        self.set_order_number(vertex)
        for color in self.colors_domain:
            self.states = self.states + 1
            if utils.valid_color_assignment(vertex, color):
                vertex.color = color
                if self.color_with_back_jumping(vertex):
                    return True
                vertex.color = -1
        self.unset_order_number(vertex)
        utils.unset_conflict_set_assignment(vertex)
        return self.color_with_back_jumping(prev_vertex)

    # Color the graph using forward checking
    def color_with_forward_checking(self, prev_vertex=None):
        if time.time() > self.end_time:
            self.time_limit_reached = True
            return True
        vertex = self.choose_vertex(prev_vertex, True)
        if vertex is None:
            return True
        for color in vertex.colors_domain:
            self.states = self.states + 1
            if utils.valid_color_assignment(vertex, color):
                vertex.color = color
                vertex.remove_color_from_neighbors()
                if self.color_with_forward_checking(vertex):
                    return True
                vertex.color = -1
                vertex.update_neighbors_colors(color)
        return False

    # Run the AC3 algorithm
    def ac3_algorithm(self, edges=None):
        if edges is None:
            edges = self.edges
        arc_consistency_edges = []
        for edge in edges:
            arc_consistency_edges.append(Edge(edge.name, edge.vertex_1, edge.vertex_2))
        while len(arc_consistency_edges) != 0:
            edge = arc_consistency_edges[0]
            arc_consistency_edges.remove(edge)
            if edge.remove_inconsistency_values():
                for neighbor in edge.vertex_1.neighbors:
                    arc_consistency_edges.append(Edge(edge.name, edge.vertex_1, neighbor))

    # Color the graph using arc consistency
    def color_with_arc_consistency(self, prev_vertex=None):
        if time.time() > self.end_time:
            self.time_limit_reached = True
            return True
        vertex = self.choose_vertex(prev_vertex, True)
        if vertex is None:
            return True
        for color in vertex.colors_domain:
            self.states = self.states + 1
            if utils.valid_color_assignment(vertex, color):
                vertex.color = color
                self.ac3_algorithm()
                if self.color_with_arc_consistency(vertex):
                    return True
                vertex.color = -1
        return False

    # print a solution
    def print_solution(self):
        with open("output.txt", 'a') as file:
            file.write("+++++++++++++++++++++++++++++++++++++++++++++++++++")
            file.write("Solution for " + self.name + '\n')
            for vertex in self.vertices:
                file.write("Vertex " + str(vertex.number) + " colored " + str(vertex.color) + '\n')
            print("\n")

    # Reset color domains and remove coloring from vertices
    def reset_colors(self):
        for vertex in self.vertices:
            vertex.color = -1
            for color in self.colors_domain:
                if color not in vertex.colors_domain:
                    vertex.colors_domain.append(color)
            vertex.colors_domain.sort()

    # Set vertex coloring order number
    def set_order_number(self, vertex):
        vertex.set_order = self.setting_number
        self.setting_number = self.setting_number + 1

    # Unset vertex coloring order number
    def unset_order_number(self, vertex):
        vertex.set_order = -1
        self.setting_number = self.setting_number - 1

    # Return how many colors are used
    def used_colors_number(self):
        used_colors = []
        for vertex in self.vertices:
            if vertex.color not in used_colors and vertex.color != -1:
                used_colors.append(vertex.color)
        return len(used_colors)

    # Return the largest number of neighbors a vertex has in the graph
    def get_largest_neighbors_num(self):
        neighbors_num = 0
        for vertex in self.vertices:
            if neighbors_num < len(vertex.neighbors):
                neighbors_num = len(vertex.neighbors)
        return neighbors_num

    # Find the least colors number that can be given by running forward checking
    def find_colors_num(self):
        colors_num = self.get_largest_neighbors_num()
        print("Setting domain to " + str(colors_num) + " colors (number of maximum neighbors)")
        self.set_domain(colors_num)
        self.color_with_forward_checking()
        self.states = 0
        used_colors = self.used_colors_number()
        print("Used colors number is " + str(used_colors) + "/" + str(colors_num))
        self.set_domain(used_colors)
        return used_colors

    # Color the graph with feasibility
    def color_with_feasibility(self):
        colors_num = self.get_largest_neighbors_num()
        print("Setting domain to " + str(colors_num) + " colors (number of maximum neighbors)")
        self.set_domain(colors_num)
        self.greedy_coloring_algorithm()
        self.compress_colors()
        used_colors = self.used_colors_number()
        print("Used colors number is " + str(used_colors) + "/" + str(colors_num))
        success = True
        colors_map = {}
        while success:
            self.replace_color()
            self.compress_colors(False)
            success = self.minimum_conflicts()
            if success:
                colors_map.clear()
                with open("output.txt", 'a') as file:
                    file.write("Color removed successfully and graph repainted. Down to " +
                               str(self.used_colors_number()) + " colors\n")
                for vertex in self.vertices:
                    colors_map[vertex.number] = vertex.color
            else:
                with open("output.txt", 'a') as file:
                    file.write("Color cannot be removed, minimum number of colors is "
                               + str(self.used_colors_number() + 1) + '\n')
        used_colors = self.used_colors_number() + 1
        print("Used colors are " + str(used_colors))
        self.set_domain(used_colors)
        for vertex in self.vertices:
            vertex.color = colors_map[vertex.number]

    # Run minimum conflicts local search
    def minimum_conflicts(self):
        curr_iter = 0
        while not self.is_solution_valid() and curr_iter < self.max_iter:
            self.states = self.states + 1
            curr_iter = curr_iter + 1
            vertex = self.get_problematic_vertex()
            color = self.get_least_problematic_color(vertex)
            vertex.color = color
        return self.is_solution_valid()

    # Get the color that can be given to a vertex which provides the least amount of conflicts
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

    # Return a single problematic vertex (bad edge)
    def get_problematic_vertex(self):
        problematic_vertices = []
        for vertex in self.vertices:
            for neighbor in vertex.neighbors:
                if vertex.color == neighbor.color and vertex not in problematic_vertices:
                    problematic_vertices.append(vertex)
        return random.choice(problematic_vertices)

    # Check if a solution is valid
    def is_solution_valid(self):
        for vertex in self.vertices:
            if vertex.color == -1:
                return False
            for neighbor in vertex.neighbors:
                if vertex.color == neighbor.color:
                    return False
        return True

    # Compress colors to a consecutive domain (example: [0,4,6] -> [0,1,2])
    def compress_colors(self, validate=True):
        domain = []
        self.colors_domain.sort()
        for i in self.colors_domain:
            domain.append(i)
        for color in domain:
            if not self.is_color_used(color):
                self.colors_domain.remove(color)
        for i in range(len(self.colors_domain)):
            if i != self.colors_domain[i]:
                self.colors_domain.append(i)
                previous_color = self.colors_domain[i]
                self.colors_domain.remove(self.colors_domain[i])
                self.update_vertex_color(previous_color, i)
                self.colors_domain.sort()
        if validate:
            self.validate_solution(False)

    # Update all vertices with color X to color Y
    def update_vertex_color(self, from_color, to_color):
        for vertex in self.vertices:
            if vertex.color == from_color:
                vertex.color = to_color

    # Check if a color is used in the graph
    def is_color_used(self, color):
        for vertex in self.vertices:
            if vertex.color == color:
                return True
        return False

    # Remove a random color and randomly reassign colors to the vertices that were given the original color
    def replace_color(self):
        color = random.choice(self.colors_domain)
        print("Trying to remove color " + str(color) + " and compressing assignments")
        self.colors_domain.remove(color)
        for vertex in self.vertices:
            if vertex.color == color:
                vertex.color = random.choice(self.colors_domain)

    # Return the least used color
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

    # Color the graph with a greedy algorithm
    def greedy_coloring_algorithm(self, prev_vertex=None):
        vertex = self.choose_vertex(prev_vertex, False)
        if vertex is None:
            return True
        while True:
            color = random.choice(self.colors_domain)
            if utils.valid_color_assignment(vertex, color):
                self.states = self.states + 1
                vertex.color = color
                if self.greedy_coloring_algorithm(vertex):
                    return True
                vertex.color = -1
        return False

    # Color the graph with KEMPE chains
    def color_with_kempe_chains(self):
        colors_num = self.get_largest_neighbors_num()
        print("Setting domain to " + str(colors_num) + " colors (number of maximum neighbors)")
        self.set_domain(colors_num)
        self.greedy_coloring_algorithm()
        self.compress_colors()
        used_colors = self.used_colors_number()
        print("Used colors number is " + str(used_colors) + "/" + str(colors_num))
        success = True
        while success:
            success = self.kempe_chains()
            if success:
                print("Color removed successfully and graph repainted. Down to " +
                      str(self.used_colors_number()) + " colors")
            else:
                print("Color cannot be removed, minimum number of colors is " + str(self.used_colors_number() + 1))
        used_colors = self.used_colors_number() + 1
        self.set_domain(used_colors)
        self.reset_colors()
        return self.color_with_forward_checking(None)

    # Run kempe chains
    def kempe_chains(self):
        color_groups = self.color_groups()
        color = self.get_least_used_color()
        # print("Trying to remove color " + str(color) + " and compressing assignments")
        self.colors_domain.remove(color)
        return self.remove_smallest_group(color_groups)

    # Remove the color that is least used in the graph
    def remove_smallest_group(self, color_groups):
        smallest_group = min(color_groups, key=len)
        color_groups.remove(smallest_group)
        color_groups.sort(key=lambda s: len(s))
        colors = []
        for group in color_groups:
            colors.append(group[0].color)
        for vertex in smallest_group:
            colored = False
            for color in reversed(colors):
                can_be_colored = True
                for neighbor in vertex.neighbors:
                    self.states = self.states + 1
                    if neighbor.color == color:
                        can_be_colored = False
                        break
                if can_be_colored:
                    vertex.color = color
                    colored = True
                    break
            if not colored:
                return False
        self.compress_colors()
        return True

    # Get all color groups
    def color_groups(self):
        color_groups = []
        self.compress_colors()
        for i in self.colors_domain:
            color_groups.append([])
        for vertex in self.vertices:
            group = color_groups[vertex.color]
            group.append(vertex)
            color_groups[vertex.color] = group
        return color_groups

    # Remove the smallest group and reassign colors, then if there are any conflicts, run hill climbing to solve them
    def force_remove_smallest_group(self, color_groups):
        smallest_group = min(color_groups, key=len)
        smallest_color = smallest_group[0].color
        color_groups.remove(smallest_group)
        color_groups.sort(key=lambda s: len(s))
        colors = []
        for group in color_groups:
            colors.append(group[0].color)
        for vertex in smallest_group:
            for color in reversed(colors):
                can_be_colored = True
                for neighbor in vertex.neighbors:
                    self.states = self.states + 1
                    if neighbor.color == color:
                        can_be_colored = False
                        break
                if can_be_colored:
                    vertex.color = color
                    break
        for vertex in smallest_group:
            if vertex.color == smallest_color:
                vertex.color = random.choice(colors)
        return self.hill_climbing(colors)

    # Color the graph with hybrid
    def color_with_hybrid(self):
        colors_num = self.get_largest_neighbors_num()
        print("Setting domain to " + str(colors_num) + " colors (number of maximum neighbors)")
        self.set_domain(colors_num)
        self.greedy_coloring_algorithm()
        used_colors = self.used_colors_number()
        print("Used colors number is " + str(used_colors) + "/" + str(colors_num))
        success = True
        while success:
            self.compress_colors()
            self.set_domain(self.used_colors_number())
            color_groups = self.color_groups()
            color = self.get_least_used_color()
            self.colors_domain.remove(color)
            success = self.force_remove_smallest_group(color_groups)
            if success:
                print("Color removed successfully and graph repainted. Down to " +
                      str(self.used_colors_number()) + " colors")
            else:
                print("Color cannot be removed, minimum number of colors is " + str(self.used_colors_number() + 1))
        used_colors = self.used_colors_number() + 1
        print("Used colors are " + str(used_colors))
        self.set_domain(used_colors)
        self.reset_colors()
        return self.color_with_forward_checking(None)

    # Return all conflicted edges
    def get_all_bad_edges(self):
        bad_edges = []
        for vertex in self.vertices:
            for neighbor in vertex.neighbors:
                if neighbor.color == vertex.color:
                    bad_edges.append(vertex)
        return bad_edges

    # Run hill climbing
    def hill_climbing(self, colors):
        bad_edges = self.get_all_bad_edges()
        if not bad_edges:
            return True
        for edge in bad_edges:
            for color in colors:
                can_assign_color = True
                for neighbor in edge.neighbors:
                    self.states = self.states + 1
                    if neighbor.color == color:
                        can_assign_color = False
                if can_assign_color:
                    edge.color = color
                    break
        return self.is_solution_valid()
