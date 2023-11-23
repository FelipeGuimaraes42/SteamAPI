import pandas as pd
import networkx as nx
import ast

df = pd.read_csv("steam_friends_by_user_final.csv")

# data = []
# for index, row in df.iterrows():
#     friends_list = ast.literal_eval(row['Friends'])
#     data.append((row['ID'], friends_list))
#
# count = 0
# for user, friends in data:
#     if len(friends) > 2000:
#         count += 1
#
# print('Numero de usuarios com mais de 2000 amigos:', count)

# count = 0
# for index, row in df.iterrows():
#     friends_list = ast.literal_eval(row['Friends'])
#     if len(friends_list) > 2000:
#         count += 1
#
# print('Numero de usuarios com mais de 2000 amigos:', count)

G = nx.Graph()

for index, row in df.iterrows():
    friends_list = ast.literal_eval(row['Friends'])
    for friend in friends_list:
        G.add_edge(row['ID'], friend)

# Encontrar o nó com o maior grau
node, degree = max(G.degree, key=lambda x: x[1])

print(f"O nó com o maior grau é: {node}, com grau: {degree}")
# O nó com o maior grau é: 76561198042359209, com grau: 3288
