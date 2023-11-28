import pandas as pd
import gdown

google_drive_url = 'https://drive.google.com/uc?id=1tzPr7xjSmQy1qVK8OumeZkvZIX0eQCpT'
output_file_name = 'steam_final_snowball.csv'

gdown.download(google_drive_url, output_file_name, quiet=False)
df = pd.read_csv(output_file_name, sep=',')

valid_users = df['ID'].tolist()
valid_users.remove(76561198042359209)

gdrive_url = "https://drive.google.com/uc?id=1-zE01JUYaH9Jua9Ux65e4ln1sEFLx3G2"
output_file_name = "steam_final_snowball.parquet"

gdown.download(gdrive_url, output_file_name, quiet=False)
df = pd.read_parquet(output_file_name)

df_final = df[df.index.isin(valid_users)]

df_final.to_parquet('steam_final_snowball_filtered.parquet')
