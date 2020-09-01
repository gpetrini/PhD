%config InlineBackend.figure_format = 'retina'
import sys

sys.path.insert(1, './codes/')

from setup import *

start_year = "2019-01-01"

file_path = './raw/LCA/'
image_path = './figs/Confianca/'

file = "IIE-Br_FGV"
df = pd.read_excel(
    f"{file_path + file}.xlsx",
    index_col=[0],
    skiprows=11,
    parse_dates=True
)
df.index.name = ''
df = df["2019-01-01":]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5), dpi=300)

df.plot(
    ax=ax,
    title = "Indicador de Incerteza (IIE-Br)")

ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + file +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file = "ICE_FGV"
df = pd.read_excel(
    f"{file_path + file}.xlsx",
    index_col=[0],
    skiprows=11,
    parse_dates=True,
    sheet_name='Com_ajuste'
)
df.index.name = ''
df = df["2019-01-01":]
df = interpolator(df)
fig, ax = plt.subplots(figsize=(8,5), dpi=300)

df.plot(
    ax=ax,
    title = "Indicador de Confiança Empresaria (ICE-FGV)")

ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + file +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )
