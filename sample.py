import networkx as nx
import matplotlib.pyplot as plt
import metis
import pymetis
G = metis.example_networkx()
i = 0
pos=nx.spring_layout(G)
#(edgecuts, parts) = metis.part_graph(G, 4)
(edgecuts, parts) = pymetis.part_graph(4, G)
color_dict = dict()

colors = ['red','blue','green','black']
for color in colors:
     color_dict[color] = []
for i, p in enumerate(parts):
     G.node[i]['color'] = colors[p]
     temp_list = color_dict[colors[p]]
     temp_list.append(i)
#pos=nx.get_node_attributes(G,'pos')
for color in colors:
     nx.draw_networkx_nodes(G,pos,nodelist=color_dict[color], node_color=color)
plt.axis('off')
plt.savefig("sample.png") # save as png
plt.show() # display