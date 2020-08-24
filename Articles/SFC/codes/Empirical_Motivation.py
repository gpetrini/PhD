%config InlineBackend.figure_format = 'retina'

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader.data as web
import datetime

sns.set_context('paper')

start = datetime.datetime(1951, 12, 1)
end = datetime.datetime(2019, 3, 1)

def salvar_grafico(file_name, extension=".png", pasta="./figs/"):
    fig.savefig(pasta + file_name + extension, dpi = 300, bbox_inches = 'tight',
    pad_inches = 0.2, transparent = False,)

df = web.DataReader(
    [
        'GDP',
        'PRFI',
        'PNFI',
        'TCU'
    ], 
    'fred', 
    start, end
)
df['TCU'] = df['TCU']/100
df['H-GFI'] = df['PRFI']/df['PNFI']
df['H-GDP'] = df['PRFI']/df['GDP']
df['Investment share'] = df['PNFI']/df['GDP']
df['Housing share'] = df['PRFI']/df['GDP']
df['Year'] = df.index.year
df = df.resample('Q').last()
df.index.name = ''
df.to_csv('./data/Cycle.csv')
df.head()

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

fig, ax = plt.subplots(2,3, sharex=True, sharey=True, squeeze=False)

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
fig.tight_layout(rect=[0, 0.03, 1, 0.85])
plt.show()

fig.savefig("./figs/cycles.png", transparent = True, dpi = 300)

from datetime import datetime as dt
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
df.head()

sns.set_context('paper')
fig, ax = plt.subplots(figsize=(8,5))

df[['Real mortgage interest rate', "Own interest rate", '$g_{I_h}$']].plot(ax=ax, lw=3)

sns.despine()
plt.show()
salvar_grafico("Own_gI")
