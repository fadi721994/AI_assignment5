from algorithm_type import AlgorithmType


class Algorithm:
    def __init__(self, data):
        self.data = data
        algorithm_string = 'Running with '
        if self.data.algorithm_type == AlgorithmType.BACKTRACKING:
            algorithm_string = algorithm_string + 'backtracking'
        elif self.data.algorithm_type == AlgorithmType.BACK_JUMPING:
            algorithm_string = algorithm_string + 'back jumping'
        elif self.data.algorithm_type == AlgorithmType.FORWARD_CHECKING:
            algorithm_string = algorithm_string + 'forward checking'
        else:
            algorithm_string = algorithm_string + 'arc consistency'
        print(algorithm_string)

    def run(self):
        for graph in self.data.graphs:
            print("==============================================================")
            print("Solving problem: \"" + graph.name + "\"")
            colors_num = 3
            solution_found = False
            while not solution_found:
                print("Setting domain to " + str(colors_num) + " colors")
                graph.set_domain(colors_num)
                graph.reset_colors()
                if self.data.algorithm_type == AlgorithmType.BACKTRACKING:
                    solution_found = graph.color_with_backtracking()
                # elif self.data.algorithm_type == AlgorithmType.BACK_JUMPING:
                #     graph.color_with_back_jumping()
                # elif self.data.algorithm_type == AlgorithmType.FORWARD_CHECKING:
                #     graph.color_with_back_jumping()
                # else:
                #     graph.color_with_arc_consistency()
                colors_num = colors_num + 1
            graph.validate_solution()
            graph.print_solution()

