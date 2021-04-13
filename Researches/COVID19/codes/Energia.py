%config InlineBackend.figure_format = 'retina'

import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter

import seaborn as sns
import pandas_datareader.data as web
import requests
import json

import country_converter as coco
cc = coco.CountryConverter()

import matplotlib.image as image

logo = "./figs/Cecon_Logo.png"
logo = image.imread(logo)

infos = {
    'Country' : [],
    'Type': [],
    'Usage': [],
    'Source': [],
    'Units' : [],
    'Frequency' : [],
    'Link' : []
        }


def get_energy_links(start=1577833200000, end=1590443159999,  path='../data/'):
    countries = [
        "AT", # Austria
        'DE', # Germany
    ]
    for country in countries:
        url = f"https://www.smard.de/en/downloadcenter/download_market_data/5730#!?downloadAttributes=%7B%22selectedCategory%22:1,%22selectedSubCategory%22:1,%22selectedRegion%22:%22{country}%22,%22from%22:{start},%22to%22:{end},%22selectedFileType%22:%22CSV%22%7D"
        url = url.replace('%22', '"').replace('%7B', '{').replace('%7D', '}')
        print(url)

def ploter(df, country, days=365, units="MWh"):
    fig, ax = plt.subplots(1,2, figsize=(8,5), dpi=300)
    df.plot(ax=ax[0], 
             ls='-', 
             title= f"Energy consumption for {country}\nTotal {units}",
             color='darkred'
            )
    df.pct_change(days).dropna().plot(ax=ax[1], 
             ls='-', 
             title= f"Energy consumption for {country}",
             color='darkred',
             label="Year over Year Growth rate"
            )
    df.pct_change(days).rolling(7).mean().dropna().plot(ax=ax[1], 
             ls='--', 
             label="1 Week Moving average",
             color='black'
            )
    ax[1].legend(labels=("YoY Growth rate", "1 Week Moving average"))
    ax[1].axhline(y=0, ls='--', color='black')
    
    ax2 = plt.axes([0.08,0.12,0.2,0.2])
    ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
    ax2.axis('off')
    ax3 = plt.axes([0.58,0.12,0.2,0.2])
    ax3.imshow(logo, aspect='auto', zorder=0, alpha=.5)
    ax3.axis('off')
    sns.despine()
    plt.tight_layout()
    plt.show()
    fig.savefig(
        f"./figs/Energia/DailyEnergyConsumption_{country}_{units}.svg", 
        dpi = 300, 
        bbox_inches='tight',pad_inches=0
    )
    return fig, ax

share = pd.read_excel(
    './raw/LCA/Consumo_Energia_EPE.xlsx',
    sheet_name='BR', 
    parse_dates=True,
    skiprows=11,
    usecols="A:F",
    index_col=[0],
)
#share = share[:-11] # Until March: Change here
share.index.name=''
share.index = pd.date_range(
    start = share.index[0],
    periods=share.shape[0],
    #end = share.index[-1],
    freq='M', 
)
share = share.apply(lambda x: x/share["TOTAL"]).drop(["TOTAL"], axis='columns')
share.columns = [
    "Comercial",
    "Residential",
    "Industrial",
    "Others"
]

fig, ax = plt.subplots(figsize=(8,5), dpi=300)

share["2019":].plot(
    ax=ax,
    kind='bar',
    stacked=True,
    edgecolor='black',
    lw=2
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
ax.set_xticklabels(map(lambda x: line_format(x), share["2019":].index))


sns.despine()
plt.show()
share["Non-Residential"] = 1- share["Residential"]

datelist = pd.date_range(
    start = "01/31/2018",
    end = str(dt.today().strftime("%m/%d/%Y")),
    freq='M',
).to_pydatetime().tolist()
datelist = [date.strftime("%Y_%m_%d") for date in datelist] #+ [str(dt.today().strftime("%Y_%m_%d"))]

bra = pd.DataFrame()

for date in datelist:
    url = f"http://sdro.ons.org.br/SDRO/DIARIO/{date}/HTML/07_DadosDiariosAcumulados_Regiao.html"
    bra = bra.append(pd.read_html(
        url,
        parse_dates=True,
        index_col = [0], skiprows=1, header=0, 
        thousands='.', #decimal=','
            )[0])
bra = bra[["Total"]] # TODO Check later: MWmed dia -> MW
bra.columns = ["BRA"]
bra.index = pd.date_range(
    start = bra.index[0],
    end = bra.index[-1],
    freq='D', 
)


energy_bra = bra.merge(share["2018":], left_index=True, right_index=True, how='left', ).fillna(method='ffill', ).fillna(method='bfill')
energy_bra["Daily Industrial"] = energy_bra["BRA"]*energy_bra["Industrial"]
energy_bra["Daily Non-Residential"] = energy_bra["BRA"]*energy_bra["Non-Residential"]
energy_bra["Daily Residential"] = energy_bra["BRA"]*energy_bra["Residential"]

country="Brazil"
units="MWmed"
days=365
fig, ax = plt.subplots(figsize=(8,5), dpi=300)
bra["2020":].plot(ax=ax, 
         ls='-', 
         title= f"Energy consumption for {country}\nTotal {units}",
         color='darkred'
        )
ax.axvline(x = '2020-03-18', color='black', ls='-', lw=1, label='More than 60 COVID19 cases')
ax.legend()
ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
sns.despine()
plt.show()
fig.savefig(
    f"./figs/Energia/DailyEnergyConsumption_{country}_{units}_level.svg", 
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
)


fig, ax = plt.subplots(figsize=(8,5), dpi=300)
bra.pct_change(days)["2020":].plot(ax=ax, 
         ls='-', 
         title= f"Energy consumption for {country}",
         color='red',
         label="Year over Year Growth rate",
         zorder=-1
        )
bra.pct_change(days).rolling(7).mean()["2020":].plot(ax=ax, 
         ls='--', 
         label="1 Week Moving average",
         color='black'
        )
ax.axvline(x = '2020-03-18', color='black', ls='-', lw=1.5, label='More than 60 COVID19 cases')
ax.axvline(x = '2020-03-24', color='gray', ls='-', lw=1.5, label='Beginning of social isolation in SP')
ax.legend(labels=("YoY Growth rate", "1 Week Moving average", 'More than 60 COVID19 cases'))
ax.axhline(y=0, ls='--', color='black')

ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
sns.despine()
plt.show()
fig.savefig(
    f"./figs/Energia/DailyEnergyConsumption_{country}_{units}_growth.svg", 
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
)

infos['Country'].append("BRA")
infos["Type"].append('Demand') # Consumption not available
infos['Usage'].append(np.nan)
infos['Source'].append('All')
infos['Units'].append("MWmed")
infos['Frequency'].append('Dailly')
infos['Link'].append(url)


country="Brazil"
units="MWmed"
days=365
fig, ax = plt.subplots(figsize=(8,5), dpi=300)
energy_bra[["Daily Industrial"]].rolling(7).mean()["2020":].plot(ax=ax, 
         ls='-', 
         title= f"Industrial Energy consumption for {country}\n1 Week Moving Average",
         color='red'
        )
#ax.axvline(x = '2020-03-18', color='black', ls='-', lw=1.5, label='More than 60 COVID19 cases')
ax.axvline(x = '2020-03-24', color='black', ls='-', lw=1.5, label='Beginning of social isolation in SP')
ax.legend()
ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
sns.despine()
plt.show()
fig.savefig(
    f"./figs/Energia/DailyEnergyConsumption_{country}_{units}_level_Industrialshares.svg", 
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
)


fig, ax = plt.subplots(figsize=(8,5), dpi=300)
# energy_bra[["Daily Industrial"]].pct_change(days)["2020":].plot(ax=ax, 
#          ls='-', 
#          title= f"Industrial Energy consumption for {country}",
#          color='red',
#          label="Year over Year Growth rate",
#          zorder=-1
#         )
energy_bra[["Daily Industrial"]].pct_change(days).rolling(7).mean()["2020":].plot(ax=ax, 
         ls='-', 
         label="1 Week Moving average",
         title= f"Industrial Energy consumption for {country}\nYoY growth rate",
         color='red'
        )
#ax.axvline(x = '2020-03-18', color='black', ls='-', lw=1.5, label='More than 60 COVID19 cases')
ax.axvline(x = '2020-03-24', color='black', ls='-', lw=1.5, label='Beginning of social isolation in SP')
ax.legend(labels=("YoY Growth rate\n1 Week Moving average", 'SP social isolation'))
ax.axhline(y=0, ls='-', color='black', lw=.7)

ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
sns.despine()
plt.show()
fig.savefig(
    f"./figs/Energia/DailyEnergyConsumption_{country}_{units}_growth_Industrialshares.svg", 
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
)


country="Brazil"
units="MWmed"
days=365
fig, ax = plt.subplots(figsize=(8,5), dpi=300)
energy_bra[["Daily Non-Residential"]].rolling(7).mean()["2020":].plot(ax=ax, 
         ls='-', 
         title= f"Consumo de energia não residencial\nMédia móvel de uma semana",
         color='red',
         label='Consumo diário'
        )
#ax.axvline(x = '2020-03-18', color='black', ls='-', lw=1.5, label='More than 60 COVID19 cases')
ax.axvline(x = '2020-03-24', color='black', ls='-', lw=1.5, label='Início do isolamento social em SP')
ax.legend(labels=("Consumo diário\nSemana Móvel", 'Início do Isolamento social em SP'))
ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
sns.despine()
plt.show()
fig.savefig(
    f"./figs/Energia/DailyEnergyConsumption_{country}_{units}_level_Non-Residentialshares.svg", 
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
)


fig, ax = plt.subplots(figsize=(8,5), dpi=300)
# energy_bra[["Daily Non-Residential"]].pct_change(days)["2020":].plot(ax=ax, 
#          ls='-', 
#          title= f"Non-Residential Energy consumption for {country}",
#          color='red',
#          label="Year over Year Growth rate",
#          zorder=-1
#         )
energy_bra[["Daily Non-Residential"]].pct_change(days).rolling(7).mean()["2020":].plot(ax=ax, 
         ls='-', 
         title= f"Consumo não-residencial de energia\nTaxa de Crescimento YoY (semana móvel)",
         label="1 Week Moving average",
         color='red'
        )
#ax.axvline(x = '2020-03-18', color='black', ls='-', lw=1.5, label='More than 60 COVID19 cases')
ax.axvline(x = '2020-03-24', color='black', ls='-', lw=1.5, label='Beginning of social isolation in SP')
ax.legend(labels=("Taxa de crescimento YoY\nSemana Móvel", 'Início do Isolamento social em SP'))
ax.axhline(y=0, ls='-', color='black', lw=.7)

ax2 = plt.axes([0.7,0.7,0.2,0.2])
ax2.imshow(logo, aspect='auto', zorder=0, alpha=.5)
ax2.axis('off')
sns.despine()
plt.show()
fig.savefig(
    f"./figs/Energia/DailyEnergyConsumption_{country}_{units}_growth_Non-Residentialshares.svg", 
    dpi = 300, 
    bbox_inches='tight',pad_inches=0
)

url = 'https://www.data.gouv.fr/en/datasets/r/cfc27ff9-1871-4ee8-be64-b9a290c06935'
fra = pd.read_csv(
    url,
    sep = ';',
    #'../data/Energy/FRA.csv',
    usecols=['Date - Heure', 'Date', 'Heure', 'Consommation brute totale (MW)'],
    index_col=['Date'], 
    parse_dates=True, dayfirst=True, # Check
    #thousands=',' # Check
)
fra = fra.sort_values(by='Date - Heure').drop('Date - Heure', axis='columns')
fra.reset_index(inplace=True)
fra = (fra.groupby(by='Date').mean())
fra = fra[['Consommation brute totale (MW)']]
fra = fra["2020":]#/1000 # Check later
fra = fra.dropna()
fra.columns = ["FRA"]
fra.index.name=''
fra.to_csv('./raw/Energy/FRA.csv')

ploter(
    df=fra, 
    country="France", 
    days = 7,
    units="MW"
)

infos['Country'].append("FRA")
infos["Type"].append('Consumption')
infos['Usage'].append(np.nan)
infos['Source'].append('All')
infos['Units'].append("MW")
infos['Frequency'].append('halfhour')
infos['Link'].append(url)

datelist = pd.date_range(
    start = "01/01/2020",
    end = str((dt.today()- timedelta(days=2)).strftime("%d/%m/%Y")),
    freq='D', 
).to_pydatetime().tolist()

spa = pd.DataFrame()
for day in datelist:
    #url = f'https://demanda.ree.es/visiona/peninsula/demanda/tablas/{day:%Y-%m-%d}/1'
    url = f"https://apidatos.ree.es/es/datos/demanda/demanda-tiempo-real?start_date={day:%Y-%m-%d}T00:00&end_date={(day + timedelta(days=2)):%Y-%m-%d}T01:00&time_trunc=hour"
    response=requests.request(url=url, method='get')
    data=response.json()
    value = pd.DataFrame(
    data['included'][0]['attributes']['values'],
        )
    value = value[['value']].rolling(6).sum()
    value = value[['value']].mean() # Unity: MW
    value = pd.DataFrame({
    'ESP': value,
    'Date': [day.strftime("%Y-%m-%d")]
    },)
    value['Date'] = pd.to_datetime(value['Date'])
    value = value.set_index('Date')
    value.index.name=''
    spa = spa.append(value)
spa.to_csv('./raw/Energy/ESP.csv')

ploter(
    df=spa, 
    country="Spain", 
    days = 7,
    units="MW"
)

infos['Country'].append("ESP")
infos["Type"].append('Consumption')
infos['Usage'].append(np.nan)
infos['Source'].append('All')
infos['Units'].append("MW")
infos['Frequency'].append('10 minutes')
infos['Link'].append(url)

aus = pd.read_csv(
    './raw/Energy/AUS.csv', 
    sep=';', 
    index_col=["Date", "Time of day"], 
    parse_dates=True, 
    thousands=',', decimal='.'
)
sources = ['Biomass[MWh]', 'Hydropower[MWh]', 
                       'Wind onshore[MWh]', 'Photovoltaics[MWh]',
                       'Other renewable[MWh]', 'Fossil hard coal[MWh]',
                       'Fossil gas[MWh]', 'Hydro pumped storage[MWh]',
                       'Other conventional[MWh]'
                      ]

#aus[sources] = aus[sources].apply(pd.to_numeric, errors='coerce') 
aus["Total[MWh]"] = aus["Total[MWh]"].str.replace(',', '')
aus["Total[MWh]"] = pd.to_numeric(aus["Total[MWh]"], errors='coerce')
aus["Total[MWh]"] = aus["Total[MWh]"]*(4) # TODO Check later: MWh -> MW
#aus["Total[MWh]"] = aus["Total[MWh]"].rolling(4).mean() # TODO Check later: MWhmed
aus = aus.groupby(by='Date', sort=False).mean()
aus = aus[["Total[MWh]"]]
aus.index.name = ''
aus.columns = ["AUS"]
df_ = aus.copy()

infos['Country'].append("AUS")
infos["Type"].append('Consumption')
infos['Usage'].append(np.nan)
infos['Source'].append("All")
infos['Units'].append("Total[MWh]")
infos['Frequency'].append('Quarterhour')
infos['Link'].append(np.NaN)

ploter(
    df=aus, 
    country="Austria", 
    days = 7,
    units="MWh"
)

ger = pd.read_csv(
    './raw/Energy/GER.csv', 
    sep=';', 
    index_col=["Date", "Time of day"], 
    parse_dates=True, 
    thousands=',', decimal='.', 
)
sources = ['Biomass[MWh]', 'Hydropower[MWh]', 
                       'Wind onshore[MWh]', 'Photovoltaics[MWh]',
                       'Other renewable[MWh]', 'Fossil hard coal[MWh]',
                       'Fossil gas[MWh]', 'Hydro pumped storage[MWh]',
                       'Other conventional[MWh]'
                      ]

#ger[sources] = ger[sources].apply(pd.to_numeric, errors='coerce') 
ger["Total[MWh]"] = ger["Total[MWh]"].str.replace(',', '')
ger["Total[MWh]"] = pd.to_numeric(ger["Total[MWh]"], errors='coerce')
ger["Total[MWh]"] = ger["Total[MWh]"]*(4) # TODO Check later: MWh -> MW
#ger["Total[MWh]"] = ger["Total[MWh]"].rolling(4).mean() # TODO Check later: MWhmed
ger = ger.groupby(by='Date', sort=False).mean()
ger = ger[["Total[MWh]"]]
ger.index.name = ''
ger.columns = ["GER"]

ploter(
    df=ger, 
    country="Germany", 
    days = 7,
    units="MWh"
)

infos['Country'].append("GER")
infos["Type"].append('Consumption')
infos['Usage'].append(np.nan)
infos['Source'].append("All")
infos['Units'].append("Total[MWh]")
infos['Frequency'].append('Quarterhour')
infos['Link'].append(np.NaN)

lux = pd.read_csv(
    './raw/Energy/LUX.csv', 
    sep=';', 
    index_col=["Date", "Time of day"],  
    thousands=',', decimal='.',
    parse_dates=True
)
lux["Total[MWh]"] = lux["Total[MWh]"].str.replace(',', '')
lux["Total[MWh]"] = pd.to_numeric(lux["Total[MWh]"], errors='coerce')
lux["Total[MWh]"] = lux["Total[MWh]"]*(4) # TODO Check later: MWh -> MW
#lux["Total[MWh]"] = lux["Total[MWh]"].rolling(4).mean() # TODO Check later: MWhmed
lux = lux.groupby(by='Date', sort=False).mean()
lux.index.name = ''
lux.columns = ["LUX"]

ploter(
    df=lux, 
    country="Luxembourg", 
    days = 7,
    units="MWh"
)

infos['Country'].append("LUX")
infos["Type"].append('Consumption') # Production not available
infos['Usage'].append(np.nan)
infos['Source'].append(np.nan)
infos['Units'].append("MWh")
infos['Frequency'].append('Quarterhour')
infos['Link'].append(np.NaN)
