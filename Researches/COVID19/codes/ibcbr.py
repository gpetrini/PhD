%config InlineBackend.figure_format = 'retina'
import sys

sys.path.insert(1, './codes/')

from setup import *

start_year = "2019-01-01"

file_path = './raw/LCA/IBCBr.xlsx'
image_path = './figs/Antecedente/'

df = pd.read_excel(
    file_path,
    sheet_name = "IBC-Br Dessaz",
    skiprows = 11,
#    usecols = "A:B",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''

df = rebase(df)
df = df[start_year:]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = f"Índice de Atividade Econômica do Banco Central\nDessazonalizado\n{base} = 100",
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label=corona_sp_txt)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_path.strip("/")[-1] + "IBCBr" + "_" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )
