from ChameleonAlgo import *
from util import *

if __name__ == "__main__":
    pprint("in main")
    # file_path = "./data/graphData.txt.orig"
    file_path = "./data/t4.8k.dat"
    k = 2
    min_size = 0.075
    tool = ChameleonAlgo(k, min_size)
    tool.read_Data(file_path)
    tool.connected_graph()
    (edgecuts, parts) = pymetis.part_graph(40, ChameleonAlgo.adj_edges)
    print(parts)
    # tool.make_smaller_cluster(ChameleonAlgo.adj_edges, tool.points)
    # tool.print_cluster(tool.init_cluster)
    # # tool.construct_graph(tool.init_cluster)
    # print("--------------------------------")
    # tool.combine_sub_cluster()
    # tool.print_cluster(tool.result_cluster)
    # tool.construct_graph(tool.result_cluster)