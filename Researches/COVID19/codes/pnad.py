%config InlineBackend.figure_format = 'retina'
import sys

sys.path.insert(1, './codes/')

from setup import *


file_path = './raw/LCA/PNAD_Continua.xlsx'
image_path = './figs/Emprego/'
start_year = "2019-01-01"

var = "Taxa de desocupação"
df = pd.read_excel(
    file_path,
    sheet_name = "Brasil Dessaz",
    skiprows = 11,
    usecols = "A,F",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''


df = df[start_year:]
df.columns = [
    var
]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = "Taxa de Desocupação\n(% da Força de Trabalho)",
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_path.strip("/")[-1] + var.replace(" ", "_") + "_" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

var = "Massa de renda real efetiva"
df = pd.read_excel(
    file_path,
    sheet_name = "Brasil Dessaz",
    skiprows = 11,
    usecols = "A,R",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''


df = df[start_year:]
df.columns = [
    var
]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = "Massa de renda real efetiva",
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento social em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_path.strip("/")[-1] + var.replace(" ", "_") + "_" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

var = "Desalentados_Subocupados"
df = pd.read_excel(
    file_path,
    sheet_name = "Brasil Dessaz",
    skiprows = 11,
    usecols = "A,D,S,T",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''
df.columns = [
    "Força de trabalho",
    "Subocupados",
    "Desalentados"
]
df = df.apply(pd.to_numeric, errors='coerce')
df["Taxa de desalentados"] = df["Desalentados"]/df["Força de trabalho"]
df["Taxa de Subocupados por \ninsuficiência de horas trabalhadas"] = df["Subocupados"]/df["Força de trabalho"]
df = df[start_year:]
df = df[["Taxa de desalentados", "Taxa de Subocupados por \ninsuficiência de horas trabalhadas"]]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = "Taxa de desalentados e subocupatos\n(em % da força de trabalho)",
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento social em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_path.strip("/")[-1] + var.replace(" ", "_") + "_" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

df = pd.read_excel(
    file_path,
    sheet_name = "Brasil Mensal RHM Setor Real",
    skiprows = 11,
    usecols = "A:K",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''
df = df[start_year:]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = "Rendimento habitual médio por atividade",
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento social em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_path.strip("/")[-1] + "RHM_Setor" + "_" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

df = pd.read_excel(
    file_path,
    sheet_name = "Brasil Mensal PO Setor",
    skiprows = 11,
    usecols = "A:K",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''
df = df[start_year:]


fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = "População ocupada por atividade",
    ax = ax,
    lw = 1.5,
    edgecolor = 'black',
    kind = 'bar', stacked = True
)



ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_path.strip("/")[-1] + "PO_Atividade" + "_" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

var = "Taxa de ocupação"
df = pd.read_excel(
    file_path,
    sheet_name = "Brasil Dessaz",
    skiprows = 11,
    usecols = "A,D,E",
    parse_date = True,
    index_col = [0]
)

df.index.name = ''
df = df[start_year:]
df.columns = ["Força de trabalho", "População ocupada"]

df[var] = df["População ocupada"]/df["Força de trabalho"]
df = df[[var]]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = "Taxa de Ocupação\n(% da Força de Trabalho)",
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
    image_path + file_path.strip("/")[-1] + var.replace(" ", "_") + "_" + "linha" +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

df = pd.read_excel(
    file_path,
    sheet_name = "Brasil Mensal PO Setor",
    skiprows = 11,
    usecols = "A:L",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''
df = df[start_year:]
for col in df:
    df[col] = df[col].apply(lambda x: (100*x)/df["Total"])

df.drop(["Total"], axis='columns', inplace=True)
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = "População ocupada por atividade\n(% Força de trabalho)",
    ax = ax,
    lw = 1.5,
)

ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label=corona_sp_txt)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_path.strip("/")[-1] + "PO_Atividade" + "_" + "linha" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )
