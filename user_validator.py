import pandas as pd
import networkx as nx
import ast

df = pd.read_csv("steam_friends_by_user_final_filtered.csv")

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

# G = nx.Graph()
#
# for index, row in df.iterrows():
#     friends_list = ast.literal_eval(row['Friends'])
#     for friend in friends_list:
#         G.add_edge(row['ID'], friend)
#
# # Encontrar o nó com o maior grau
# node, degree = max(G.degree, key=lambda x: x[1])
#
# print(f"O nó com o maior grau é: {node}, com grau: {degree}")
# # O nó com o maior grau é: 76561198042359209, com grau: 2738

# df.set_index('ID', inplace=True)
#
# # Lista para armazenar os IDs válidos
# ids_validos = df.index.tolist()
#
# # Itera sobre a coluna 'Friends' e remove IDs inválidos
# for index, row in df.iterrows():
#     friends_list = ast.literal_eval(row['Friends'])
#     friends_list = [friend for friend in friends_list if friend in ids_validos]
#     df.at[index, 'Friends'] = friends_list
#
# # Salva o DataFrame resultante em um novo arquivo CSV
# df.to_csv('steam_friends_by_user_final_filtered.csv')

# # Supondo que você tenha um DataFrame chamado df
# contador = df['Friends'].apply(lambda x: x.count('76561198042359209')).sum()
#
# # Exibe o resultado
# print(f'O valor 76561198042359209 aparece {contador} vezes na coluna "Friends".')
# linha_id_especifico = df[df['ID'] == 76561198042359209]
#
# # Verifique se encontrou alguma linha
# if not linha_id_especifico.empty:
#     # Use ast.literal_eval para converter a string em lista
#     amigos_lista = ast.literal_eval(linha_id_especifico['Friends'].iloc[0])
#
#     # Obtenha o número de amigos
#     numero_amigos = len(amigos_lista)
#
#     # Exiba o resultado
#     print(f'O ID 76561198042359209 tem {numero_amigos} amigos.')
# else:
#     print('ID não encontrado no DataFrame.')

# # Verifique se há duplicatas com base em todas as colunas
# duplicatas = df.duplicated()
#
# # Verifique se há pelo menos uma duplicata em todo o DataFrame
# existe_duplicata = duplicatas.any()
#
# # Exiba o resultado
# print(f'Há duplicatas no DataFrame? {existe_duplicata}')

# # Verifique se há duplicatas na coluna 'ID'
# duplicatas_id = df.duplicated(subset=['ID'])
#
# # Verifique se há pelo menos uma duplicata na coluna 'ID'
# existe_duplicata_id = duplicatas_id.any()
#
# # Exiba o resultado
# print(f'Há duplicatas na coluna "ID"? {existe_duplicata_id}')

# print(len(df['ID'].tolist()))
# print(len(set(df['ID'].tolist())))

# # Itera sobre todas as linhas do DataFrame
#
# for index, row in df.iterrows():
#     friends_list = ast.literal_eval(row['Friends'])
#     num_friends = len(friends_list)
#
#     # Imprime o ID se tiver mais de 2000 amigos
#     if num_friends > 2000:
#         print(f"ID {row['ID']} tem mais de 2000 amigos.")
