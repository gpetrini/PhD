%config InlineBackend.figure_format = 'retina'
import sys

sys.path.insert(1, './codes/')

from setup import *

start_year = "2019-01-01"

file_path = './raw/LCA/'
image_path = './figs/Credito/'
file_name = 'Indicadores_de_Credito_Bacen'
def line_format(label):
    """
    Convert time label to the format of pandas line plot
    """
    month = label.month_name()[:3]
    if month == 'Jan':
        month += f'\n{label.year}'
    return month
#ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))

sheet = "SaldoPJ"
titulo = "Saldo Pessoa jurídica"
porcentagem=False
unidade="Milhões"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,Z,AM", 
)[0:]
df.index = pd.date_range( # Check for NaN
    start = '2007-03-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df = df[start_year:]
df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = titulo,
    ax = ax,
    lw=2, 
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento\nsocial em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if porcentagem == False:
    ax.set_yticklabels(['{:,.0f}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'R$ {unidade}')
else: 
    ax.set_yticklabels(['{:,.2%}'.format(x/100) for x in ax.get_yticks()])
    ax.set_ylabel(f'em % {unidade}')
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +   '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

sheet = "SaldoPJ"
titulo = "Saldo Pessoa jurídica"
porcentagem=False
unidade="Milhões"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,Z,AM", 
)[0:]
df.index = pd.date_range( # Check for NaN
    start = '2007-03-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.pct_change(12)[start_year:].plot(
    title = titulo,
    ax = ax,
    lw=2, 
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento\nsocial em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +   '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

sheet = "SaldoPF"
titulo = "Saldo Pessoa física"
porcentagem=False
unidade="Milhões"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,W,AJ", 
)[0:]
df.index = pd.date_range( # Check for NaN
    start = '2007-03-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df = df[start_year:]
df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = titulo,
    ax = ax,
    lw=2, 
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento\nsocial em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if porcentagem == False:
    ax.set_yticklabels(['{:,.0f}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'R$ {unidade}')
else: 
    ax.set_yticklabels(['{:,.2%}'.format(x/100) for x in ax.get_yticks()])
    ax.set_ylabel(f'em % {unidade}')
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +   '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

sheet = "SaldoPF_%PIB"
titulo = "Saldo Pessoa física\nem % PIB"
porcentagem=True
unidade="PIB"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,W,AJ", 
)[0:]
df.index = pd.date_range( # Check for NaN
    start = '2007-03-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df = df[start_year:]
df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = titulo,
    ax = ax,
    lw=2, 
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento\nsocial em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if porcentagem == False:
    ax.set_yticklabels(['{:,.0f}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'R$ {unidade}')
else: 
    ax.set_yticklabels(['{:,.2%}'.format(x/100) for x in ax.get_yticks()])
    ax.set_ylabel(f'em % {unidade}')
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +   '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

sheet = "SaldoCréditoAmpliado"
titulo = "Saldo Crédito Ampliado"
porcentagem=True
unidade="do Total"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,N,V,AJ", 
)[0:]
df.columns = [
    "Setor não financeiro",
    "Governo Geral",
    "Empresas e Famílias"
]
df.index = pd.date_range( # Check for NaN
    start = '2013-01-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df = df[start_year:]
df["Total"] = df.sum(axis=1)
df = df.apply(lambda x: x/df["Total"]).drop(["Total"], axis='columns')

df.index.name = ''


fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = titulo,
    ax = ax,
    kind='bar', stacked=True, edgecolor='black',
    lw=2, 
)
ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))
#ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento\nsocial em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if porcentagem == False:
    ax.set_yticklabels(['{:,.0f}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'R$ {unidade}')
else: 
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'em % {unidade}')
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

sheet = "SaldoCréditoAmpliado"
titulo = "Saldo Crédito Ampliado"
porcentagem=False
unidade="Milhões"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,N,V,AJ", 
)[0:]
df.columns = [
    "Setor não financeiro",
    "Governo Geral",
    "Empresas e Famílias"
]
df.index = pd.date_range( # Check for NaN
    start = '2013-01-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df = df[start_year:]
#df["Total"] = df.sum(axis=1)
#df = df.apply(lambda x: x/df["Total"]).drop(["Total"], axis='columns')

df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = titulo,
    ax = ax,
    #kind='bar', stacked=True, edgecolor='black',
    lw=2, 
)
ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento\nsocial em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if porcentagem == False:
    ax.set_yticklabels(['{:,.0f}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'R$ {unidade}')
else: 
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'em % {unidade}')
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +   '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

sheet = "SaldoCréditoAmpliado_%PIB"
titulo = "Saldo Crédito Ampliado"
porcentagem=True
unidade="PIB"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,N,V,AJ", 
)[0:]
df.columns = [
    "Setor não financeiro",
    "Governo Geral",
    "Empresas e Famílias"
]
df.index = pd.date_range( # Check for NaN
    start = '2013-01-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df = df[start_year:]
#df["Total"] = df.sum(axis=1)
#df = df.apply(lambda x: x/df["Total"]).drop(["Total"], axis='columns')

df.index.name = ''

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = titulo,
    ax = ax,
    #kind='bar', stacked=True, edgecolor='black',
    lw=2, 
)
ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))
#ax.axvline(x = corona, color='black', ls='--', lw=1, label='Mais de 60 casos de COVID19')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if porcentagem == False:
    ax.set_yticklabels(['{:,.0f}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'R$ {unidade}')
else: 
    ax.set_yticklabels(['{:,.0%}'.format(x/100) for x in ax.get_yticks()])
    ax.set_ylabel(f'em % {unidade}')
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +   '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

sheet = "SaldoDirecionado"
titulo = "Saldo Crédito Direcionado"
porcentagem=False
unidade="Milhões"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,D,G,,K,L", 
)[0:]
df.columns = [
    "Rural",
    "Financiamento Imobiliário",
    "BNDES",
    "Outros"
]
df.index = pd.date_range( # Check for NaN
    start = '2007-03-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df = df[start_year:]

df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = titulo,
    ax = ax,
    #kind='bar', stacked=True, edgecolor='black',
    lw=2, 
)
#ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento\nsocial em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if porcentagem == False:
    ax.set_yticklabels(['{:,.2f}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'R$ {unidade}')
else: 
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'em % {unidade}')
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

sheet = "SaldoDirecionado"
titulo = "Saldo Crédito Direcionado"
porcentagem=True
unidade="do Total"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,D,G,,K,L", 
)[0:]
df.columns = [
    "Rural",
    "Financiamento Imobiliário",
    "BNDES",
    "Outros"
]
df.index = pd.date_range( # Check for NaN
    start = '2007-03-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df = df[start_year:]
df["Total"] = df.sum(axis=1)
df = df.apply(lambda x: x/df["Total"]).drop(["Total"], axis='columns')


df.index.name = ''

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = titulo,
    ax = ax,
    kind='bar', stacked=True, edgecolor='black',
    lw=2, 
)
ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))
#ax.axvline(x = corona, color='black', ls='--', lw=1, label='Mais de 60 casos de COVID19')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if porcentagem == False:
    ax.set_yticklabels(['{:,.2f}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'R$ {unidade}')
else: 
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'em % {unidade}')
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

sheet = "SaldoDirecionado_%PIB"
titulo = "Saldo Crédito Direcionado"
porcentagem=True
unidade="PIB"
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name=sheet, 
    parse_dates=True, # Check data-parser -> %m/%Y not %m/%d
    index_col=[0], 
    skiprows=10,
    usecols="A,D,G,,K,L", 
)[0:]
df.columns = [
    "Rural",
    "Financiamento Imobiliário",
    "BNDES",
    "Outros"
]
df.index = pd.date_range( # Check for NaN
    start = '2007-03-31',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df = df[start_year:]
# df["Total"] = df.sum(axis=1)
# df = df.apply(lambda x: x/df["Total"]).drop(["Total"], axis='columns')


df.index.name = ''

df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[start_year:].plot(
    title = titulo,
    ax = ax,
    #kind='bar', stacked=True, edgecolor='black',
    lw=2, 
)
ax.set_xticklabels(map(lambda x: line_format(x), df[start_year:].index))
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início isolamento\nsocial em SP')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if porcentagem == False:
    ax.set_yticklabels(['{:,.2f}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f'R$ {unidade}')
else: 
    ax.set_yticklabels(['{:,.0%}'.format(x/100) for x in ax.get_yticks()])
    ax.set_ylabel(f'em % {unidade}')
ax2 = plt.axes([.9,0.6,0.2,0.2])


ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')


sns.despine()
plt.show()

fig.savefig(
    image_path + sheet.replace(' ', '') + unidade +  '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )
