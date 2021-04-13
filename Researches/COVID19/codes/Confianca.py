%config InlineBackend.figure_format = 'retina'
import sys

sys.path.insert(1, './codes/')

from setup import *

start_year = "2019-01-01"

file_path = './raw/LCA/'
image_path = './figs/Confianca/'

file_name = 'Sondagem_Conjuntural_Mensal_FGV'
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name='Com Ajuste CNAE 2.0', 
    parse_dates=True,
    index_col=[0], 
    skiprows=10,
    na_values = '-'
)[1:][start_year:]
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''

# Interpolating
df = interpolator(df)


fig, ax = plt.subplots(figsize=(8,5))
df.drop(['NUCI'], axis='columns').plot(
    title = file_name.replace('_', ' '),
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Sondagem_Servicos_FGV'
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name='ICS_dessaz', 
    parse_dates=True,
    index_col=[0], 
    skiprows=10,
    na_values = '-',
)[1:][start_year:]
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''
df = interpolator(df)
fig, ax = plt.subplots(figsize=(8,5))
df.drop(['Índice de Confiança de Serviços (ICS) .1', 'NUCI'], axis='columns').plot(
    title = file_name.replace('_', ' '),
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Sondagem_do_Comercio_FGV'
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name='dessaz CNAE 2.0', 
    parse_dates=True,
    index_col=[0], 
    skiprows=11,
    na_values = '-',
)
df.index = pd.date_range( # Check for NaN
    start = '2010-03-01',
    periods=df.shape[0],
    #end='2020-05-31',
    freq='M', 
    #periods=(1241-12)
    )
df.index.name = ''
df = df[start_year:]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = file_name.replace('_', ' '),
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, 
           color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)', )
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

file_name = 'Sondagem_Construcao_FGV'
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name='Com ajuste CNAE 2.0', 
    parse_dates=True,
    index_col=[0], 
    skiprows=10,
    na_values = '-',
)[1:][start_year:]
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.drop(['NUCI'], axis='columns').plot(
    title = file_name.replace('_', ' '),
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )

agregadas = [
    'Total',
    'Ind. Extrativa',
    'Ind. de Transformação'
]
def importer(sheet='Volume Produção', skip_rows=10, initial=1):
    file_name = 'Sondagem_Industrial_CNI'
    df = pd.read_excel(
        file_path + file_name + '.xlsx', 
        sheet_name=sheet, 
        parse_dates=True,
        index_col=[0], 
        skiprows=skip_rows, na_values='-'
    )[initial:][start_year:]
    df.index = pd.to_datetime(df.index, format="%Y-%m")
    df.index.name = ''
    return df

file_name = 'Sondagem_Industrial_CNI'

sheet='Volume Produção'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Evolução Empr'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='NUCI'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='NUCI Efetivo-Usual'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Evolução Estoques'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Estoques Efetivos'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)


fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Expec Demanda'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Expec Exportação'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Expec Compra Mat. Prima'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Expec Emprego'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Expec Investimento'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

agregadas = [
    'Total',
    'Ind. Extrativa',
    'Ind. de Transformação'
]
def importer(sheet='Lucro Operacional', skip_rows=10, initial=1):
    file_name = 'Sondagem_Industrial_CNI'
    df = pd.read_excel(
        file_path + file_name + '.xlsx', 
        sheet_name=sheet, 
        parse_dates=True,
        index_col=[0], 
        skiprows=skip_rows, na_values='-'
    )[initial:]
    df.index = pd.date_range(
    start = '2007-07-31',
    periods=df.shape[0],
    freq='Q', 
    )
    df.index.name = ''
    return df

sheet='Lucro Operacional'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas]["2019-01-01":].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Situação Financeira'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

sheet='Acesso Crédito'
df = importer(sheet=sheet, initial=1, skip_rows=11)
df.columns = ['Total' if coluna == "Unnamed: 1" else coluna for coluna in df.columns]
df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df[agregadas].plot(
    title = file_name.replace('_', ' ')+'\n' + sheet,
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
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

df = web.DataReader(
    'MEI_CLI', # https://stats.oecd.org/Index.aspx?DataSetCode=MEI_CLI
    'oecd', 
    start='2007-01-01'
)
type = [
    #"Original, seasonally adjusted (GDP)",
    "Amplitude adjusted (CLI)",
    #"Normalised (CLI)",
    #"Normalised (GDP)",
    #"Trend restored (CLI)",
]
df = df.transpose().loc[(
    type[0]
),:]
df = df.reset_index()
df = df[df["Frequency"] == "Monthly"].drop(["Frequency"], axis='columns')
df = df.transpose()
df.columns = cc.convert(names = list(df.loc["Country"]), to = 'ISO3', not_found=None) # To avoid string problems
df.columns.name = ''
df.drop(['Country'], inplace=True)
df.index.name = ''
df.index = pd.date_range(
    start = df.index[0],
    end = f"{str(df.index[-1])[:6]}{int(str(df.index[-1])[6])+1}{str(df.index[-1])[7:]}",
    freq='M', 
)

df.to_csv('./raw/Dados de Confiança/CLI.csv')

cases = ["USA", "ESP", "ITA", "G7", "OECD total "]
source = f"Source: OECD\nLast query: {dt.today():%d/%m/%y}"
df = df['2019':][cases + ["BRA"]]

df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))

df['2019':][cases].plot(ax=ax, lw=2)
df['2019':][["BRA"]].plot(ax=ax, lw=3, color='darkred',)
ax.set_title(f"Composite Leading Indicators (MEI)\n{type[0]}", fontweight='bold')
fig.text(0.79, .28, source, ha='left')
ax.axvline(
    x=corona_sp, label=corona_sp_txt,
           ls='--', color='black', lw=1.5, )
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.tight_layout()
sns.despine()
plt.show()

df = web.DataReader(
    'MEI_CLI', # https://stats.oecd.org/Index.aspx?DataSetCode=MEI_CCI
    'oecd', 
    start='2007-01-01'
)
df = df.transpose().loc[(
    'OECD Standardised CCI, Amplitude adjusted (Long term average=100), sa',
    #"Normalised (CLI)",
    #"Normalised (GDP)",
    #"Trend restored (CLI)",
),:]
df = df.reset_index()
df = df[df["Frequency"] == "Monthly"].drop(["Frequency"], axis='columns')
df = df.transpose()
df.columns = cc.convert(names = list(df.loc["Country"]), to = 'ISO3', not_found=None) # To avoid string problems
df.columns.name = ''
df.drop(['Country'], inplace=True)
df.index.name = ''
df.index = pd.date_range(
    start = df.index[0],
    end = f"{str(df.index[-1])[:6]}{int(str(df.index[-1])[6])+1}{str(df.index[-1])[7:]}",
    freq='M', 
)
df = interpolator(df)
df.to_csv('./raw/Dados de Confiança/CCI.csv')


cases = ["USA", "ESP", "ITA", "G7", "OECD total "]
source = f"Source: OECD\nLast query: {dt.today():%d/%m/%y}"

fig, ax = plt.subplots(figsize=(8,5))

df['2019':][cases].plot(ax=ax, lw=2)
df['2019':][["BRA"]].plot(ax=ax, lw=3, color='darkred',)
ax.set_title("Índice de Confiança do Consumidor (CCI)", fontweight='bold')
fig.text(0.79, .28, source, ha='left')
ax.axvline(x=corona_sp, label=corona_sp_txt,
           ls='--', color='black', lw=1.5, )
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
sns.despine()
plt.show()

file_name = 'embiplus'
df = pd.read_excel(
    file_path + file_name + '.xlsx', 
    sheet_name='EMBI', 
    parse_dates=True,
    index_col=[0], 
    skiprows=11,
    na_values = '-',
)[1:][start_year:]
df.index = pd.to_datetime(df.index, format="%Y-%m")
df.index.name = ''
df = df[[
#    "Argentina",
    "Brasil",
    "Europa",
    "Latin",
    "Rússia",
    "China",
    "Coréia do Sul",
]]

df = interpolator(df)

fig, ax = plt.subplots(figsize=(8,5))
df.plot(
    title = "EMBI+ (JP Morgan)",
    ax = ax,
    lw = 2.5
)
ax.axvline(x = corona_sp, color='black', ls='--', lw=1, label='Início do isolamento em SP\n(24 de março)')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2 = plt.axes([0.135,0.135,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')

sns.despine()
plt.show()

fig.savefig(
    image_path + file_name + '.svg',
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
    )
