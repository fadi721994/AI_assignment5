import sys
import os
import time
from algorithm_type import AlgorithmType
from search_type import SearchType
from local_search import LocalSearch


class Algorithm:
    def __init__(self, data):
        self.data = data
        algorithm_string = 'Running with '
        if self.data.search_type == SearchType.BACKWARD_OR_FORWARD_SEARCH:
            print("Running a backward/forward search algorithm.")
            if self.data.algorithm_type == AlgorithmType.BACKTRACKING:
                algorithm_string = algorithm_string + 'backtracking'
            elif self.data.algorithm_type == AlgorithmType.BACK_JUMPING:
                algorithm_string = algorithm_string + 'back jumping'
            elif self.data.algorithm_type == AlgorithmType.FORWARD_CHECKING:
                algorithm_string = algorithm_string + 'forward checking'
            else:
                algorithm_string = algorithm_string + 'arc consistency'
        else:
            print("Running a local search algorithm")
            if self.data.local_search == LocalSearch.FEASIBILITY:
                algorithm_string = algorithm_string + 'feasibility'
            elif self.data.local_search == LocalSearch.KEMPE_CHAINS:
                algorithm_string = algorithm_string + 'KEMPE chains'
            else:
                algorithm_string = algorithm_string + 'hybrid algorithm'
        print(algorithm_string)
        if os.path.isfile("./output.txt"):
            os.remove("./output.txt")

    def run(self):
        sys.setrecursionlimit(5000)
        for graph in self.data.graphs:
            with open("output.txt", 'a') as file:
                file.write("==============================================================\n")
                file.write("Solving problem: \"" + graph.name + "\" with " + str(graph.vertices_num) + " vertices and "
                           + str(graph.edges_num) + " edges.\n")
            print("==============================================================")
            print("Solving problem: \"" + graph.name + "\" with " + str(graph.vertices_num) + " vertices and "
                  + str(graph.edges_num) + " edges.")
            graph.start_time = time.time()
            graph.end_time = time.time() + (self.data.max_min * 60)
            if self.data.search_type == SearchType.BACKWARD_OR_FORWARD_SEARCH:
                self.backward_or_forward_search(graph)
            else:
                self.local_search(graph)
            print("Time: " + str(round((time.time() - graph.start_time) * 1000, 5)) + " ms")
            print("States: " + str(graph.states))
            if graph.time_limit_reached:
                print("Time limit reached (3 mins), couldn't finish the run")
                print("\n")
            else:
                graph.validate_solution()
                graph.print_solution()

    def backward_or_forward_search(self, graph):
        colors_num = graph.find_colors_num()
        graph.reset_colors()
        graph.set_domain(colors_num)
        if self.data.algorithm_type == AlgorithmType.BACKTRACKING:
            graph.color_with_backtracking()
        elif self.data.algorithm_type == AlgorithmType.BACK_JUMPING:
            graph.color_with_back_jumping()
        elif self.data.algorithm_type == AlgorithmType.FORWARD_CHECKING:
            graph.color_with_forward_checking()
        else:
            graph.color_with_arc_consistency()

    def local_search(self, graph):
        if self.data.local_search == LocalSearch.FEASIBILITY:
            graph.color_with_feasibility()
        elif self.data.local_search == LocalSearch.KEMPE_CHAINS:
            graph.color_with_kempe_chains()
        else:
            graph.color_with_hybrid()
