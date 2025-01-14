import matplotlib.pyplot as plt
import pandas as pd
from global_vars import CSV_SONGS_PATH

music_stats = pd.read_csv(CSV_SONGS_PATH)

pie_chart = music_stats['Genre'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
plt.plot()

bar_chart = music_stats['Artist'].value_counts().plot.bar()
plt.plot()

line_chart = music_stats['Year'].value_counts().plot.line()
plt.plot()
