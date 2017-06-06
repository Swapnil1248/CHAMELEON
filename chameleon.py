import sys
from math import  *
from util import *

root = None
debug = False
k_nearest = 15
k5_nearest = 50
balance_constraint = 25
min_size = 0.04
width = 700
height = 500
diagonal =  860.0
max_groups = 100
alpha = 300.0
stop_cluster = 0
max_size = 10000
file_name = ""
points = []
groups = []
groups_length = []

class HyperEdge:
	point_num = None
	similarity = None

	# def __init__(point_num, similarity):
	# 	self.point_num = point_num
	# 	self.similarity = similarity

class Point:
    x = None
    y = None
    length = None
    hyperedge = None

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __init__(self,x,y, length):
        self.x = x
        self.y = y
        self.length = length
  	
class Node:
    points = None
    numberPoints = None
    left = None
    right = None


def parsing_input():
    global file_name
    global max_size
    global stop_cluster
    pprint("in parsing input")
    if len(sys.argv) == 4:
        file_name = sys.argv[1]
        max_size = int(sys.argv[2])
        stop_cluster = int(sys.argv[3])
    if stop_cluster > max_size:
        print("Error cluster greater than mam data points")
        exit(1)

def read_Data():
    pprint("in read data")
    global points
    # read file and store in points list
    for line in open(file_name, "r").readlines():
        a, b = map(float, line.split(" "))
        points.add(Point(a,b,0))

def initialize():
    pprint("in initialize")
    for i in range(max_groups):
        groups.add(None)
        groups_length.add(0)
    threshold = (int)(max_size * min_size)
    if threshold < 1:
        print("threshold less than 1, error! \n")
        exit(-1)
    root = Node()
    root.numberPoints = max_size
    for i in range(max_size):
        root.points.add(i)


def establish_hyperGraph():
    pprint("in establish hyperGraph")
    similarity = []
    for i in range(max_size):
        similarity.add(i)
    for i in range(max_size):
        for j in range(max_size):
            similarity[j] = compute_similarity(i,j)

        for k in range(k_nearest):
            bestSimi = 0.0;
            indexBestSimi = 0;

            for l in range(max_size):
                if l != i:
                    if similarity[j] > bestSimi:
                        indexBestSimi = j;
                        bestSimi = similarity[j];

            if i < indexBestSimi:
                points[i].edges[points[i].length].pointNO = indexBestSimi;
                points[i].edges[points[i].length].similarity = bestSimi;
                points[i].length += 1;
                if points[i].length > k5_nearest:
                    print("length of the edges exceeds K5_nearest! bestSimi is \n",bestSimi)
                    exit(-1)
            else:
                flag = 0
                for m in range(len(points[indexBestSimi])):
                    if points[indexBestSimi].edges[m].pointNO == i:
                        flag = 1
                        break

                if flag == 0:
                    points[indexBestSimi].edges[points[indexBestSimi].length].pointNO = i;
                    points[indexBestSimi].edges[points[indexBestSimi].length].similarity = bestSimi;
                    points[indexBestSimi].length += 1;
                    if points[indexBestSimi].length > k5_nearest:
                        print("length of the edges exceeds K5_nearest!bestSimi is \n",bestSimi);
                        exit(-1)

        similarity[indexBestSimi] = 0.0;

def compute_similarity(point_i, point_j):
    pprint("in compute similarity")
    a1 = point_i.x
    b1 = point_i.y
    a2 = point_j.x
    b2 = point_j.y

    simi = (diagonal - sqrt((float)(a1-a2)*(a1-a2)+(float)(b1-b2)*(b1-b2)) )/diagonal

    return simi


def phase2():
    pprint("in phase 2")

def cluster_result():
    pprint("in cluster result")



if __name__ == "__main__":
    pprint("in main")
    parsing_input()
    print(file_name, max_size, stop_cluster)
    read_Data()
    initialize()
    establish_hyperGraph()
    # partition(root, left, right)
    phase2()
    cluster_result()
