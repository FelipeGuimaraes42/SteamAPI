# import gdown
import pandas as pd
import csv
import ast

# gdrive_url = "https://drive.google.com/uc?id=1c9fQOru5pIfbwLZ3-yaUlDX_yOHlMMfw"
output_file_name = "steam_final_snowball.parquet"

# gdown.download(gdrive_url, output_file_name, quiet=False)
df = pd.read_parquet(output_file_name)

valid_users = df.index.tolist()
friends_by_user = []
for i in range(0, len(df)):
    user_id = df.index[i]
    try:
        friends_info = ast.literal_eval(df.iloc[i].friendsList)
        friends = []
        for friend_info in friends_info:
            try:
                friend = int(friend_info['steamid'])
                if friend in valid_users:
                    friends.append(friend)
            except Exception:
                pass
        friends_by_user.append((user_id, friends))
    except Exception:
        pass

csv_file = 'steam_friends_by_user.csv'

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)

    header = ['ID', 'Friends']
    writer.writerow(header)
    writer.writerows(friends_by_user)

print(f'Arquivo CSV "{csv_file}" criado com sucesso.')
