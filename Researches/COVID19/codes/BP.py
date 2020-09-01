%config InlineBackend.figure_format = 'retina'
import sys

sys.path.insert(1, './codes/')

from setup import *


file_path = './raw/LCA/'
image_path = './figs/SetorExterno/'
start_year = "2019-01-01"

file_name = 'Balanca_Comercial_Total_MDIC'
sheet = "Saldo Semanal"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
)[0:]
df.drop(['Semana Referência', 'Número dias úteis'], axis='columns', inplace=True)
df.drop('Período', inplace=True)
df.index.name = ''

df.columns = [
    "Exportações",
    "Exportações Média diária",
    "Importações",
    "Importações Média diária",
    "Saldo Comercial",
    "Saldo Comercial Média diária",
]


df.index = pd.date_range( # Check for NaN
    start=df.index[1][:10],
    periods=df.shape[0],
    end=df.index[-1][:10],
    #periods=(1241-12)
    )

df = df[start_year:]

fig, ax = plt.subplots(figsize=(8,5))
df[['Exportações', 'Importações', 'Saldo Comercial']].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
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
    image_path + file_name + "_" + sheet.replace(' ', '') + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Balanca_Comercial_Total_MDIC'
sheet = "Saldo Mensal"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True,
    index_col=[0], 
    skiprows=11, 
    thousands='.'
)[0:]
df = df.apply(pd.to_numeric)
# df.index = pd.date_range(
#     start = '1999-05-01',
#     periods=df.shape[0],
#     #end='2020-05-31',
#     freq='M', 
#     #periods=(1241-12)
#     )
df.index = pd.to_datetime(df.index, format="%Y-%m")
df = df[start_year:]
df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.drop(['DU'], axis='columns').plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
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
    image_path + file_name + "_" + sheet.replace(' ', '') + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Exportacao_Importacao_FUNCEX'
sheet = "Funcex Dessaz"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True,
    index_col=[0], 
    skiprows=11, 
)[0:]
df = df.apply(pd.to_numeric)
df.index = pd.to_datetime(df.index, format="%Y-%m")
df = df[start_year:]
df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
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
    image_path + file_name + "_" + sheet.replace(' ', '') + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Conta_Corrente_pct_PIB_Bacen_BPM6'
sheet = "Conta Corrente"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True,
    index_col=[0], 
    skiprows=11, 
    na_values='-' 
)[0:]
df = df.apply(pd.to_numeric)
df.index = pd.to_datetime(df.index, format="%Y-%m")
df = df[start_year:]
df.index.name = ''
df.columns = [
    "STC Mensal", "STC últimos 12 meses", "Saldo de Transações Correntes",
    "IED Mensal", "IED últimos 12 meses", "Investimento Externo Direto",
    "NFE Mensal", "NFE últimos 12 meses", "Necessidade Financiamento Externo",
    "PIB últimos 12 meses"
]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[[
    "Saldo de Transações Correntes",
    "Investimento Externo Direto",
    "Necessidade Financiamento Externo"
]].plot(
    title = sheet + "\n(em % PIB)",
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
    image_path + file_name + "_" + sheet.replace(' ', '') + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Balanca_Comercial_por_Pais_Funcex'
sheet = "Exportações Mensal"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True,
    index_col=[0], 
    skiprows=11, 
    na_values='-' 
)[0:]
df = df.apply(pd.to_numeric)
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''
principais = df.iloc[-1].sort_values(ascending=False).index[:7].to_list()
outros = df.iloc[-1].sort_values(ascending=False).index[7:].to_list()

fig, ax = plt.subplots(figsize=(8,5))
df.iloc[-1].sort_values(ascending=False).plot(
    title = file_name.replace("_", " ") + "\n" + sheet,
    ax = ax,
    kind='bar', 
    color='lightgray',
    edgecolor='black',
    lw=2, 
    zorder=1,
    stacked=False,
    label=f"{df.index[-1]: %b de %Y}",
    alpha=.5
)
df.iloc[-2].sort_values(ascending=False).plot(
    title = file_name.replace("_", " ") + "\n" + sheet,
    ax = ax,
    kind='bar', 
    edgecolor='black',
    lw=2, 
    zorder=0,
    color='black',
    stacked=False,
    label=f"{df.index[-2]: %b de %Y}"
)
df.iloc[-3].sort_values(ascending=False).plot(
    title = file_name.replace("_", " ") + "\n" + sheet,
    ax = ax,
    kind='bar', 
    edgecolor='black',
    lw=2, 
    zorder=-1,
    color='white',
    stacked=False,
    label=f"{df.index[-3]: %b de %Y}"
)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + "_" + sheet.replace(' ', '') + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Balanca_Comercial_por_Pais_Funcex'
sheet = "Exportações Mensal"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True,
    index_col=[0], 
    skiprows=11, 
    na_values='-' 
)[0:]
df = df.apply(pd.to_numeric)
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''
df["Outros"] = df[outros].sum(axis=1)
df = df[principais + ["Outros"]]

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = file_name.replace("_", " ") + "\n" + sheet + "\n Série histórica",
    ax = ax,
    kind='bar', 
    edgecolor='black',
    lw=2, 
    stacked=True,
)

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

def line_format(label):
    """
    Convert time label to the format of pandas line plot
    """
    month = label.month_name()[:3]
    if month == 'Jan':
        month += f'\n{label.year}'
    return month
ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))
# Define the date format
ax2 = plt.axes([0.7,0.7,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + "_" + sheet.replace(' ', '') + "_SerieHistorica" +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Balanca_Comercial_por_Pais_Funcex'
sheet = "Importações Mensal"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True,
    index_col=[0], 
    skiprows=11, 
    na_values='-' 
)[0:]
df = df.apply(pd.to_numeric)
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''
principais = df.iloc[-1].sort_values(ascending=False).index[:7].to_list()
outros = df.iloc[-1].sort_values(ascending=False).index[7:].to_list()

fig, ax = plt.subplots(figsize=(8,5))
df.iloc[-1].sort_values(ascending=False).plot(
    title = file_name.replace("_", " ") + "\n" + sheet,
    ax = ax,
    kind='bar', 
    color='gray',
    edgecolor='black',
    lw=2, 
    zorder=1,
    stacked=False,
    label=f"{df.index[-1]: %b de %Y}",
    alpha=.5
)
df.iloc[-2].sort_values(ascending=False).plot(
    title = file_name.replace("_", " ") + "\n" + sheet,
    ax = ax,
    kind='bar', 
    edgecolor='black',
    lw=2, 
    zorder=0,
    color='black',
    stacked=False,
    label=f"{df.index[-2]: %b de %Y}"
)
df.iloc[-3].sort_values(ascending=False).plot(
    title = file_name.replace("_", " ") + "\n" + sheet,
    ax = ax,
    kind='bar', 
    edgecolor='black',
    lw=2, 
    zorder=-1,
    color='white',
    stacked=False,
    label=f"{df.index[-3]: %b de %Y}"
)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + "_" + sheet.replace(' ', '') + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Balanca_Comercial_por_Pais_Funcex'
sheet = "Importações Mensal"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True,
    index_col=[0], 
    skiprows=11, 
    na_values='-' 
)[0:]
df = df.apply(pd.to_numeric)
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''
df["Outros"] = df[outros].sum(axis=1)
df = df[principais + ["Outros"]]

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = file_name.replace("_", " ") + "\n" + sheet + "\n Série histórica",
    ax = ax,
    kind='bar', 
    edgecolor='black',
    lw=2, 
    stacked=True,
)

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

def line_format(label):
    """
    Convert time label to the format of pandas line plot
    """
    month = label.month_name()[:3]
    if month == 'Jan':
        month += f'\n{label.year}'
    return month
ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))
# Define the date format
ax2 = plt.axes([0.7,0.7,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + "_" + sheet.replace(' ', '') + "_SerieHistorica" +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Balanca_Comercial_por_Pais_Funcex'
sheet = "Saldo Comercial Mensal"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True,
    index_col=[0], 
    skiprows=11, 
    na_values='-' 
)[0:]
df = df.apply(pd.to_numeric)
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''
principais = df.iloc[-1].sort_values(ascending=False).index[:7].to_list()
outros = df.iloc[-1].sort_values(ascending=False).index[7:].to_list()


fig, ax = plt.subplots(figsize=(8,5))
df.iloc[-1].sort_values(ascending=False).plot(
    title = file_name.replace("_", " ") + "\n" + sheet,
    ax = ax,
    kind='bar', 
    color='lightgray',
    edgecolor='black',
    lw=2, 
    zorder=1,
    stacked=False,
    label=f"{df.index[-1]: %b de %Y}",
    alpha=.5
)
df.iloc[-2].sort_values(ascending=False).plot(
    title = file_name.replace("_", " ") + "\n" + sheet,
    ax = ax,
    kind='bar', 
    edgecolor='black',
    lw=2, 
    zorder=0,
    color='black',
    stacked=False,
    label=f"{df.index[-2]: %b de %Y}"
)
df.iloc[-3].sort_values(ascending=False).plot(
    title = file_name.replace("_", " ") + "\n" + sheet,
    ax = ax,
    kind='bar', 
    edgecolor='black',
    lw=2, 
    zorder=-1,
    color='white',
    stacked=False,
    label=f"{df.index[-3]: %b de %Y}"
)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + "_" + sheet.replace(' ', '') + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Balanca_Comercial_por_Pais_Funcex'
sheet = "Saldo Comercial Mensal"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True,
    index_col=[0], 
    skiprows=11, 
    na_values='-' 
)[0:]
df = df.apply(pd.to_numeric)
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''
df["Outros"] = df[outros].sum(axis=1)
df = df[principais + ["Outros"]]

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = file_name.replace("_", " ") + "\n" + sheet + "\n Série histórica",
    ax = ax,
    kind='bar', 
    edgecolor='black',
    lw=2, 
    stacked=True,
)

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.axhline(y=0, ls='-', lw=1, color='black')

def line_format(label):
    """
    Convert time label to the format of pandas line plot
    """
    month = label.month_name()[:3]
    if month == 'Jan':
        month += f'\n{label.year}'
    return month
ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))
# Define the date format
ax2 = plt.axes([0.7,0.7,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + "_" + sheet.replace(' ', '') + "_SerieHistorica" +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )
