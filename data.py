import os
import argparse
import sys
from graph import Graph
from algorithm_type import AlgorithmType
from search_type import SearchType
from local_search import LocalSearch


class Data:
    def __init__(self):
        self.search_type = SearchType.BACKWARD_OR_FORWARD_SEARCH
        self.algorithm_type = AlgorithmType.BACKTRACKING
        self.local_search = LocalSearch.FEASIBILITY
        self.parse_cmd()

        self.graphs = []
        self.parse_input_dir('./input/')

    def parse_cmd(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-ST', default=1,
                            help='Search type: 0 for backward or forward search and 2 for local search.')
        parser.add_argument('-AT', default=3,
                            help='Algorithm type: 0 for backtracking, 1 for back jumping, 2 for forward checking, '
                                 '3 for arc consistency.')
        parser.add_argument('-LS', default=0,
                            help='Local search: 0 for feasibility, 1 for KEMPE chains and  2 for hybrid.')
        args = parser.parse_args()

        try:
            search_type = int(args.ST)
            if search_type != 0 and search_type != 1:
                print("Search type can only be 0 or 1.")
                sys.exit()
        except ValueError:
            print("Search type can only be 0 or 1.")
            sys.exit()
        self.search_type = SearchType(search_type)

        try:
            algorithm_type = int(args.AT)
            if algorithm_type != 0 and algorithm_type != 1 and algorithm_type != 2 and algorithm_type != 3:
                print("Algorithm type can only be 0, 1, 2 or 3.")
                sys.exit()
        except ValueError:
            print("Algorithm type can only be 0, 1, 2 or 3.")
            sys.exit()
        self.algorithm_type = AlgorithmType(algorithm_type)

        try:
            local_search = int(args.LS)
            if local_search != 0 and local_search != 1 and local_search != 2:
                print("Local search can only be 0, 1 or 2.")
                sys.exit()
        except ValueError:
            print("Local search can only be 0, 1 or 2.")
            sys.exit()
        self.local_search = LocalSearch(local_search)

    def parse_input_dir(self, directory):
        if not os.path.isdir(directory):
            print("\"inputs\" directory doesn't exist. Please create a directory called \"inputs\" at the same folder "
                  "of your executable.")
            return
        empty = True
        for filename in os.listdir(directory):
            empty = False
            self.parse_input_file(directory, filename)
        if empty:
            print("\"inputs\" directory is empty. Please place a graph description file from "
                  "https://mat.gsia.cmu.edu/COLOR03/ from the \"Graph Coloring Instances\" section in the directory")

    def parse_input_file(self, directory, filename):
        with open(directory + filename) as f:
            print("Parsing and creating graph from \"" + filename + "\"")
            graph = Graph(filename, f.readlines())
            self.graphs.append(graph)
