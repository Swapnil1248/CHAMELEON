import ChameleonAlgo as ca
from util import *
import copy
import sys

class Cluster:

    def __init__(self, id, points):
        self.id = id
        self.points = points
        self.weight_sum = 0.0
        self.cluster_graph = []

    def __hash__(self):
        return hash(self.id, self.points)

    def __eq__(self, other):
        return (self.id, self.points) == (other.id, other.points)

    def __ne__(self, other):
        return not(self == other)

    def calculate_internal_weight(self):
        self.weight_sum = 0.0
        for p1 in self.points:
            for p2 in self.points:
                id1 = p1.id
                id2 = p2.id
                if id1 < id2 and ca.ChameleonAlgo.edges[id1][id2] == 1:
                    self.weight_sum += 1.0 / ca.ChameleonAlgo.weights[id1][id2]


        return self.weight_sum


    def calculate_absolute_closeness(self, other_cluster):
        pprint("in calculate closeness")
        count = 0
        point_list_1 = copy.deepcopy(self.points)
        point_list_2 = copy.deepcopy(other_cluster.points)
        distance = 0.0
        for p1 in point_list_1:
            for p2 in point_list_2:
                id1 = p1.id
                id2 = p2.id
                if ca.ChameleonAlgo.edges[id1][id2] == 1:
                    count += 1
                    distance += 1.0 / ca.ChameleonAlgo.weights[id1][id2]

        return (distance, count)

    def calculate_nearest_edges(self, other, n):
        pprint("in calculate nearest")
        count = 0
        point1 = None
        point2 = None
        edge_list = []
        point_list_1 = copy.deepcopy(self.points)
        point_list_2 = copy.deepcopy(other.points)

        while count < n:
            temp_edge = []
            temp_edge.append(0)
            temp_edge.append(0)
            min_distance = sys.maxsize
            for p1 in point_list_1:
                for p2 in point_list_2:
                    distance = p1.euclidean_distance(p2)
                    if (distance < min_distance):
                        point1 = p1
                        point2 = p2
                        temp_edge[0] = p1.id
                        temp_edge[1] = p2.id

            point_list_1.remove(point1)
            point_list_2.remove(point2)
            edge_list.append(temp_edge)
            count += 1
        return edge_list

