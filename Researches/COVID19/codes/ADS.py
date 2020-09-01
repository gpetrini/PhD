%config InlineBackend.figure_format = 'retina'

import pandas as pd
import numpy as np

from datetime import datetime as dt
from datetime import timedelta

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.image as image
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import seaborn as sns

logo = "./figs/Cecon_Logo.png"
logo = image.imread(logo)

file_path = './raw/USA/'
image_path = './figs/USA/'
corona = '2020-03-18' # More than 60 cases in Brazil
start_year = "2019-01-01"

df = pd.read_excel(
    'https://www.philadelphiafed.org/-/media/research-and-data/real-time-center/business-conditions-index/ads_index_most_current_vintage.xlsx?la=en',
    index_col=[0], parse_dates = True
)

fig, ax = plt.subplots(figsize=(8,5), dpi=300)

df["2019-01-01":"2020-08-31"].plot(ax=ax, 
         ls='-', 
         title= "Aruoba-Diebold-Scotti Business Conditions Index",
         color='darkred'
        )
ax.axvline(x = '2020-03-18', color='black', ls='-', lw=1, label='More than 60 COVID19 cases')
ax.legend()
ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
sns.despine()
plt.show()
fig.savefig(
    f"./figs/USA/ADS.svg", 
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
)
