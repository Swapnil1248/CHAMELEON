from util import *
from Point import *
from math import *
import copy
from Cluster import Cluster
import sys
import pymetis
import networkx as nx
import matplotlib.pyplot as plt
import random
from heapq import heappush, heappop

class ToMergeCluster:
    def __init__(self, cluster_1, cluster_2, similarity):
        self.cluster_1 = cluster_1
        self.cluster_2 = cluster_2
        self.similarity = similarity

    def __cmp__(self, other):
        return cmp(other.similarity, self.similarity)

    def __lt__(self, other):
        return other.similarity < self.similarity

class ChameleonAlgo:
    edges = []
    weights = []
    adj_edges = []
    cluster_index = 0

    def __init__(self, k, min_size):
        self.k = k
        self.min_size = min_size
        self.points = []
        self.init_cluster = []
        self.result_cluster = []
        self.num_points = 0

    def read_Data(self, file_name):
        pprint("in read data")
        # read file and store in points list
        self.file_name = file_name
        i = 0
        for line in open(self.file_name, "r").readlines():
            a, b = map(float, line.split(" "))
            self.points.append(Point(i, a, b))
            i += 1

        self.num_points = i #len(self.points)
        self.min_size = self.min_size * self.num_points

        temp_list = []
        for i in range(self.num_points):
            temp_list.append(0.0)
            ChameleonAlgo.adj_edges.append(set())

        for i in range(self.num_points):
            ChameleonAlgo.weights.append(copy.deepcopy(temp_list))
            ChameleonAlgo.edges.append(copy.deepcopy(temp_list))

    def choose_cluster_to_combine(self):
        heap = []
        for i in range(len(self.init_cluster)):
            for j in range(len(self.init_cluster)):
                if i != j:
                    metric = self.calculate_metric_function(self.init_cluster[i], self.init_cluster[j], 2)
                    heappush(heap, ToMergeCluster(i, j, metric))
        if len(heap) == 0:
            return None
        return heappop(heap)

    def combine_cluster(self, poped_ToMergeCluster):
        if poped_ToMergeCluster.similarity == 0:
            return False
        else:
            cluster1 = self.init_cluster[poped_ToMergeCluster.cluster_1]
            cluster2 = self.init_cluster[poped_ToMergeCluster.cluster_2]
            self.init_cluster.remove(cluster2)
            self.connect_cluster_to_cluster(cluster1, cluster2)
            to_add = len(cluster1.points)
            cluster1.points.extend(cluster2.points)
            for point in cluster2.cluster_graph:
                new_point = []
                if len(point) != 0:
                    new_point = map(lambda x: to_add + x, iter(point))
                cluster1.cluster_graph.append(new_point)
            return True

    def combine_sub_cluster(self):
        while(True):
            poped_ToMergeCluster = self.choose_cluster_to_combine()
            if poped_ToMergeCluster is None:
                break
            else:
                res = self.combine_cluster(poped_ToMergeCluster)
                if res == False:
                    break
            print("############################")
            self.print_cluster(self.init_cluster)
            self.construct_graph(self.init_cluster)


    # def combine_sub_cluster(self):
    #     self.result_cluster = []
    #     # while len(self.result_cluster) <= 10 and len(self.init_cluster) > 0:
    #     while len(self.init_cluster) > 0:
    #         # print(len(self.result_cluster))
    #         cluster = self.init_cluster[0]
    #         self.combine_and_remove(cluster, self.init_cluster)
    #
    #
    # def combine_and_remove(self, cluster, cluster_list):
    #     cluster1 = None
    #     cluster2 = None
    #     max_metric = 0
    #
    #     for _cluster in cluster_list:
    #         if _cluster.id != cluster.id:
    #             metric = self.calculate_metric_function(cluster, _cluster,2) # alpha
    #             if metric > max_metric:
    #                 max_metric = metric
    #                 cluster1 = cluster
    #                 cluster2 = _cluster
    #
    #     print(max_metric)
    #     if max_metric > 0:
    #     # if max_metric != -sys.maxsize and max_metric > 0:
    #         cluster_list.remove(cluster2)
    #         self.connect_cluster_to_cluster(cluster1, cluster2)
    #         to_add = len(cluster1.points)
    #         cluster1.points.extend(cluster2.points)
    #         for point in cluster2.cluster_graph:
    #             new_point = []
    #             if len(point) != 0:
    #                 new_point = map( lambda x: to_add + x, iter(point))
    #             cluster1.cluster_graph.append(new_point)
    #     else:
    #         cluster_list.remove(cluster)
    #         self.result_cluster.append(cluster)


    def connect_cluster_to_cluster(self, c1, c2):
        connected_edges = c1.calculate_nearest_edges(c2, 1)
        for a,b in connected_edges:
            ChameleonAlgo.edges[a][b] = 1
            ChameleonAlgo.edges[b][a] = 1

    def connected_graph(self):
        pprint("in connected graph")
        for i in range(self.num_points):
            for j in range(self.num_points):

                p1 = self.points[i]
                p2 = self.points[j]

                distance = p1.euclidean_distance(p2)
                if distance == 0:
                    ChameleonAlgo.weights[i][j] = 0
                else:
                    ChameleonAlgo.weights[i][j] = 1.0 / distance

        for i in range(self.num_points):
            temp_weight = ChameleonAlgo.weights[i]
            ids = self.sort_weight_array(temp_weight)

            for j in range(len(ids)):
                if j < self.k:
                    id1 = i
                    id2 = ids[j]
                    ChameleonAlgo.adj_edges[id1].add(id2)
                    ChameleonAlgo.adj_edges[id2].add(id1)
                    ChameleonAlgo.edges[id1][id2] = 1
                    ChameleonAlgo.edges[id2][id1] = 1
                else:
                    break
        for i in range(self.num_points):
            ChameleonAlgo.adj_edges[i] = list(ChameleonAlgo.adj_edges[i])


    def sort_weight_array(self, array):
        pprint("in sort weight array")
        copy_array = copy.deepcopy(array)
        ids = []
        for i in range(self.num_points):
            ids.append(0)
            max_weight = -1
            for j in range(len(copy_array)):
                if copy_array[j] > max_weight:
                    max_weight = copy_array[j]
                    temp_index = j

            ids[i] = temp_index
            copy_array[temp_index] = -1

        return ids

    def make_smaller_cluster(self, graph, points):
        pprint("in make smaller cluster")
        left_num , right_num, point_list_left, point_list_right, left_graph, right_graph = self.divide_cluster(graph, points)
        if left_num > self.min_size:
            self.make_smaller_cluster(left_graph, point_list_left)
        else:
            pprint("assign it to cluster")
            cluster = Cluster(ChameleonAlgo.cluster_index, point_list_left)
            self.init_cluster.append(cluster)
            cluster.cluster_graph = left_graph
            ChameleonAlgo.cluster_index += 1

        if right_num > self.min_size:
            self.make_smaller_cluster(right_graph, point_list_right)
        else:
            pprint("assign it to cluster")
            cluster = Cluster(ChameleonAlgo.cluster_index, point_list_right)
            self.init_cluster.append(cluster)
            cluster.cluster_graph = right_graph
            ChameleonAlgo.cluster_index += 1

    def divide_cluster(self, adj_list, points):
        pprint("in divide cluster")
        reverse_point = dict()
        i = 0
        for point in points:
            reverse_point[(point.x, point.y)] = i
            i+=1

        (edgecuts, parts) = pymetis.part_graph(2, adj_list)
        left_num = 0
        right_num = 0
        point_list_left = []
        point_list_right = []
        left_graph = []
        right_graph = []
        left_dict = dict()
        right_dict = dict()
        for i in range(len(parts)):
            if parts[i] == 0:
                left_dict[(points[i].x, points[i].y)] = left_num
                left_num += 1
                point_list_left.append(points[i])
                left_graph.append([])

            else:
                right_dict[(points[i].x, points[i].y)] = right_num
                right_num += 1
                point_list_right.append(points[i])
                right_graph.append([])

        i = 0
        for point in point_list_left:
            temp_key = (point.x, point.y)
            if temp_key in left_dict:
                temp_list = left_graph[i]
                adj_index = reverse_point[temp_key]
                for mapped_index in adj_list[adj_index]:
                    temp_temp_key = (points[mapped_index].x, points[mapped_index].y)
                    if temp_temp_key in left_dict:
                        temp_list.append(left_dict[temp_temp_key])
            i+=1

        i = 0
        for point in point_list_right:
            temp_key = (point.x, point.y)
            if temp_key in right_dict:
                temp_list = right_graph[i]
                adj_index = reverse_point[temp_key]
                for mapped_index in adj_list[adj_index]:
                    temp_temp_key = (points[mapped_index].x, points[mapped_index].y)
                    if temp_temp_key in right_dict:
                        temp_list.append(right_dict[temp_temp_key])
            i += 1

        return (left_num , right_num, point_list_left, point_list_right, left_graph, right_graph)


    # Change required
    def calculate_EC(self, c1, c2):
        distance, count = c1.calculate_absolute_closeness(c2)
        return (distance, count)

    def calculate_average_bisect_weight(self, point_list_1, point_list_2):
        count = 0
        distance = 0.0
        for p1 in point_list_1:
            for p2 in point_list_2:
                id1 = p1.id
                id2 = p2.id
                if ChameleonAlgo.edges[id1][id2] == 1:
                    count += 1
                    distance += 1.0 / ChameleonAlgo.weights[id1][id2]

        return (distance, count)

    def calculate_RC(self, c1, c2):
        pNum1 = len(c1.points)
        pNum2 = len(c2.points)
        left_num, right_num, point_list_left, point_list_right, left_graph, right_graph = self.divide_cluster(c1.cluster_graph, c1.points)

        EC1, count = self.calculate_average_bisect_weight(point_list_left, point_list_right)
        if count > 0:
            EC1 = EC1 / count
        left_num, right_num, point_list_left, point_list_right, left_graph, right_graph = self.divide_cluster(c2.cluster_graph, c2.points)

        EC2, count = self.calculate_average_bisect_weight(point_list_left, point_list_right)
        if count > 0:
            EC2 = EC2 / count

        EC1To2, count = self.calculate_EC(c1, c2)
        if count > 0:
            EC1To2 = EC1To2 / count

        if (pNum2 * EC1 + pNum1 * EC2) == 0.0:
            return 0

        RC = EC1To2 * (pNum1 + pNum2) / (pNum2 * EC1 + pNum1 * EC2)
        return RC

    def calculate_RI(self, c1, c2):
        left_num, right_num, point_list_left, point_list_right, left_graph, right_graph = self.divide_cluster(
            c1.cluster_graph, c1.points)
        EC1, count = self.calculate_average_bisect_weight(point_list_left, point_list_right)
        left_num, right_num, point_list_left, point_list_right, left_graph, right_graph = self.divide_cluster(
            c2.cluster_graph, c2.points)

        EC2, count = self.calculate_average_bisect_weight(point_list_left, point_list_right)
        EC1To2, count = self.calculate_EC(c1, c2)
        if EC1 + EC2 == 0:
            return 0
        RI = 2 * EC1To2 / (EC1 + EC2)
        return RI

    def calculate_metric_function(self, c1, c2, alpha):
        RI = self.calculate_RI(c1, c2)
        RC = self.calculate_RC(c1, c2)
        metricValue = RI * pow(RC, alpha)
        return metricValue

    def print_cluster(self, cluster_list):
        i = 1
        for cluster in cluster_list:
            print "Cluster "+ str(i)
            for p in cluster.points:
                print (p.x, p.y)
            i += 1

    def construct_graph(self, cluster_list):
        G = nx.Graph()
        pos = dict()
        colors = []
        colors = ['red', 'blue', 'green', 'black', 'white', 'brown', 'Navy', 'Cyan','Snow', 'Linen', 'Cornsilk']
        node_list = []
        for i in range(self.num_points):
            G.add_node(i)
            _point = self.points[i]
            pos[i] = (_point.x, _point.y)

        for i, cluster in enumerate(cluster_list):
            node_list.append([])

            for point in cluster.points:
                node_list[i].append(point.id)

        for i in range(len(cluster_list)):
            print str(i) +" : "+ str(node_list[i]) + str(colors[i])
            nx.draw_networkx_nodes(G, pos, nodelist=node_list[i], node_color=colors[i], node_size=50)

        # nx.draw(G, pos)
        plt.show()


    def plotKNN(self):
        G = nx.Graph()
        pos = dict()
        node_list = []
        for i in range(self.num_points):
            G.add_node(i)
            _point = self.points[i]
            pos[i] = (_point.x, _point.y)

        edges_list = []
        for i in range(self.num_points):
            for j in range(i+1,self.num_points):
                if i < j:
                    if ChameleonAlgo.edges[i][j] == 1:
                        edges_list.append((i,j))
                else:
                    break

        nx.draw_networkx_nodes(G, pos, node_color='r', node_size=50)
        nx.draw_networkx_edges(G, pos,
                               edgelist=edges_list,
                               width=1,alpha=0.5,edge_color='b')

        plt.show()
