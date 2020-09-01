%config InlineBackend.figure_format = 'retina'
import sys

sys.path.insert(1, './codes/')

from setup import *


file_path = './raw/LCA/'
image_path = './figs/Setoriais/'
start_year = "2019-01-01"
base = "2014-12-01"

file_name = "PIM_IBGE"
df = pd.read_excel(
    file_path + file_name + ".xlsx",
    sheet_name = "Seções Ativi Dessaz",
    skiprows = 11,
    usecols = "A:D",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''
for col in df:
    df[col] = df[col].apply(lambda x: (100*x)/df[col][base])

df = df[start_year:]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = f"Pesquisa Industrial Mensal (PIM)\nSeções de atividades desazonalizadas\n{base} = 100",
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
    image_path + file_name + "_" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = "PMC_IBGE"
df = pd.read_excel(
    file_path + file_name + ".xlsx",
    sheet_name = "Volume Vendas Dessaz",
    skiprows = 11,
    usecols = "A:D,F,G,J:P",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''
for col in df:
    df[col] = df[col].apply(lambda x: (100*x)/df[col][base])

df = df[start_year:]
df = interpolator(df)

df.columns = [
    "Comércio Varejista Restrito",
    "Combustíveis e Lubiricantes",
    "Hipermercados, Supermercados, Prod. Alimentícios, Bebidas e Fumo",
    "Tecidos, Vestuário e Calçados",
    "Móveis e Eletrodomésticos",
    "Artigos Farmacêuticos, Médicos, Ortopédicos, de Perfumaria e Cosméticos",
    "Livros, Jornais, Revistas e Papelaria",
    "Equipamentos e Materiais para Escritório, Informática e Comunicação",
    "Outros Artigos de Uso Pessoal e Doméstico",
    "Veículos, Motos, Partes e Peças",
    "Material de Construção",
    "Comércio Varejista Ampliado",
]

UsoPessoalDomestico = [
    "Artigos Farmacêuticos, Médicos, Ortopédicos, de Perfumaria e Cosméticos",
    "Livros, Jornais, Revistas e Papelaria",
    "Equipamentos e Materiais para Escritório, Informática e Comunicação",
    "Outros Artigos de Uso Pessoal e Doméstico",
]


fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = f"Pesquisa Mensal do Comércio (PMC)\nVolume de Vendas Dessazonalizado\n{base} = 100",
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
    image_path + file_name + "_" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = "PMS_IBGE"
df = pd.read_excel(
    file_path + file_name + ".xlsx",
    sheet_name = "Volume dessaz",
    skiprows = 11,
    usecols = "A:C,F,K,N,S",
    parse_date = True,
    index_col = [0]
)
df.index.name = ''

for col in df:
    df[col] = df[col].apply(lambda x: (100*x)/df[col][base])

df = df[start_year:]
df = interpolator(df)
df.columns = [
    "Total Geral",
    "Serviços prestados às Famílias",
    "Serviços de informação e comunicação",
    "Serviços Profissionais, Administrativos e Complementares",
    "Transportes, Serviços auxiliares aos transportes e Correio",
    "Outros serviços"
]

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = f"Pesquisa Mensal de Serviços (PMS)\nÍndice de Volume de serviços dessazonalizado\n{base} = 100",
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
    image_path + file_name + "_" + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )
