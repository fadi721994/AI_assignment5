import os
from graph import Graph


class Data:
    def __init__(self):
        self.graphs = []
        self.parse_input_dir('./input/')

    def parse_input_dir(self, directory):
        if not os.path.isdir(directory):
            print("\"inputs\" directory doesn't exist.")
            return
        for filename in os.listdir(directory):
            if filename.endswith(".txt") or filename.endswith(".col"):
                self.parse_input_file(directory, filename)
        else:
            print("\"inputs\" directory is empty.")

    def parse_input_file(self, directory, filename):
        with open(directory + filename) as f:
            print("Parsing and creating graph from \"" + filename + "\"")
            graph = Graph(filename, f.readlines())
            self.graphs.append(graph)



