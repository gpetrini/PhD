%config InlineBackend.figure_format = 'retina'

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader.data as web
import datetime
from datetime import datetime as dt

sns.set_context('paper')
plt.style.use('seaborn-white')

start = datetime.datetime(1951, 12, 1)
end = datetime.datetime(2019, 3, 1)

def salvar_grafico(file_name, extension=".png", pasta="./figs/"):
    fig.savefig(pasta + file_name + extension, dpi = 300, bbox_inches = 'tight',
    pad_inches = 0.2, transparent = False,)

def crise_subprime(axes, alpha=0.4):
    axes.axvspan(
    xmin='2007-12-01', 
    xmax='2009-06-01',
    color='gray', 
    label='Subprime Crises',
    zorder=0,
    alpha=alpha
)

def crises(axes, color='lightgray', alpha=0.4):
    axes.axvspan(xmin = "1953-07", xmax='1954-04', color = color, alpha=alpha, label = 'Recession')
    axes.axvspan(xmin = "1957-08", xmax='1958-05', color = color, alpha=alpha, label = '')
    axes.axvspan(xmin = "1960-05", xmax='1961-02', color = color, alpha=alpha, label = '')
    axes.axvspan(xmin = "1969-12", xmax='1970-11', color = color, alpha=alpha, label = '')
    axes.axvspan(xmin = "1973-11", xmax='1975-03', color = color, alpha=alpha, label = '')
    axes.axvspan(xmin = "1980-01", xmax='1980-07', color = color, alpha=alpha, label = '')
    axes.axvspan(xmin = "1981-07", xmax='1982-01', color = color, alpha=alpha, label = '')
    axes.axvspan(xmin = "1990-07", xmax='1991-03', color = color, alpha=alpha, label = '')
    axes.axvspan(xmin = "2001-03", xmax='2001-11', color = color, alpha=alpha, label = '')

df = web.DataReader(
    [
        'GDP',
        'PRFI',
        'PNFI',
        'TCU',
        'PCDG',
    ], 
    'fred', 
    start, end
)
df['TCU'] = df['TCU']/100
df['H-GFI'] = df['PRFI']/df['PNFI']
df['H-GDP'] = df['PRFI']/df['GDP']
df['Investment share'] = df['PNFI']/df['GDP']
df['Housing share'] = df['PRFI']/df['GDP']
df["Durables"] = df["PCDG"]/df["GDP"]
df['Year'] = df.index.year
df = df.resample('Q').last()
df.index.name = ''
df.to_csv('./data/Cycle.csv')

start=dt(1987,1,1)
end=dt(2019,10,1)

df = web.DataReader(
    [
        "PRFI",
        "CSUSHPISA",
        "MORTGAGE30US",
        "CPIAUCSL"
    ], 
    'fred', 
    start, 
    end
)

df.columns = [
    "Residential investment", 
    "House prices", 
    "Mortgage interest rate",
    "General Prices"
]
df.index.name = ""


df['Mortgage interest rate'] = df['Mortgage interest rate'].divide(100)
df = df.resample('M').last()

df['House prices'] = df['House prices']/df['House prices'][0]
df = df.resample('Q').last()
df["Inflation"]= df["House prices"].pct_change()
df["General inflation"] = df["General Prices"].pct_change()
df["Own interest rate"] = ((1+df["Mortgage interest rate"])/(1+df["Inflation"])) -1
df["Real mortgage interest rate"] = ((1+df["Mortgage interest rate"])/(1+df["General inflation"])) -1

df['$g_{I_h}$'] = df["Residential investment"].pct_change()
df.to_csv("./data/OwnInterestRate_data.csv")

df = pd.read_csv(
    './data/OwnInterestRate_data.csv',
    index_col = [0],
    parse_dates = True
)

df = df.merge(
    pd.read_csv(
        './data/Cycle.csv',
        index_col = [0],
        parse_dates = True
    ),
    left_index=True, right_index=True
)

sns.set_context('talk')
fig, ax = plt.subplots(1,2, figsize=(2*8,5),
                       sharex=True, sharey=True
)



sns.scatterplot(y = 'Housing share', x='Own interest rate', data=df["1992-01":"2001-12"],
                ax=ax[0], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='Own interest rate', data=df["1992-01":"2001-12"],
             ax=ax[0], sort=False, color = 'black')
ax[0].set_title("1992 (I) - 2001 (IV)")

sns.scatterplot(y = 'Housing share', x='Own interest rate', data=df["2001-12":"2009-07"],
                ax=ax[1], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='Own interest rate', data=df["2001-12":"2009-07"],
             ax=ax[1], sort=False, color = 'black')
ax[1].set_title("2001 (IV) - 2009 (II)")


sns.despine()
fig.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()

fig.savefig("./figs/Own_Cycle.png", transparent = True, dpi = 300)

fig, ax = plt.subplots()

df['H-GDP'].plot(color = 'black', label = 'Residential investment/GDP', ax = ax)
ax.axvspan(xmin = "1953-07", xmax='1954-04', color = "lightgray", label = 'Recession')
ax.axvspan(xmin = "1957-08", xmax='1958-05', color = "lightgray", label = '')
ax.axvspan(xmin = "1960-05", xmax='1961-02', color = "lightgray", label = '')
ax.axvspan(xmin = "1969-12", xmax='1970-11', color = "lightgray", label = '')
ax.axvspan(xmin = "1973-11", xmax='1975-03', color = "lightgray", label = '')
ax.axvspan(xmin = "1980-01", xmax='1980-07', color = "lightgray", label = '')
ax.axvspan(xmin = "1981-07", xmax='1982-01', color = "lightgray", label = '')
ax.axvspan(xmin = "1990-07", xmax='1991-03', color = "lightgray", label = '')
ax.axvspan(xmin = "2001-03", xmax='2001-11', color = "lightgray", label = '')
ax.axvspan(xmin = "2007-12", xmax='2009-07', color = "lightgray", label = '')
ax.legend()
sns.despine()
fig.savefig("./figs/housing_gdp.png", transparent = True, dpi = 300)
plt.show()

df = pd.read_csv(
    './data/OwnInterestRate_data.csv',
    index_col = [0],
    parse_dates = True
)

df = df.merge(
    pd.read_csv(
        './data/Cycle.csv',
        index_col = [0],
        parse_dates = True
    ),
    left_index=True, right_index=True
)

sns.set_context('talk')
fig, ax = plt.subplots(1,2, figsize=(2*8,5),
                       sharex=True, sharey=True
)



sns.scatterplot(x = 'Housing share', y='Durables', data=df["1992-01":"2001-12"],
                ax=ax[0], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(x = 'Housing share', y='Durables', data=df["1992-01":"2001-12"],
             ax=ax[0], sort=False, color = 'black')
ax[0].set_title("1992 (I) - 2001 (IV)")

sns.scatterplot(x = 'Housing share', y='Durables', data=df["2001-12":"2009-07"],
                ax=ax[1], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(x = 'Housing share', y='Durables', data=df["2001-12":"2009-07"],
             ax=ax[1], sort=False, color = 'black')
ax[1].set_title("2001 (IV) - 2009 (II)")


sns.despine()
fig.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()

fig.savefig("./figs/Durables.png", transparent = True, dpi = 300)

df = pd.read_csv(
    './data/Cycle.csv',
    index_col = [0],
    parse_dates = True
)
sns.set_context('talk')
fig, ax = plt.subplots(2,3, sharex=True, sharey=True, squeeze=False, figsize=(8*3,2*5))

sns.scatterplot(y = 'Housing share', x='TCU', data=df["1970-12":"1975-01"], ax=ax[0,0], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='TCU', data=df["1970-12":"1975-01"], ax=ax[0,0], sort=False, color = 'black')
ax[0,0].set_title("1970 (IV) - 1975 (I)")

sns.scatterplot(y = 'Housing share', x='TCU', data=df["1975-01":"1980-10"], ax=ax[0,1], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='TCU', data=df["1975-01":"1980-10"], ax=ax[0,1], sort=False, color = 'black')
ax[0,1].set_title("1977 (I) - 1980 (III)")

sns.scatterplot(y = 'Housing share', x='TCU', data=df["1980-10":"1982-12"], ax=ax[0,2], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='TCU', data=df["1980-10":"1982-12"], ax=ax[0,2], sort=False, color = 'black')
ax[0,2].set_title("1980 (III) - 1982 (IV)")

sns.scatterplot(y = 'Housing share', x='TCU', data=df["1982-12":"1991-01"], ax=ax[1,0], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='TCU', data=df["1982-12":"1991-01"], ax=ax[1,0], sort=False, color = 'black')
ax[1,0].set_title("1982 (IV) - 1991 (I)")

sns.scatterplot(y = 'Housing share', x='TCU', data=df["1991-01":"2001-12"], ax=ax[1,1], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='TCU', data=df["1991-01":"2001-12"], ax=ax[1,1], sort=False, color = 'black')
ax[1,1].set_title("1991 (I) - 2001 (IV)")

sns.scatterplot(y = 'Housing share', x='TCU', data=df["2001-12":"2009-07"], ax=ax[1,2], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='TCU', data=df["2001-12":"2009-07"], ax=ax[1,2], sort=False, color = 'black')
ax[1,2].set_title("2001 (IV) - 2009 (II)")


sns.despine()
ax[0,0].set_ylabel(""); ax[1,0].set_xlabel('')
ax[1,0].set_ylabel(""); ax[1,1].set_xlabel(''); ax[1,2].set_xlabel('')

fig.tight_layout(rect=[0, 0.03, 1, 0.90])
fig.text(0.5, 0.03, 'Capacity utilization ratio (Total Industry)', ha='center', fontsize =9)
fig.text(0, 0.5, 'Residential Investment/GDP', va='center', rotation='vertical', fontsize=9)
#fig.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()

fig.savefig("./figs/cycles.png", transparent = True, dpi = 300)

df = pd.read_csv(
    './data/OwnInterestRate_data.csv',
    index_col = [0],
    parse_dates = True
)

sns.set_context('paper')
fig, ax = plt.subplots(figsize=(8,5))

df[['Real mortgage interest rate', "Own interest rate", '$g_{I_h}$']].plot(ax=ax, lw=3, color = ("gray", "black", "darkgray"))

sns.despine()
plt.show()
salvar_grafico("Own_gI")

df = pd.read_excel(
    './data/SCF_merged.xlsx', 
    sheet_name='Riqueza',
    index_col=[0]
)

imoveis = df.loc['Imóveis',:]
imoveis = imoveis.drop(['Percentil da riqueza'], axis='columns')
imoveis.index = [.249, .499, .749, .899, 1]
imoveis = imoveis/100

acoes = df.loc['Ações',:]
acoes = acoes.drop(['Percentil da riqueza'], axis='columns')
acoes.index = [.249, .499, .749, .899, 1]
acoes = acoes/100

secund = df.loc['Secundário',:]
secund = secund.drop(['Percentil da riqueza'], axis='columns')
secund.index = [.249, .499, .749, .899, 1]
secund = secund/100

# Suavizando curvas. Não utilizado
def suavizacao(serie, n=1000, k=2):

    xnew = np.linspace(serie.min().min(), serie.max().max(), n) 
    suavizado = serie.apply(lambda x: make_interp_spline(x.index, x, k=k)(xnew))
    suavizado = suavizado[suavizado > 0].dropna()
    suavizado.index = suavizado.index/n
    return suavizado

import numpy as np
fig, ax = plt.subplots(figsize=(16, 10))

ax.plot(
    np.linspace(0,0), 
    np.linspace(0,0),
    color='white',
    ls='-',
    label='Primary\n'
)

imoveis.loc[:, imoveis.columns <= 2010].plot(
    ax=ax,
    cmap="Grays", 
    linewidth=2.5,
    ls = "--"
)

ax.plot(
    np.linspace(0,0), 
    np.linspace(0,0),
    color='white',
    ls='-',
    label='Secoundary\n'
)

secund.loc[:, secund.columns <= 2010].plot(
    ax=ax,
    cmap="Grays", 
    linewidth=2.5,
    ls=":"
)

ax.legend(ncol=2)

ax.plot(
    np.linspace(*ax.get_xlim()), 
    np.linspace(*ax.get_xlim()),
    color='black',
    ls='--',
)

ax.arrow(0.6, 0.6, +0.08, -0.08, head_width=0.01, head_length=0.01, fc='gray', ec='black')
ax.text(.61,.53, "Concentration", fontsize=12, rotation=-30)
ax.arrow(0.6, 0.6, -0.07, 0.07, head_width=0.01, head_length=0.01, fc='gray', ec='black')
ax.text(.54,.61, "Distribution", fontsize=12, rotation=-30)
ax.text(.8,.75, "Perfect equality line", fontsize=12, rotation=35)

ax.set_xlim(0,1)
ax.set_ylim(0,1)

ax.set_xlabel('Cumulative proportion of Households\n(Households without wealth omiited)')
ax.set_ylabel('Asset cumulative proportion\n(Primary and Secoundary houses)')
ax.secondary_yaxis('right')

plt.show()
salvar_grafico(file_name="Concentration_Curve")

start = dt(1947, 1, 1)
end = dt(2015, 1, 1)

df = web.DataReader(
    [
        'CMDEBT', # debt securities and loans; liability, Level 
        'CSUSHPINSA', # S&P/Case-Shiller U.S. National Home Price Index
    ], 
    'fred', 
    start, 
    end
)

df.columns = [
    'Household debt',
    'House prices',
]

for i in df.columns:
    df[i] = (df[i]/df[i]['2000-01-01'])*100

df.index.name = ''
df = df.resample("QS").mean().dropna()


fig, ax = plt.subplots(figsize=(16, 10))

df.iloc[df.index>='1970-01',:].plot(
    ax=ax,
    color=('darkred', 'darkblue'),
    linewidth=2.5,
)

crise_subprime(ax)
crises(ax)
ax.legend()


plt.show()
salvar_grafico(file_name="Debt_Prices")

from mpl_toolkits.mplot3d import Axes3D
import numpy as np

df = pd.read_csv(
    './data/OwnInterestRate_data.csv',
    index_col = [0],
    parse_dates = True
)

df = df.merge(
    pd.read_csv(
        './data/Cycle.csv',
        index_col = [0],
        parse_dates = True
    ),
    left_index=True, right_index=True
)


fig = plt.figure(
    figsize=(2*8,2*5)
)


ax = fig.add_subplot(1, 1, 1, projection='3d')
tmp_planes = ax.zaxis._PLANES 
ax.zaxis._PLANES = ( tmp_planes[2], tmp_planes[3], 
                     tmp_planes[0], tmp_planes[1], 
                     tmp_planes[4], tmp_planes[5])
view_1 = (25, -135)
view_2 = (25, -45)
init_view = view_1
ax.view_init(*init_view)


start = "1992-01"
end = "2001-12"
# Data for a three-dimensional line
zline = df[start:end]["Durables"]
xline = df[start:end]["Housing share"]
yline = df[start:end]["Own interest rate"]
ax.plot3D(xline, yline, zline, 'darkred', label='1992 (I) - 2001 (IV)', lw=4)
ax.scatter3D(xline, yline, zline, c=df[start:end].index, cmap='Reds', s=[i.timestamp()/10**7 for i in df[start:end].index]);

start = "2001-12"
end = "2005-09"
# Data for a three-dimensional line
zline = df[start:end]["Durables"]
xline = df[start:end]["Housing share"]
yline = df[start:end]["Own interest rate"]
ax.plot3D(xline, yline, zline, 'darkblue', label='2001 (IV) - 2005 (III)', lw=4)
ax.scatter3D(xline, yline, zline, c=df[start:end].index, cmap='Blues', s=[i.timestamp()/10**7 for i in df[start:end].index]);

start = "2005-09"
end = "2009-07"
# Data for a three-dimensional line
zline = df[start:end]["Durables"]
xline = df[start:end]["Housing share"]
yline = df[start:end]["Own interest rate"]
ax.plot3D(xline, yline, zline, 'darkgreen', label='2005 (III) - 2009 (III)',lw=4)
ax.scatter3D(xline, yline, zline, c=df[start:end].index,  cmap='Greens', s=[i.timestamp()/10**7 for i in df[start:end].index]);
#ax.plot(xline, yline, zs=.05, zdir='z', c='k', lw=2); ax.plot(xline, yline, zs=0.05, zdir='z', c='k', lw=2);
#ax.scatter(xline, yline, zs=.05, zdir='z', c=df[start:end].index,  cmap='Greys');


#ax.invert_xaxis()
ax.set_xlabel('\nResidential investment share', linespacing=2.5)
ax.set_ylabel('\nHouses Own interest rate', linespacing=2.5)
ax.zaxis.set_rotate_label(False)  # disable automatic rotation
ax.set_zlabel('Durables Consumption Share', linespacing=2.5,
              rotation=90,
              verticalalignment='baseline',
              horizontalalignment='left');
ax.legend()
sns.despine()

fig.tight_layout()
plt.show()

fig.savefig("./figs/Durables_3D.png", transparent = True, dpi = 300)

df = pd.read_csv(
    './data/OwnInterestRate_data.csv',
    index_col = [0],
    parse_dates = True
)

df = df.merge(
    pd.read_csv(
        './data/Cycle.csv',
        index_col = [0],
        parse_dates = True
    ),
    left_index=True, right_index=True
)

fig, ax = plt.subplots(1,3, sharex=True, sharey=True, squeeze=False, figsize=(3*8,5))
sns.scatterplot(y = 'Housing share', x='Own interest rate', data=df["1982-12":"1991-01"], ax=ax[0,0], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='Own interest rate', data=df["1982-12":"1991-01"], ax=ax[0,0], sort=False, color = 'black')
ax[0,0].set_title("1982 (IV) - 1991 (I)")

sns.scatterplot(y = 'Housing share', x='Own interest rate', data=df["1991-01":"2001-12"], ax=ax[0,1], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='Own interest rate', data=df["1991-01":"2001-12"], ax=ax[0,1], sort=False, color = 'black')
ax[0,1].set_title("1991 (I) - 2001 (IV)")

sns.scatterplot(y = 'Housing share', x='Own interest rate', data=df["2001-12":"2009-07"], ax=ax[0,2], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(y = 'Housing share', x='Own interest rate', data=df["2001-12":"2009-07"], ax=ax[0,2], sort=False, color = 'black')
ax[0,2].set_title("2001 (IV) - 2009 (II)")


sns.despine()
ax[0,0].set_xlabel(""); ax[0,1].set_xlabel(''); ax[0,2].set_xlabel('')
ax[0,0].set_ylabel(""); ax[0,1].set_ylabel(''); ax[0,2].set_ylabel('')

fig.text(0.5, 0.03, 'Houses own interest rate', ha='center', fontsize =9)
fig.text(0, 0.5, 'Residential Investment/GDP', va='center', rotation='vertical', fontsize=9)
fig.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()

fig.savefig("./figs/own_Ih.png", transparent = True, dpi = 300)

df = pd.read_csv(
    './data/OwnInterestRate_data.csv',
    index_col = [0],
    parse_dates = True
)

df = df.merge(
    pd.read_csv(
        './data/Cycle.csv',
        index_col = [0],
        parse_dates = True
    ),
    left_index=True, right_index=True
)

fig, ax = plt.subplots(1,3, sharex=True, sharey=True, squeeze=False, figsize=(3*8,5))
sns.scatterplot(x = 'Housing share', y='Durables', data=df["1982-12":"1991-01"], ax=ax[0,0], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(x = 'Housing share', y='Durables', data=df["1982-12":"1991-01"], ax=ax[0,0], sort=False, color = 'black')
ax[0,0].set_title("1982 (IV) - 1991 (I)")

sns.scatterplot(x = 'Housing share', y='Durables', data=df["1991-01":"2001-12"], ax=ax[0,1], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(x = 'Housing share', y='Durables', data=df["1991-01":"2001-12"], ax=ax[0,1], sort=False, color = 'black')
ax[0,1].set_title("1991 (I) - 2001 (IV)")

sns.scatterplot(x = 'Housing share', y='Durables', data=df["2001-12":"2009-07"], ax=ax[0,2], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(x = 'Housing share', y='Durables', data=df["2001-12":"2009-07"], ax=ax[0,2], sort=False, color = 'black')
ax[0,2].set_title("2001 (IV) - 2009 (II)")


sns.despine()
ax[0,0].set_xlabel(""); ax[0,1].set_xlabel(''); ax[0,2].set_xlabel('')
ax[0,0].set_ylabel(""); ax[0,1].set_ylabel(''); ax[0,2].set_ylabel('')

fig.text(0.0, 0.3, 'Durables Consumption/GDP', ha='center', fontsize =9, rotation='vertical')
fig.text(0.3, 0.03, 'Residential Investment/GDP', va='center', fontsize=9)
plt.show()

fig.savefig("./figs/Durables_Ih.png", transparent = True, dpi = 300)

df = pd.read_csv(
    './data/OwnInterestRate_data.csv',
    index_col = [0],
    parse_dates = True
)

df = df.merge(
    pd.read_csv(
        './data/Cycle.csv',
        index_col = [0],
        parse_dates = True
    ),
    left_index=True, right_index=True
)

fig, ax = plt.subplots(1,3, sharex=True, sharey=True, squeeze=False, figsize=(3*8,5))
sns.scatterplot(x = 'Own interest rate', y='Durables', data=df["1982-12":"1991-01"], ax=ax[0,0], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(x = 'Own interest rate', y='Durables', data=df["1982-12":"1991-01"], ax=ax[0,0], sort=False, color = 'black')
ax[0,0].set_title("1982 (IV) - 1991 (I)")

sns.scatterplot(x = 'Own interest rate', y='Durables', data=df["1991-01":"2001-12"], ax=ax[0,1], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(x = 'Own interest rate', y='Durables', data=df["1991-01":"2001-12"], ax=ax[0,1], sort=False, color = 'black')
ax[0,1].set_title("1991 (I) - 2001 (IV)")

sns.scatterplot(x = 'Own interest rate', y='Durables', data=df["2001-12":"2009-07"], ax=ax[0,2], size='Year', sizes = (5,100), color = 'black', legend=False)
sns.lineplot(x = 'Own interest rate', y='Durables', data=df["2001-12":"2009-07"], ax=ax[0,2], sort=False, color = 'black')
ax[0,2].set_title("2001 (IV) - 2009 (II)")


sns.despine()
ax[0,0].set_xlabel(""); ax[0,1].set_xlabel(''); ax[0,2].set_xlabel('')
ax[0,0].set_ylabel(""); ax[0,1].set_ylabel(''); ax[0,2].set_ylabel('')

fig.text(0.0, 0.3, 'Durables Consumption/GDP', ha='center', fontsize =9, rotation='vertical')
fig.text(0.3, 0.03, 'Houses own interest rate', va='center', fontsize=9)
plt.show()

fig.savefig("./figs/Durables_Own.png", transparent = True, dpi = 300)

df = pd.read_csv(
    './data/OwnInterestRate_data.csv',
    index_col = [0],
    parse_dates = True
)

df = df.merge(
    pd.read_csv(
        './data/Cycle.csv',
        index_col = [0],
        parse_dates = True
    ),
    left_index=True, right_index=True
)

df["$g_{DG}$"] = df["PCDG"].pct_change()
sns.set_context('talk')
fig, ax = plt.subplots(1,3, squeeze=False, figsize=(3*8,5))

df.loc["1982-12":"1991-01",["$g_{I_h}$", "Own interest rate", "$g_{DG}$"]].plot(ax=ax[0,0], title = "1982 (IV) - 1991 (I)")
df.loc["1991-01":"2001-12",["$g_{I_h}$", "Own interest rate", "$g_{DG}$"]].plot(ax=ax[0,1], title = "1991 (I) - 2001 (IV)")
df.loc["2001-12":"2009-07",["$g_{I_h}$", "Own interest rate", "$g_{DG}$"]].plot(ax=ax[0,2], title = "2001 (IV) - 2009 (II)")
sns.despine()
plt.show()

fig.savefig("./figs/Durables_Ih_own.png", transparent = True, dpi = 300)
