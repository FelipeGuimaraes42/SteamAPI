import pandas as pd
import networkx as nx
import ast
import matplotlib.pyplot as plt

df = pd.read_csv("steam_friends_by_user_final_filtered.csv")

G = nx.Graph()

for index, row in df.iterrows():
    friends_list = ast.literal_eval(row['Friends'])
    for friend in friends_list:
        G.add_edge(row['ID'], friend)

nodes_to_remove = [node for node, degree in G.degree() if degree > 2000]
G.remove_nodes_from(nodes_to_remove)

nx.draw(G, with_labels=False,  edge_color='black', node_color='blue')

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=False, edge_color='black', node_color='blue')

plt.savefig("graph.png")
