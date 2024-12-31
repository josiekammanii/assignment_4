import pandas as pd

CSV_PATH = "songs.csv"

df_of_songs = pd.read_csv(CSV_PATH)
print(df_of_songs)
print(df_of_songs.iloc[0])
print(df_of_songs.iloc[2:7])
