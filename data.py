import os
import argparse
import sys
from graph import Graph
from algorithm_type import AlgorithmType


class Data:
    def __init__(self):
        self.algorithm_type = AlgorithmType.BACKTRACKING
        self.parse_cmd()

        self.graphs = []
        self.parse_input_dir('./input/')

    def parse_cmd(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-AT', default=1,
                            help='Algorithm type: 0 for backtracking, 1 for backjumping, 2 for forward checking, '
                                 '3 for arc consistency.')
        args = parser.parse_args()

        try:
            algorithm_type = int(args.AT)
            if algorithm_type != 0 and algorithm_type != 1 and algorithm_type != 2 and algorithm_type != 3:
                print("Algorithm type can only be 0, 1, 2 or 3.")
                sys.exit()
        except ValueError:
            print("Algorithm type can only be 0, 1, 2 or 3.")
            sys.exit()
        self.algorithm_type = AlgorithmType(algorithm_type)

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
