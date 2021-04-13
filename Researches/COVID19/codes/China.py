%config InlineBackend.figure_format = 'retina'
import sys

sys.path.insert(1, './codes/')

from setup import *


file_path = './raw/LCA/'
image_path = './figs/SetorExterno/'
start_year = "2019-01-01"

file_name = 'China_Banco_dados'
sheet = "Atividade Econômica"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    na_values='-'
)[0:]
df.index = pd.date_range( # Check for NaN
    start = '1994-01-01',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M'
    )
df = df['2019-01-01':]
df = df.fillna(method='ffill')
df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + "_" + sheet.replace(' ', '') + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'China_Banco_dados'
sheet = "PIB Trimestral Dessaz"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=11,
    na_values='-'
)[0:]
df.index = pd.date_range( # Check for NaN
    start = '1994-01-01',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='Q'
    )
df = df['2019-01-01':]
df = df.fillna(method='ffill')
df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + "_" + sheet.replace(' ', '') + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )
