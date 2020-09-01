%config InlineBackend.figure_format = 'retina'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
import seaborn as sns
import datetime

plt.style.use('seaborn-dark-palette')

import matplotlib.image as image

logo = "./figs/Cecon_Logo.png"
logo = image.imread(logo)

Colunas = [
    "Agropecuaria",
    "Industria Extrativa",
    "Industria de Transformacao",
    "Eletricidade e agua",
    "Construcao",
    "Total Industria",
    "Comercio",
    "Transporte, armazenagem e correio",
    "Informacao e comunicacao",
    "Atividades Financeiras",
    "Atividades Imobiliarias",
    "Outras atividades",
    "ADM, defesa, etc",
    "Total Servicos",
    "VA",
    "PIB",
    "Consumo das Familias",
    "Consumo do Governo",
    "FBCF",
    "Exportacao",
    "Importacao"
]

Agropecuaria = ['Agropecuaria']

Industria = [
    "Industria Extrativa",
    "Industria de Transformacao",
    "Eletricidade e agua",
    "Construcao",
    "Total Industria"
]

Servicos = [
    "Comercio",
    "Transporte, armazenagem e correio",
    "Informacao e comunicacao",
    "Atividades Financeiras",
    "Atividades Imobiliarias",
    "Outras atividades",
    "ADM, defesa, etc",
    "Total Servicos",
]

Demanda = [
    "Consumo das Familias",
    "Consumo do Governo",
    "FBCF",
    "Exportacao",
    "Importacao"
]

Oferta = [
    'Agropecuaria',
    "Total Industria",
    "Total Servicos",
]

df = pd.read_excel('./raw/ContasNacionais/Tab_Compl_CNT.xlsx', header=3, sheet_name='Val encad preços 95 com ajuste', index_col=0)
df.index = df.index.str.replace('.', 'Q').str.replace('IV', '4').str.replace('III', '3').str.replace('II', '2').str.replace('I', '1')
df.index = pd.PeriodIndex(df.index, freq='Q')
df.columns = Colunas
df["Importacao"] = -df["Importacao"]

fig = plt.figure(figsize=(9,4))
ax = plt.axes()
ax2 = plt.axes([0.15,0.6,0.2,0.2])

suptitle = 'Taxa de crescimento'
title = 'Trimestre contra trimestre anterior'


df['PIB'].pct_change().tail(4).plot(kind='bar', ax=ax, color='darkblue')
ax.axhline(y=0, ls='--', color='black')

plt.suptitle(suptitle, color='black', weight = 'bold')
ax.set_title(title, color='black')

ax.text(0.95, -0.2, 'Fonte: IBGE',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

ax.text(0.6, -0.2, 'Atualizado em {}. Último dado disponível: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y"), df.index[-1]),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

#sns.set_style("white")
sns.set_context('paper', font_scale=1.2)
sns.despine()
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.yaxis.label.set_color('black')
ax.xaxis.label.set_color('black')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
sns.set_style('white')
fig.savefig('./figs/PIB/PIB.png')
plt.show()

print(df['PIB'].pct_change().tail(4))

fig, ax = plt.subplots(figsize=(9,4))
ax2 = fig.add_axes([0.15,0.6,0.2,0.2])


df[Agropecuaria].pct_change().tail(4).plot(kind='bar', ax=ax, color='darkblue')

plt.suptitle('Agricultura', color='black', weight = 'bold')
ax.axhline(y=0, color='gray', linestyle='--', lw=2)

ax.set_title('Trimestre contra trimestre anterior', color='black')

ax.text(0.95, -0.2, 'Fonte: IBGE',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

ax.text(0.6, -0.2, 'Atualizado em {}. Último dado disponível: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y"), df.index[-1]),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

#sns.set_style("white")
sns.set_context('paper', font_scale=1.2)
sns.despine()
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.yaxis.label.set_color('black')
ax.xaxis.label.set_color('black')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

fig.savefig('./figs/PIB/Agropecuaria.png')
plt.show()

fig, ax = plt.subplots(figsize=(9,4))
ax2 = fig.add_axes([0.15,0.6,0.2,0.2])


df[Industria].pct_change().tail(4).plot(kind='bar', ax=ax)

plt.suptitle('Indústria', color='black', weight = 'bold')
ax.axhline(y=0, color='gray', linestyle='--', lw=2)

ax.set_title('Trimestre contra trimestre anterior', color='black')

ax.text(0.95, -0.2, 'Fonte: IBGE',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

ax.text(0.6, -0.2, 'Atualizado em {}. Último dado disponível: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y"), df.index[-1]),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

#sns.set_style("white")
sns.set_context('paper', font_scale=1.2)
sns.despine()
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.yaxis.label.set_color('black')
ax.xaxis.label.set_color('black')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
plt.show()
fig.savefig('./figs/PIB/Industria.png')

print(df[Industria].pct_change().tail(4))

fig, ax = plt.subplots(figsize=(9,4))
ax2 = fig.add_axes([0.15,0.6,0.2,0.2])


df[Servicos].pct_change().tail(4).plot(kind='bar', ax=ax)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


plt.suptitle('Serviços', color='black', weight = 'bold')

ax.axhline(y=0, color='gray', linestyle='--', lw=2)

ax.set_title('Trimestre contra trimestre anterior', color='black')

ax.text(0.95, -0.2, 'Fonte: IBGE',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

ax.text(0.6, -0.2, 'Atualizado em {}. Último dado disponível: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y"), df.index[-1]),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

#sns.set_style("white")
sns.set_context('paper', font_scale=1.2)
sns.despine()
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.yaxis.label.set_color('black')
ax.xaxis.label.set_color('black')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
plt.show()
fig.savefig('./figs/PIB/Servicos.png')

print(df[Servicos].pct_change())

fig, ax = plt.subplots(figsize=(9,4))
ax2 = fig.add_axes([0.15,0.6,0.2,0.2])


df[Demanda + ['PIB']].pct_change().tail(4).plot(kind='bar', ax=ax)

plt.suptitle('Demanda', color='black', weight = 'bold')
ax.axhline(y=0, color='gray', linestyle='--', lw=2)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


ax.set_title('Trimestre contra trimestre anterior', color='black')

ax.text(0.95, -0.2, 'Fonte: IBGE',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

ax.text(0.6, -0.2, 'Atualizado em {}. Último dado disponível: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y"), df.index[-1]),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

#sns.set_style("white")
sns.set_context('paper', font_scale=1.2)
sns.despine()
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.yaxis.label.set_color('black')
ax.xaxis.label.set_color('black')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
plt.show()
fig.savefig('./figs/PIB/Demanda.png')

print(df[Demanda + ['PIB']].pct_change().tail(4))

fig, ax = plt.subplots(figsize=(9,4))
ax2 = fig.add_axes([0.15,0.6,0.2,0.2])


df[Oferta + ['PIB']].pct_change().tail(4).plot(kind='bar', ax=ax)

plt.suptitle('Oferta', color='black', weight = 'bold')
ax.axhline(y=0, color='gray', linestyle='--', lw=2)
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


ax.set_title('Trimestre contra trimestre anterior', color='black')

ax.text(0.95, -0.2, 'Fonte: IBGE',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

ax.text(0.6, -0.2, 'Atualizado em {}. Último dado disponível: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y"), df.index[-1]),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

#sns.set_style("white")
sns.set_context('paper', font_scale=1.2)
sns.despine()
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.yaxis.label.set_color('black')
ax.xaxis.label.set_color('black')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
plt.show()
fig.savefig('./figs/PIB/Oferta.png')

print(df[Oferta + ['PIB']].pct_change().tail(4))

fig = plt.Figure()
ax = plt.gca()
ax2 = fig.add_axes([0.15,0.7,0.2,0.2])

df[Demanda].diff().apply(lambda x: x/(df["PIB"].shift())).tail(8).plot(
    kind = 'bar', 
    stacked = True, 
    ax = ax,
    color = (
        "tomato",
        "darkred",
        "darkslateblue",
        "tan",
        "khaki"
    ),
    width = 0.75,
    edgecolor='black'
)
plt.suptitle('Demanda', color='black', weight = 'bold')
ax.axhline(y=0, color='black', linestyle='-', lw=2)
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


ax.set_title('Contribuição para variação do PIB', color='black')

ax.text(0.95, -0.3, 'Fonte: IBGE',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

ax.text(0.6, -0.3, 'Atualizado em {}. Último dado disponível: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y"), df.index[-1]),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

#sns.set_style("white")
sns.set_context('paper', font_scale=1.2)
sns.despine()
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.yaxis.label.set_color('black')
ax.xaxis.label.set_color('black')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 
#ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
plt.show()
fig.savefig('./figs/PIB/Contrib_Demanda.png')

print(df[Demanda].diff().apply(lambda x: x/(df["PIB"].shift())).tail(8))

fig, ax = plt.subplots(1,1,figsize=(9,4))
ax2 = fig.add_axes([0.15,0.6,0.2,0.2])


#df["PIB"].pct_change().tail(12).plot(ax = ax, kind = 'line', legend = True, color = 'black')
df[Oferta].diff().apply(lambda x: x/(df["VA"].shift())).tail(8).plot(
    kind = 'bar', 
    stacked = True, 
    ax = ax,
    color = (
        "green",
    #    "darkred",
        "darkslateblue",
        "tan",
    #    "khaki"
    ),
    cmap="Set1",
    width = 0.75,
    edgecolor='black'
)

plt.suptitle('Oferta', color='black', weight = 'bold')
ax.axhline(y=0, color='black', linestyle='-', lw=2)
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


ax.set_title('Contribuição para variação do valor adicionado', color='black')

ax.text(0.95, -0.3, 'Fonte: IBGE',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

ax.text(0.6, -0.3, 'Atualizado em {}. Último dado disponível: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y"), df.index[-1]),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=10)

#sns.set_style("white")
sns.set_context('paper', font_scale=1.2)
sns.despine()
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.yaxis.label.set_color('black')
ax.xaxis.label.set_color('black')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y))) 
#ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
plt.show()
fig.savefig('./figs/PIB/Contrib_Oferta.png')

print(df[Oferta].diff().apply(lambda x: x/(df["VA"].shift())).tail(8))
