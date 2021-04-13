import datetime
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import networkx as nx
import statsmodels.api as sm
sns.set_context('talk')
plt.style.use('bmh')


def consulta_bc(codigo_bcb, nome = ["Nome da série"]):
  url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
  df = pd.read_json(url)
  df['data'] = pd.to_datetime(df['data'], dayfirst=True)
  df.set_index('data', inplace=True)
  df.index.name = ''
  df.columns = nome
  return df

fig, ax = plt.subplots(figsize=(19.2, 10.8))

G = nx.DiGraph()
G.add_edges_from(
    [
        ("$h_{t-n}$", "$h_{t}$"),
        ("$r_{t-m}$", "$h_{t}$"),
        ("$\\varepsilon^{D}$", "$h_{t}$"),  # IS
        ("$\pi_{t-n}$", "$\pi_{t}$"),
        ("$\pi^{e}_{t+n}$", "$\pi_{t}$"),
        ("$h_{t-n}$", "$\pi_{t}$"),
        ("$\Delta p^{F}$", "$\pi_{t}$"),
        ("$\Delta e$", "$\pi_{t}$"),
        ("$\\varepsilon^{S}$", "$\pi_{t}$"),  # Phillips
        ("$\Delta i^{F}_{t}$", "$\Delta e$"),
        ("$\Delta x_{t}$", "$\Delta e$"),
        ("$\Delta i_{t}$", "$\Delta e$"),
        ("$\\varepsilon^{F}_{t}$", "$\Delta e$"),  # Câmbio
        ("$i_{t-n}$", "$i_{t}$"),
        ("$\pi_{t} - \pi^{\star}$", "$i_{t}$"),
        ("$h_{t}$", "$i_{t}$"),  # Regra PM
        ("$\pi_{t}$", "$r_{t}$"),
        ("$r_{t-m}$", "$r_{t}$"),
        ("$i_{t}$", "$r_{t}$"),  # Juros real
        ("$r_{t}$", "$h_{t}$"),
        ("$\pi_{t}$", "$\pi_{t} - \pi^{\star}$"),
        ("$i_{t}$", "$\Delta i_{t}$")
    ]
)


# Specify the edges you want here
red_edges = []
edge_colours = ["black" if not edge in red_edges else "red" for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]

highlights = ["$h_{t}$", "$\pi_{t}$", "$\Delta e$", "$i_{t}$"]
red_nodes = [node for node in G.nodes() if node in highlights]
white_nodes = [node for node in G.nodes() if node not in highlights]


# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.shell_layout(
    G,
)
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=3200,
    ax=ax,
    node_color="white",
    edgecolors="black",
    nodelist=white_nodes,
)
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=3200,
    ax=ax,
    node_color="red",
    edgecolors="black",
    nodelist=red_nodes,
)
nx.draw_networkx_labels(G, pos, font_size=20)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=red_edges,
    edge_color="darkred",
    arrows=True,
    arrowsize=30,
    min_target_margin=25,
    width=3.0,
)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=black_edges,
    arrows=True,
    arrowsize=30,
    min_target_margin=25,
)


sns.despine(left=True, bottom=True)
fig.savefig(
    "./figs/RMI.png", transparent=True, dpi=600, bbox_inches="tight", pad_inches=0
)

fig, ax = plt.subplots(figsize=(19.2, 10.8))

G = nx.DiGraph()
G.add_edges_from(
    [
        ("$h_{t-n}$", "$h_{t}$"),
        ("$r_{t-m}$", "$h_{t}$"),
        ("$\\varepsilon^{D}$", "$h_{t}$"),  # IS
        ("$\pi_{t-n}$", "$\pi_{t}$"),
        ("$\pi^{e}_{t+n}$", "$\pi_{t}$"),
        ("$h_{t-n}$", "$\pi_{t}$"),
        ("$\Delta p^{F}$", "$\pi_{t}$"),
        ("$\Delta e$", "$\pi_{t}$"),
        ("$\\varepsilon^{S}$", "$\pi_{t}$"),  # Phillips
        ("$\Delta i^{F}_{t}$", "$\Delta e$"),
        ("$\Delta x_{t}$", "$\Delta e$"),
        ("$\Delta i_{t}$", "$\Delta e$"),
        ("$\\varepsilon^{F}_{t}$", "$\Delta e$"),  # Câmbio
        ("$i_{t-n}$", "$i_{t}$"),
        ("$\pi_{t} - \pi^{\star}$", "$i_{t}$"),
        ("$h_{t}$", "$i_{t}$"),  # Regra PM
        ("$\pi_{t}$", "$r_{t}$"),
        ("$r_{t-m}$", "$r_{t}$"),
        ("$i_{t}$", "$r_{t}$"),  # Juros real
        ("$r_{t}$", "$h_{t}$"),
        ("$\pi_{t}$", "$\pi_{t} - \pi^{\star}$"),
        ("$i_{t}$", "$\Delta i_{t}$"),
    ]
)


# Specify the edges you want here
red_edges = []
edge_colours = ["black" if not edge in red_edges else "red" for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]

highlights = [
    "$h_{t}$",
    "$\pi_{t} - \pi^{\star}$",
    "$\Delta e$",
    "$i_{t-n}$",
    "$\Delta x_{t}$",
    "$\Delta p^{F}$",
    "$\\varepsilon^{F}_{t}$",
    "$\\varepsilon^{S}$",
    "$\\varepsilon^{D}$",
    "$\pi^{e}_{t+n}$"
]
red_nodes = [node for node in G.nodes() if node in highlights]
white_nodes = [node for node in G.nodes() if node not in highlights]


# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.shell_layout(
    G,
)
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=3200,
    ax=ax,
    node_color="white",
    edgecolors="black",
    nodelist=white_nodes,
)
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=3200,
    ax=ax,
    node_color="yellow",
    edgecolors="black",
    nodelist=red_nodes,
)
nx.draw_networkx_labels(G, pos, font_size=20)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=red_edges,
    edge_color="darkred",
    arrows=True,
    arrowsize=30,
    min_target_margin=25,
    width=3.0,
)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=black_edges,
    arrows=True,
    arrowsize=30,
    min_target_margin=25,
)


sns.despine(left=True, bottom=True)
fig.savefig(
    "./figs/RMI_234.png", transparent=True, dpi=600, bbox_inches="tight", pad_inches=0
)

import matplotlib.ticker as mticker


df = pd.concat(
    [
        consulta_bc(22109, ["PIB"]),
        consulta_bc(22110, ["Consumo das famílias"]),
        consulta_bc(22111, ["Consumo do governo"]),
        consulta_bc(22113, ["FBCF"]),
        consulta_bc(22114, ["Exportação"]),
        consulta_bc(22115, ["Importação"]),
    ],
    axis=1,
)

df["Mercado doméstico"] = df[
    ["Consumo das famílias", "Consumo do governo", "FBCF"]
].sum(axis=1)
df["Setor Externo"] = df["Exportação"] - df["Importação"]
df = df["2001-01-01":"2011-12-31"]
fig, ax = plt.subplots(figsize=(19.20, 10.80))

df[["Mercado doméstico", "Setor Externo"]].diff(4).apply(
    lambda x: x / (df["PIB"].shift(4))
).dropna().plot(ax=ax, lw=2.5, kind="bar", stacked=True, width=0.75, edgecolor="black")
# ax.set_xticklabels(df.index.strftime('%Y-%m')[::8])
# ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ticklabels = [""] * len(df)
skip = len(df) // 12
ticklabels[4::skip] = df.index[4::skip].strftime("%Y")
ax.xaxis.set_major_formatter(mticker.FixedFormatter(ticklabels))
fig.autofmt_xdate()

sns.despine()
fig.savefig("./figs/PIB_Decomp_I.png", transparent=True, dpi=300)
plt.cla()

fig, ax = plt.subplots(figsize=(19.20, 10.80))
df[["Consumo das famílias", "Consumo do governo", "FBCF", "Setor Externo"]].diff(
    4
).apply(lambda x: x / (df["PIB"].shift(4))).dropna().plot(
    ax=ax,
    lw=2.5,
    kind="bar",
    stacked=True,
    width=0.75,
    color=(
        "darkred",
        "darkblue",
        "darkorange",
        "darkgreen",
    ),
    edgecolor="black",
)
ticklabels = [""] * len(df)
skip = len(df) // 12
ticklabels[4::skip] = df.index[4::skip].strftime("%Y")
ax.xaxis.set_major_formatter(mticker.FixedFormatter(ticklabels))
fig.autofmt_xdate()

sns.despine()

fig.savefig("./figs/PIB_Decomp_Total_I.png", transparent=True, dpi=300)
plt.cla()

df = consulta_bc(28512, ["Emprego Formal"])
df = df["2001-01-01":"2011-12-31"]
fig, ax = plt.subplots(figsize=(19.20, 10.80))

df.plot(
    ax=ax,
    lw=2.5,
    color="black",
    ls="-",
)
sns.despine()

fig.savefig("./figs/EmpregoFormal_I.png", transparent=True, dpi=300)

df = consulta_bc(20360, ['Câmbio'])

fig, ax = plt.subplots(figsize=(19.20,10.80))
df = df[:"2011-12-31"]
df.plot(ax=ax,
	lw=2.5,
	color='black',
	ls='-',
        label=False,
)
sns.despine()

fig.savefig("./figs/CambioNominal_I.png", transparent = True, dpi = 300)

fig, ax = plt.subplots(1,1, figsize=(19.20,10.80))


df = pd.concat([consulta_bc(1178, ['Efetiva']), consulta_bc(432, ['Meta'])],axis=1)
df["Desvio"] = df["Meta"] - df["Efetiva"]

df["1999-01-01":"2011-12-31"].plot(ax=ax, color=('black', 'red', 'gray'))

ax.set_yticklabels(['{:,.2%}'.format(x/100) for x in ax.get_yticks()])
sns.despine()

fig.savefig("./figs/Selic_I.png", transparent = True, dpi = 300)

df = consulta_bc(13521, ["Meta"])
df = df.resample('MS').ffill()#.bfill()

df["Teto"] = df["Meta"] + 2.0
df["Piso"] = df["Meta"] - 2.0

df = pd.concat([
    df,
    consulta_bc(433,["IPCA"])
], axis=1)

df = df["1998-01-01":"2011-12-31"]
df = df/100
df["IPCA"] = (1+ df["IPCA"]).rolling(window=12).agg(lambda x : x.prod()) -1

fig, ax = plt.subplots(figsize=(19.20,10.80))

df[["IPCA"]].plot(ax=ax,
lw=2,
ls='-',
color = 'red',                  
)

ax.pcolorfast(ax.get_xlim(), ax.get_ylim(),
              (df['IPCA'] > df["Teto"]).values[np.newaxis],
              cmap='Reds', alpha=0.3, label="Acima do Teto",
              zorder=-1,
)

ax.pcolorfast(ax.get_xlim(), ax.get_ylim(),
              (df['IPCA'] < df["Piso"]).values[np.newaxis],
              cmap='Blues', alpha=0.3, label="Abaixo do Piso",
              zorder=-1,
)

ax.legend()

sns.despine()

fig.savefig("./figs/IPCA_I.png", transparent = True, dpi = 300)

df = consulta_bc(13521, ["Meta"])
df = df.resample('MS').ffill()#.bfill()

df["Teto"] = df["Meta"] + 2.0
df["Piso"] = df["Meta"] - 2.0

df = pd.concat([
    df,
    consulta_bc(433,["IPCA"]),
    consulta_bc(11428,["Livres"]),
    consulta_bc(4449,["Monitorados"]),
    consulta_bc(10844,["Serviços"]),
], axis=1)

df = df["1998-01-01":"2011-12-31"]
df = df/100
df["IPCA"] = (1+ df["IPCA"]).rolling(window=12).agg(lambda x : x.prod()) -1
df["Livres"] = (1+ df["Livres"]).rolling(window=12).agg(lambda x : x.prod()) -1
df["Monitorados"] = (1+ df["Monitorados"]).rolling(window=12).agg(lambda x : x.prod()) -1
df["Serviços"] = (1+ df["Serviços"]).rolling(window=12).agg(lambda x : x.prod()) -1
fig, ax = plt.subplots(figsize=(19.20,10.80))

df[["Livres", "Monitorados", "Serviços", "IPCA"]].dropna().plot(ax=ax,
lw=2,
ls='-',
color = ('blue','red','green', 'black'),                  
)

ax.pcolorfast(ax.get_xlim(), ax.get_ylim(),
              (df['IPCA'] > df["Teto"]).values[np.newaxis],
              cmap='Reds', alpha=0.3, label="Acima do Teto",
              zorder=-1,
)

ax.pcolorfast(ax.get_xlim(), ax.get_ylim(),
              (df['IPCA'] < df["Piso"]).values[np.newaxis],
              cmap='Blues', alpha=0.3, label="Abaixo do Piso",
              zorder=-1,
)

ax.legend()

sns.despine()

fig.savefig("./figs/Livres_Administrados_I.png", transparent = True, dpi = 300)

import matplotlib.ticker as mticker


df = pd.concat([
    consulta_bc(22109,["PIB"]),
    consulta_bc(22110,["Consumo das famílias"]),
    consulta_bc(22111,["Consumo do governo"]),
    consulta_bc(22113,["FBCF"]),
    consulta_bc(22114,["Exportação"]),
    consulta_bc(22115,["Importação"])
], axis=1)

df["Mercado doméstico"] = df[["Consumo das famílias", "Consumo do governo", "FBCF"]].sum(axis=1)
df["Setor Externo"] = df["Exportação"] - df["Importação"]
df = df["2010-12-31":]
fig, ax = plt.subplots(figsize=(19.20,10.80))

df[["Mercado doméstico", "Setor Externo"]].diff(4).apply(lambda x: x/(df["PIB"].shift(4))).dropna().plot(ax=ax,
                                                lw=1.5,
                                                kind='bar',
                                                stacked=True,
                                                                                                width = 0.75,
                                                edgecolor='black'
                                                
)
#ax.set_xticklabels(df.index.strftime('%Y-%m')[::8])
#ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

ticklabels = ['']*len(df)
skip = len(df)//12
ticklabels[4::skip] = df.index[4::skip].strftime('%Y')
ax.xaxis.set_major_formatter(mticker.FixedFormatter(ticklabels))
fig.autofmt_xdate()

ax.text(
	0.95, -0.12,
	f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=15)


sns.despine()
fig.savefig("./figs/PIB_Decomp.png", transparent = True, dpi = 300)
plt.cla()

fig, ax = plt.subplots(figsize=(19.20,10.80))
df = df["2010-12-31":]
df[["Consumo das famílias", "Consumo do governo", "FBCF",
    "Setor Externo"
]].diff(4).apply(lambda x: x/(df["PIB"].shift(4))).dropna().plot(ax=ax,
                                                                 lw=1.5,
                                                                 kind='bar',
                                                                 stacked=True,
                                                                 width = 0.75,
                                                                 color = ("darkred", "darkblue", "darkorange", "darkgreen",),
                                                                 edgecolor='black'
                                                
)
ticklabels = ['']*len(df)
skip = len(df)//12
ticklabels[4::skip] = df.index[4::skip].strftime('%Y')
ax.xaxis.set_major_formatter(mticker.FixedFormatter(ticklabels))
fig.autofmt_xdate()

ax.text(
	0.95, -0.12,
	f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=15)


sns.despine()

fig.savefig("./figs/PIB_Decomp_Total.png", transparent = True, dpi = 300)
plt.cla()

df = consulta_bc(28512, ["Emprego Formal"])

fig, ax = plt.subplots(figsize=(19.20,10.80))

df = df["2010-12-31":]
df.plot(ax=ax,
lw=2.5,
color='black',
ls='-',
)

ax.text(
0.95, -0.15,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)


sns.despine()

fig.savefig("./figs/EmpregoFormal.png", transparent = True, dpi = 300)

df = consulta_bc(20360, ['Câmbio'])

df = df["2010-12-31":]
fig, ax = plt.subplots(figsize=(19.20,10.80))

df.plot(ax=ax,
	lw=2.5,
	color='black',
	ls='-',
        label=False,
)

ax.text(
	0.95, -0.2,
	f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)


sns.despine()

fig.savefig("./figs/CambioNominal.png", transparent = True, dpi = 300)

fig, ax = plt.subplots(1,1, figsize=(19.20,10.80))


df = pd.concat([consulta_bc(1178, ['Efetiva']), consulta_bc(432, ['Meta'])],axis=1)
df["Desvio"] = df["Meta"] - df["Efetiva"]

df = df["2010-12-31":]
df.plot(ax=ax, color=('black', 'red', 'gray'))

ax.set_yticklabels(['{:,.2%}'.format(x/100) for x in ax.get_yticks()])



ax.text(
0.95, -0.2,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)


sns.despine()

fig.savefig("./figs/Selic.png", transparent = True, dpi = 300)

df = consulta_bc(13521, ["Meta"])
df = df.resample('MS').ffill()#.bfill()

df["Teto"] = df["Meta"] + 2.0
df["Piso"] = df["Meta"] - 2.0

df = pd.concat([
    df,
    consulta_bc(433,["IPCA"])
], axis=1)

df = df["2009-12-31":]
df = df/100
df["IPCA"] = (1+ df["IPCA"]).rolling(window=12).agg(lambda x : x.prod()) -1
df = df.dropna()
fig, ax = plt.subplots(figsize=(19.20,10.80))

df[["IPCA"]].plot(ax=ax,
lw=2,
ls='-',
color = 'red',                  
)

ax.text(
0.95, -0.15,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)

ax.pcolorfast(ax.get_xlim(), ax.get_ylim(),
              (df['IPCA'] > df["Teto"]).values[np.newaxis],
              cmap="Reds", alpha=0.3, label="Acima do Teto",
              zorder=-1,
)

ax.pcolorfast(ax.get_xlim(), ax.get_ylim(),
              (df['IPCA'] < df["Piso"]).values[np.newaxis],
              cmap='Blues', alpha=0.3, label="Abaixo do Piso",
              zorder=-1,
)

ax.legend()

sns.despine()

fig.savefig("./figs/IPCA.png", transparent = True, dpi = 300)

df = consulta_bc(13521, ["Meta"])
df = df.resample("MS").ffill()  # .bfill()

df["Teto"] = df["Meta"] + 2.0
df["Piso"] = df["Meta"] - 2.0

df = pd.concat(
    [
        df,
        consulta_bc(433, ["IPCA"]),
        consulta_bc(11428, ["Livres"]),
        consulta_bc(4449, ["Monitorados"]),
        consulta_bc(10844, ["Serviços"]),
    ],
    axis=1,
)

df = df["2009-12-31":]
df = df / 100
df["IPCA"] = (1 + df["IPCA"]).rolling(window=12).agg(lambda x: x.prod()) - 1
df["Livres"] = (1 + df["Livres"]).rolling(window=12).agg(lambda x: x.prod()) - 1
df["Monitorados"] = (1 + df["Monitorados"]).rolling(window=12).agg(
    lambda x: x.prod()
) - 1
df["Serviços"] = (1 + df["Serviços"]).rolling(window=12).agg(lambda x: x.prod()) - 1
fig, ax = plt.subplots(figsize=(19.20, 10.80))

df[["Livres", "Monitorados", "Serviços", "IPCA"]].dropna().plot(
    ax=ax,
    lw=2,
    ls="-",
    color=("blue", "red", "green", "black"),
)

ax.text(
    0.95,
    -0.15,
    f"\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}",
    verticalalignment="bottom",
    horizontalalignment="right",
    transform=ax.transAxes,
    color="black",
    fontsize=10,
)

ax.pcolorfast(
    ax.get_xlim(),
    ax.get_ylim(),
    (df["IPCA"] > df["Teto"]).values[np.newaxis],
    cmap="Reds",
    alpha=0.3,
    label="Acima do Teto",
    zorder=-1,
)

ax.pcolorfast(
    ax.get_xlim(),
    ax.get_ylim(),
    (df["IPCA"] < df["Piso"]).values[np.newaxis],
    cmap="Blues",
    alpha=0.3,
    label="Abaixo do Piso",
    zorder=-1,
)

ax.legend()

sns.despine()

fig.savefig("./figs/Livres_Administrados.png", transparent=True, dpi=300)
plt.cla()

df = pd.read_html(
    'http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=40940&module=M',
    thousands='.',
)[2]

df = pd.DataFrame(df).iloc[1:]
df.iloc[:,0] =  pd.to_datetime(df.iloc[:,0], format='%d/%m/%Y')
df.columns = ["Data", "EMBI+"]
df.set_index("Data", inplace=True)
df.index.name=''
df = df.apply(pd.to_numeric, errors='coerce')#.resample('B').last()

fig, ax = plt.subplots(figsize=(19.2,10.8))

df.plot(ax=ax,
	lw=2.5,
	color='red',
	ls='-',
)

ax.text(
    0.95, -0.12,
    f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
    verticalalignment='bottom', horizontalalignment='right',
    transform=ax.transAxes,
    color='black', fontsize=15)


sns.despine()
plt.show()
fig.savefig("./figs/EMBI.png", transparent = True, dpi = 300)
plt.cla()

df = pd.concat([
    consulta_bc(27574, nome = ["Brasil"]),
    consulta_bc(27576, nome = ["Metal"]),
    consulta_bc(27575, nome = ["Agropecuária"]),
], axis=1)


for col in df.columns:
    df[col] = df[col].apply(lambda x: 100*x/df[col]["2002-01-01"])


fig, ax = plt.subplots(figsize=(19.20,10.80))

df.plot(ax=ax,
	lw=2.5,
	ls='-',
)

ax.text(
	0.95, -0.1,
        f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)


sns.despine()

fig.savefig("./figs/Commodities.png", transparent = False, dpi = 300)

df = pd.concat([
    consulta_bc(22866, nome = ["Investimento Direto Estrangeiro (ingresso)"]),
    consulta_bc(22907, nome = ["Investimento em carteira (ingresso)"]),
    consulta_bc(22970, nome = ["Outros investimentos (ingresso)"]),
    consulta_bc(22864, nome = ["Conta financeira (líquida)"]),
]).apply(pd.to_numeric, errors='coerce').resample("MS").last()

fig, ax = plt.subplots(figsize=(19.20,10.80))

df.drop(['Conta financeira (líquida)'], axis='columns').rolling(12).mean().plot(
    ax=ax,
    lw=2.5,
    color=('orange', 'lightblue', 'darkblue'),
    ls='-',
    legend=False
)

df[['Conta financeira (líquida)']].rolling(12).mean().plot(
    ax=ax,
    lw=2.5,
    color=('red'),
    kind='area',
    legend=False,
    stacked=False
)

ax.legend(frameon=True, edgecolor='black')

ax.set_ylabel('US$ (Milhões)')

ax.text(
    0.95, -0.08,
    f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
    verticalalignment='bottom', horizontalalignment='right',
    transform=ax.transAxes,
    color='black', fontsize=15)


sns.despine()
fig.savefig("./figs/FluxosInternacionais.png", transparent = True, dpi = 300)
plt.cla()

df = consulta_bc(13621, nome = ["Total"])
#df = pd.concat([df, consulta_bc(13982 , nome = ["Conceito Liquidez"])], axis=1, sort=False)
fig, ax = plt.subplots(figsize=(19.20,10.80))

df.plot(ax=ax,
lw=2.5,
ls='-',
        color='darkred'
)

ax.text(
0.95, -0.2,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)
ax.set_ylabel('US$ (milhões)')

sns.despine()

fig.savefig("./figs/Reservas_Internacionais.png", transparent = True, dpi = 300)

df = consulta_bc(
    10790,
    ["RMRE - Todos os trabalhos"]
)

df['Série Desazonalizada'] = sm.tsa.seasonal_decompose(df["RMRE - Todos os trabalhos"]).trend

fig, ax = plt.subplots(figsize=(19.20,10.80))

df.plot(ax=ax,
lw=2.5,
color=('darkred', 'black'),
ls='-'
)

ax.text(
0.95, -0.15,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)
ax.set_ylabel('R$')


sns.despine()

fig.savefig("./figs/RendimentoEfetivo.png", transparent = True, dpi = 300)
plt.cla()

df = consulta_bc(28545, ["MRRH - Todos os trabalhos"])

fig, ax = plt.subplots(figsize=(19.20,10.80))

df.plot(ax=ax,
lw=2.5,
color='darkred',
ls='-'
)

ax.text(
0.95, -0.15,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)
ax.set_ylabel('R$ (milhões)')


sns.despine()

fig.savefig("./figs/RendimentoHabitual.png", transparent = True, dpi = 300)

fig, ax = plt.subplots(figsize=(19.20,10.80))

consulta_bc(22110, ["Número Índice"]).plot(ax=ax,
lw=2.5,
color='black',
ls='-',
)

ax.text(
0.95, -0.1,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)


sns.despine()

fig.savefig("./figs/ConsumoFamilias.png", transparent = True, dpi = 300)

df = pd.concat(
    [
        consulta_bc(19882, ["Total"]),
        consulta_bc(20400, ["Exceto crédito habitacional"])
    ],
    axis = 1
)

fig, ax = plt.subplots(figsize=(19.20,10.80))

df.plot(ax=ax,
	lw=2.5,
	ls='-'
)

ax.text(
	0.95, -0.15,
	f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)
ax.set_yticklabels(['{:,.2%}'.format(x/100) for x in ax.get_yticks()])

sns.despine()

fig.savefig("./figs/EndividamentoFam.png", transparent = True, dpi = 300)

fig, ax = plt.subplots(figsize=(19.20,10.80))

df = pd.concat([
    consulta_bc(4536, ["Líquida"]),
    consulta_bc(13762, ["Bruta"]),
    ]
).apply(pd.to_numeric, errors='coerce').resample("MS").last()



(df/100).plot(ax=ax,
lw=2.5,
color=('black','red'),
ls='-',
)

ax.axhline(y=0, ls='--', color='gray', lw=1.0)

ax.text(
0.95, -0.15,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)


sns.despine()

fig.savefig("./figs/Divida_BrutaLiquida.png", transparent = True, dpi = 300)

fig, ax = plt.subplots(figsize=(19.20,10.80))

df = pd.concat([
    consulta_bc(5497, ["Resultado Primário"]),
    consulta_bc(5431, ["Resultado Nominal"]),
    consulta_bc(5464, ["Juros nominais"]),
    ]
).apply(pd.to_numeric, errors='coerce').resample("MS").last().dropna()

df[["Resultado Primário", "Resultado Nominal"]] = df[["Resultado Primário", "Resultado Nominal"]]*(-1)

(df/100)["1996-01-01":].plot(ax=ax,
lw=2.5,
color=('black','red', 'blue'),
ls='-',
)

ax.axhline(y=0, ls='--', color='gray', lw=1.0)

ax.text(
0.95, -0.15,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)


sns.despine()

fig.savefig("./figs/Resultado_Primario.png", transparent = True, dpi = 300)

df = consulta_bc(20622, ["Total"])

df = pd.concat([
    df,
    consulta_bc(20625, ["Crédito livre"]),
    consulta_bc(20628, ["Crédito direcionado"]),
]
).apply(pd.to_numeric, errors='coerce').resample("MS").last()


fig, ax = plt.subplots(figsize=(19.20,10.80))

df = df["2001-01-01":"2011-12-31"]
df.plot(ax=ax,
lw=2.5,
ls='-',
)

ax.text(
0.95, -0.17,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)

ax.set_yticklabels(['{:,.2%}'.format(x/100) for x in ax.get_yticks()])

sns.despine()

fig.savefig("./figs/Credito_I.png", transparent = True, dpi = 300)

df = consulta_bc(20622, ["Total"])

df = pd.concat([
    df,
    consulta_bc(20625, ["Crédito livre"]),
    consulta_bc(20628, ["Crédito direcionado"]),
]
).apply(pd.to_numeric, errors='coerce').resample("MS").last()


fig, ax = plt.subplots(figsize=(19.20,10.80))

df["1996-01-01":].plot(ax=ax,
lw=2.5,
ls='-',
)

ax.text(
0.95, -0.17,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)

ax.set_yticklabels(['{:,.2%}'.format(x/100) for x in ax.get_yticks()])

sns.despine()

fig.savefig("./figs/Credito.png", transparent = True, dpi = 300)

df = pd.concat(
    [
        consulta_bc(4503, ["Total"]),
        consulta_bc(4514, ["Interna"]),
        consulta_bc(4525, ["Externa"]),
    ],
    axis=1
)

fig, ax = plt.subplots(figsize=(19.20,10.80))

df.plot(ax=ax,
lw=2.5,
ls='-'
)

ax.set_yticklabels(['{:,.2%}'.format(x/100) for x in ax.get_yticks()])
ax.axhline(y=0, ls='--', lw=1.0, color='black')

ax.text(
0.95, -0.1,
f'\nAtualizado em {datetime.datetime.now():%Y-%m-%d %H:%M}',
verticalalignment='bottom', horizontalalignment='right',
transform=ax.transAxes,
color='black', fontsize=10)


sns.despine()

fig.savefig("./figs/DividaLiquida.png", transparent = True, dpi = 300)
