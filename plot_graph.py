import pandas as pd
from matplotlib import pyplot as plt

from configs import CSV_PATH

df = pd.read_csv(CSV_PATH, index_col=0, names=['time', 'n_people'])

plt.plot(df)
plt.xticks(rotation='vertical', fontsize=5)
plt.tight_layout()
plt.show()
