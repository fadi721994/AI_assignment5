from data import Data
from algorithm import Algorithm
import cProfile, pstats, io


def main():
    algorithm = Algorithm(Data())
    algorithm.run()


# pr = cProfile.Profile()
# pr.enable()
main()
# pr.disable()
# s = io.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print(s.getvalue())