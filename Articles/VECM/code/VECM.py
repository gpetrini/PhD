from datetime import datetime as dt

t1 = dt.now()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import matplotlib.ticker as plticker

import pandas_datareader.data as web

from scipy.interpolate import make_interp_spline, BSpline  # Smooth plot


sns.set(style="whitegrid")
sns.set_context("paper")

plt.rc("axes", titlesize=22)  # fontsize of the axes title
plt.rcParams.update({"font.size": 15})
plt.rc("legend", fontsize=14)  # legend fontsize

def salvar_grafico(file_name, extension="png", pasta="./figs/"):
    fig.savefig(pasta + file_name + '.' + extension, dpi = 600, bbox_inches = 'tight', format=extension,
    pad_inches = 0.2, transparent = False,)

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
    "Residential Investment", 
    "House Prices", 
    "Interest rate",
    "Prices"
]
df.index.name = ""


df['Interest rate'] = df['Interest rate'].divide(100)
df = df.resample('M').last()

df['House Prices'] = df['House Prices']/df['House Prices'][0]
df = df.resample('Q').last()
df["Inflation"]= df["House Prices"].pct_change()
df["General inflation"] = df["Prices"].pct_change()
df["Own interest rate"] = ((1+df["Interest rate"])/(1+df["Inflation"])) -1
df["Real mortgages interest rate"] = ((1+df["Interest rate"])/(1+df["General inflation"])) -1

df['$g_{I_h}$'] = df["Residential Investment"].pct_change()

    
fig, ax = plt.subplots(figsize=(19.2,10.8))

df[['Real mortgages interest rate', "Own interest rate", '$g_{I_h}$']].plot(ax=ax, lw=3)

ax.tick_params(axis="both", which="major", labelsize=15)
sns.despine()
salvar_grafico("TxPropria_Investo") 
plt.close('all')

df = pd.read_csv("./data/Data_yeojohnson.csv", index_col=[0], parse_dates=True)

fig, ax = plt.subplots(figsize=(19.2,10.8), sharey=True)

df[[
    'Interest rate', 
    "Inflation", 
    "gIh", 
    "Own Interest rate"
]].plot(
    ax=ax, 
    subplots=True, layout=(2,2),
    #subplots=False, 
    lw = 3,
)

ax.tick_params(axis="both", which="major", labelsize=15)
plt.tight_layout()
sns.despine()

salvar_grafico("YeoJohnson_All")
plt.close('all')

df_autorizacao = pd.read_excel(
    "./data/construcao_autorizacao.xls", skiprows=11, index_col=[0], parse_dates=True
)
df_autorizacao.index.name = "Ano"
df_autorizacao.columns = [
    "Total",
    "Venda",
    "Contratado",
    "Proprietário",
    "Total (2 ou mais unidade)",
    "2 a 4",
    "5 a 9",
    "10 a 19",
    "20 ou mais",
]
df_autorizacao = df_autorizacao.apply(pd.to_numeric, errors="coerce")
numero_linhas = int((dt(2018, 1, 1) - dt(1976, 1, 1)).days / 365.25 + 1)
df_autorizacao = df_autorizacao.iloc[:numero_linhas, :]

df_start = pd.read_excel(
    "./data/construction.xls", skiprows=11, index_col=[0], parse_dates=True
)
df_start.index.name = "Ano"
df_start.columns = [
    "Total",
    "Venda",
    "Contratado",
    "Proprietário",
    "Total (2 ou mais unidade)",
    "2 a 4",
    "5 a 9",
    "10 a 19",
    "20 ou mais",
]
df_start = df_start.apply(pd.to_numeric, errors="coerce")
numero_linhas = int((dt(2018, 1, 1) - dt(1971, 1, 1)).days / 365.25 + 1)
df_start = df_start.iloc[:numero_linhas, :]
df = df_autorizacao + df_start
df = df.dropna()


fig, ax = plt.subplots(figsize=(19.2, 10.8))

sns.kdeplot(df["Total"], shade=True, color="darkred", ax=ax, label="Mean")
sns.kdeplot(df["Venda"], shade=True, color="darkgreen", ax=ax, label="For Sale")
sns.kdeplot(df["Contratado"], shade=True, color="orange", ax=ax, label="By contract")
sns.kdeplot(df["Proprietário"], shade=True, color="purple", ax=ax, label="By the owner")

# ax.xaxis.set_ticks(np.arange(0, 16, 3))
loc = plticker.MultipleLocator(base=3.0)  # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(loc)


ax.tick_params(axis="both", which="major", labelsize=15)
ax.set_xlabel("Months")
ax.set_ylabel("Probability density")

# ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.legend()

sns.despine()
plt.tight_layout()
salvar_grafico("Meses_construcao")
plt.close('all')

start = dt(1951, 12, 1)
end = dt(2019, 1, 1)
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

df.columns = [
    "GDP",
    "Residential investment",
    "Non-residential investment",
    "Capacity utilization",
    "Duráveis"
]

df['Capacity utilization'] = df['Capacity utilization']/100
df['Ih/GDP'] = df['Residential investment']/df['GDP']
df['If/GDP'] = df['Non-residential investment']/df['GDP']
df['Duráveis/GDP'] = df['Duráveis']/df['GDP']
df['Ano'] = df.index.year
df = df.resample('Q').last()
df['gY'] = df['GDP'].pct_change(4)

df.index.name = ''
df = df.dropna()

sns.set_context('talk')
fig, ax = plt.subplots(2,
                       3,
                       sharex=True,
                       sharey=True,
                       squeeze=False,
                       figsize=(19.2, 10.8))

sns.scatterplot(y='Ih/GDP',
                x='Capacity utilization',
                data=df["1970-12":"1975-01"],
                ax=ax[0, 0],
                size='Ano',
                sizes=(5, 300),
                color='black',
                legend=False)
sns.lineplot(y='Ih/GDP',
             x='Capacity utilization',
             data=df["1970-12":"1975-01"],
             ax=ax[0, 0],
             sort=False,
             color='black',
             lw=4,
            )
ax[0, 0].set_title("1970 (IV) - 1975 (I)", fontsize=18)

sns.scatterplot(y='Ih/GDP',
                x='Capacity utilization',
                data=df["1975-01":"1980-10"],
                ax=ax[0, 1],
                size='Ano',
                sizes=(5, 300),
                color='black',
                legend=False)
sns.lineplot(y='Ih/GDP',
             x='Capacity utilization',
             data=df["1975-01":"1980-10"],
             ax=ax[0, 1],
             sort=False,
             color='black',
             lw=4,)
ax[0, 1].set_title("1975 (I) - 1980 (III)", fontsize=18)

sns.scatterplot(y='Ih/GDP',
                x='Capacity utilization',
                data=df["1980-10":"1982-12"],
                ax=ax[0, 2],
                size='Ano',
                sizes=(5, 300),
                color='black',
                legend=False)
sns.lineplot(y='Ih/GDP',
             x='Capacity utilization',
             data=df["1980-10":"1982-12"],
             ax=ax[0, 2],
             sort=False,
             color='black',
             lw=4,)
ax[0, 2].set_title("1980 (III) - 1982 (IV)", fontsize=18)

sns.scatterplot(y='Ih/GDP',
                x='Capacity utilization',
                data=df["1982-12":"1991-01"],
                ax=ax[1, 0],
                size='Ano',
                sizes=(5, 300),
                color='black',
                legend=False)
sns.lineplot(y='Ih/GDP',
             x='Capacity utilization',
             data=df["1982-12":"1991-01"],
             ax=ax[1, 0],
             sort=False,
             color='black',
             lw=4,)
ax[1, 0].set_title("1982 (IV) - 1991 (I)")

sns.scatterplot(y='Ih/GDP',
                x='Capacity utilization',
                data=df["1991-01":"2001-12"],
                ax=ax[1, 1],
                size='Ano',
                sizes=(5, 300),
                color='black',
                legend=False)
sns.lineplot(y='Ih/GDP',
             x='Capacity utilization',
             data=df["1991-01":"2001-12"],
             ax=ax[1, 1],
             sort=False,
             color='black',
             lw=4,)
ax[1, 1].set_title("1991 (I) - 2001 (IV)", fontsize=18)

sns.scatterplot(y='Ih/GDP',
                x='Capacity utilization',
                data=df["2001-12":"2009-07"],
                ax=ax[1, 2],
                size='Ano',
                sizes=(5, 300),
                color='black',
                legend=False)
sns.lineplot(y='Ih/GDP',
             x='Capacity utilization',
             data=df["2001-12":"2009-07"],
             ax=ax[1, 2],
             sort=False,
             color='black',
             lw=4,)
ax[1, 2].set_title("2001 (IV) - 2009 (II)", fontsize=18)

sns.despine()
ax[0, 0].set_ylabel("")
ax[1, 0].set_xlabel('')
ax[1, 0].set_ylabel("")
ax[1, 1].set_xlabel('')
ax[1, 2].set_xlabel('')

fig.tight_layout(rect=[0, 0.03, 1, 0.90])
fig.text(0.5,
         0.03,
         'Capacity utilization (Total industry)',
         ha='center',
         fontsize=20)
fig.text(-0.01,
         0.5,
         'Residential investment/GDP',
         va='center',
         rotation='vertical',
         fontsize=20)
plt.suptitle(
    "(Markers sizes increases over time)"
)

salvar_grafico(file_name="Ciclo_Ih_u")
plt.close('all')

from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.api import SVAR
from statsmodels.tsa.vector_ar.vecm import coint_johansen, CointRankResults, VECM, select_coint_rank

from statsmodels.stats.diagnostic import acorr_breusch_godfrey, acorr_ljungbox, het_arch, het_breuschpagan, het_white
from statsmodels.tsa.stattools import adfuller, kpss, grangercausalitytests, q_stat, coint
from arch.unitroot import PhillipsPerron, ZivotAndrews, DFGLS, KPSS, ADF

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


import pandas_datareader.data as web
from scipy.stats import yeojohnson

start = dt(1987, 1, 1)
end = dt(2019, 7, 1)

df = web.DataReader(
    [
        "PRFI",
        "CSUSHPISA",
        "MORTGAGE30US",
    ], 
    'fred', 
    start, 
    end
)

df.columns = [
    "Residential Investment", 
    "House Prices", 
    "Interest rate",
]
df.index.name = ""

df['Interest rate'] = df['Interest rate'].divide(100)
df = df.resample('M').last()
df['House Prices'] = df['House Prices']/df['House Prices'][0]
df = df.resample('Q').last()

df["Inflation"] = df["House Prices"].pct_change() # Warning: 4
df['gIh'] = df["Residential Investment"].pct_change() # Warning: 4
df["Own Interest rate"] = ((1+df["Interest rate"])/(1+df["Inflation"])) -1

df['Own Interest rate'], *_ = yeojohnson(df['Own Interest rate'])
#df['Inflation'], *_ = yeojohnson(df['Inflation'])
df['gIh'], *_ = yeojohnson(df['gIh'])

df[["Inflation", "gIh", "Own Interest rate", "Interest rate"]].to_csv("./data/Complete_Data")

df["Crisis"] = [0 for i in range(len(df["gIh"]))]
for i in range(len(df["Crisis"])):
    if df.index[i] > dt(2007,12,1) and df.index[i] < dt(2009,7,1):
        df["Crisis"][i] = 1

df = df[["Interest rate", "Inflation", "gIh", "Crisis", "Own Interest rate"]]

df["d_Own Interest rate"] = df["Own Interest rate"].diff()
df["d_gIh"] = df["gIh"].diff()
df["d_Inflation"] = df["Inflation"].diff()
df["d_Interest rate"] = df['Interest rate'].diff()
df = df.dropna()

def testes_raiz(df=df["gIh"], original_trend='c', diff_trend='c'):
    """
    serie: Nome da coluna do df
    orignal_trend: 'c', 'ct', 'ctt'
    diff_trend: 'c', 'ct', 'ctt'
    
    Plota série o original e em diferenta e retorna testes de raíz unitária
    """
    fig, ax = plt.subplots(1,2)

    df.plot(ax=ax[0], title='Original series')
    df.diff().plot(ax=ax[1], title='First differences')

    plt.tight_layout()
    sns.despine()
    plt.close('all')
    
    fig, ax = plt.subplots(2,2)
    
    plot_acf(df, ax=ax[0,0], title='ACF: serie original') 
    plot_pacf(df, ax=ax[0,1], title='PACF: serie original')
    
    plot_acf(df.diff().dropna(), ax=ax[1,0], title='ACF: serie em diferença') 
    plot_pacf(df.diff().dropna(), ax=ax[1,1], title='PACF: serie em diferença')
    
    plt.tight_layout()
    sns.despine() 
    plt.close('all')

    
    # Zivot Andrews
    print('\nZIVOT ANDREWS level series')
    print(ZivotAndrews(df, trend = original_trend).summary(),"\n")
    print('\nZIVOT ANDREWS First differences')
    print(ZivotAndrews(df.diff().dropna(), trend = diff_trend).summary(),"\n")
    
    print('\nADF level series')
    print(ADF(df, trend=original_trend).summary(),"\n")
    print('\nADF First differences')
    print(ADF(df.diff().dropna(), trend=diff_trend).summary(),"\n")
    
    print('\nDFGLS level series')
    print(DFGLS(df, trend=original_trend).summary(),"\n")
    print('\nDFGLS First differences')
    print(DFGLS(df.diff().dropna(), trend=diff_trend).summary(),"\n")
    
    print('\nKPSS em nível')
    print(KPSS(df, trend = original_trend).summary(),"\n")
    print('\nKPSS em primeira diferença')
    print(KPSS(df.diff().dropna(), trend = diff_trend).summary(),"\n")
    
    print('\nPhillips Perron em nível')
    print(PhillipsPerron(df, trend=original_trend).summary(),"\n")
    print('\nPhillips Perron em primeira diferença')
    print(PhillipsPerron(df.diff().dropna(), trend=diff_trend).summary(),"\n")

# Teste de cointegração

def cointegracao(ts0, ts1, signif = 0.05, lag=1):
  trends = ['nc', 'c', 'ct', 'ctt']
  for trend in trends:
    print(f"\nTestando para lag = {lag} e trend = {trend}")
    result = coint(ts0, ts1, trend = trend, maxlag=lag)
    print('Null Hypothesis: there is NO cointegration')
    print('Alternative Hypothesis: there IS cointegration')
    print('t Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    if result[1] < signif:
      print('CONCLUSION: REJECT null Hypothesis: there IS cointegration\n')
    else:
      print('CONCLUSION: FAIL to reject Null Hypothesis: there is NO cointegration\n')
    
def testes_coint(series, maxlag=6, signif = 0.05,):
    for i in range(1, maxlag):
        print(50*'=')
        cointegracao(
            ts0=series.iloc[:, 0],
            ts1=series.iloc[:, 1:],
            signif=signif,
            lag=i
        )
        print("\nTESTE DE JOHANSEN\n")
        print("Teste SEM constante")
        result = select_coint_rank(endog=series, k_ar_diff=i, det_order=-1, signif=signif) ## Warning: 1
        print(result.summary())
        print(f'Para lag = {i} e significância = {signif*100}%, Rank = {result.rank}')
        print("\nTeste COM constante\n")
        result = select_coint_rank(endog=series, k_ar_diff=i, det_order=0, signif=signif) ## Warning: 1
        print(result.summary())
        print(f'Para lag = {i} e significância = {signif*100}%, Rank = {result.rank}')
        print("\nTeste COM constante E tendência\n")
        result = select_coint_rank(endog=series, k_ar_diff=i, det_order=1, signif=signif) ## Warning: 1
        print(result.summary())
        print(f'Para lag = {i} e significância = {signif*100}%, Rank = {result.rank}')
        print(10*'=')

### Resíduos

def LjungBox_Pierce(resid, signif = 0.05, boxpierce = False, k = 4):
  """
  resid = residuals df
  signif = signif. level
  """
  var = len(resid.columns)
  print("H0: autocorrelations up to lag k equal zero")
  print('H1: autocorrelations up to lag k not zero')
  print("Box-Pierce: ", boxpierce)
  
  for i in range(var):
    print("Testing for ", resid.columns[i].upper(), ". Considering a significance level of",  signif*100,"%")
    result = acorr_ljungbox(x = resid.iloc[:,i-1], lags = k, boxpierce = boxpierce)[i-1]
    conclusion = result < signif
    for j in range(k):
      print(f'p-value = {result[j]}')
      print("Reject H0 on lag " ,j+1,"? ", conclusion[j], "\n")
    print("\n")
    
def ARCH_LM(resid, signif = 0.05, autolag = 'bic'):
  """
  df = residuals df
  signif = signif. level
  """
  var = len(resid.columns)
  print("H0: Residuals are homoscedastic")
  print('H1: Residuals are heteroskedastic')
  
  for i in range(var):
    print("Testing for ", resid.columns[i].upper())
    result = het_arch(resid = resid.iloc[:,i], autolag = autolag)
    print('LM statistic: ', result[0])
    print('LM p-value: ', result[1])
    print("Reject H0? ", result[1] < signif)
    print('F statistic: ', result[2])
    print('F p-value: ', result[3])
    print("Reject H0? ", result[3] < signif)
    print('\n')
    

def analise_residuos(results, nmax=15):
    
    residuals = pd.DataFrame(results.resid, columns = results.names)
    
    residuals.plot()
    sns.despine()
    
    plt.close('all')
    
    for serie in residuals.columns:
        sns.set_context('talk')
        fig, ax = plt.subplots(1,2, figsize=(10,8))

        plot_acf(residuals[serie], ax=ax[0], title=f'ACF Resíduo de {serie}', zero=False) 
        plot_pacf(residuals[serie], ax=ax[1], title=f'PACF Resíduo de {serie}', zero=False)
        
        plt.tight_layout()
        sns.despine() 
        
        plt.close('all')

    print('AUTOCORRELAÇÃO RESIDUAL: PORTMANTEAU\n')
    print(results.test_whiteness(nlags=nmax).summary())
    print('\nAUTOCORRELAÇÃO RESIDUAL: PORTMANTEAU AJUSTADO\n')
    print(results.test_whiteness(nlags=nmax, adjusted=True).summary())
    print('\nLJUNGBOX\n')
    LjungBox_Pierce(residuals, k = 12, boxpierce=False)
    print('\nBOXPIERCE\n')
    LjungBox_Pierce(residuals, k = 12, boxpierce=True)
    print('\nNORMALIDADE\n')
    print(results.test_normality().summary())
    print('\nHOMOCEDASTICIDADE\n')
    ARCH_LM(residuals)
    
    return residuals
results = []
def plot_lags(results = results, trimestres=[2, 5]):
    series = results.names
    sns.set_context('talk')
    fig, ax = plt.subplots(len(trimestres),2, figsize = (16,10))
    
    for i in range(len(trimestres)):
        sns.regplot(y = df[series[0]], x = df[series[1]].shift(-trimestres[i]), color = 'black', ax = ax[i,0], order = 2)
        ax[i,0].set_xlabel(f'{series[1]} lagged in {trimestres[i]} quarters')

        sns.regplot(x = df[series[0]].shift(-trimestres[i]), y = df[series[1]], color = 'black', ax = ax[i,1], order = 2)
        ax[i,1].set_xlabel(f'{series[0]} lagged in {trimestres[i]} quarters')
        
    plt.tight_layout()
    plt.close('all')
    
    return fig

from statsmodels.compat.python import lrange, iteritems
from statsmodels.tsa.vector_ar import output, plotting, util
def fmse(self, steps):
        r"""
        Compute theoretical forecast error variance matrices

        Parameters
        ----------
        steps : int
            Number of steps ahead

        Notes
        -----
        .. math:: \mathrm{MSE}(h) = \sum_{i=0}^{h-1} \Phi \Sigma_u \Phi^T

        Returns
        -------
        forc_covs : ndarray (steps x neqs x neqs)
        """
        ma_coefs = self.ma_rep(steps)

        k = len(self.sigma_u)
        forc_covs = np.zeros((steps, k, k))

        prior = np.zeros((k, k))
        for h in range(steps):
            # Sigma(h) = Sigma(h-1) + Phi Sig_u Phi'
            phi = ma_coefs[h]
            var = phi @ self.sigma_u @ phi.T
            forc_covs[h] = prior = prior + var

        return forc_covs

class FEVD(object):
    """
    Compute and plot Forecast error variance decomposition and asymptotic
    standard errors
    """
    def __init__(self, model, P=None, periods=None):

        self.periods = periods

        self.model = model
        self.neqs = model.neqs
        self.names = model.model.endog_names

        self.irfobj = model.irf(periods=periods)
        self.orth_irfs = self.irfobj.orth_irfs

        # cumulative impulse responses
        irfs = (self.orth_irfs[:periods] ** 2).cumsum(axis=0)

        rng = lrange(self.neqs)
        mse = fmse(self.model, periods)[:, rng, rng]

        # lag x equation x component
        fevd = np.empty_like(irfs)

        for i in range(periods):
            fevd[i] = (irfs[i].T / mse[i]).T

        # switch to equation x lag x component
        self.decomp = fevd.swapaxes(0, 1)

    def summary(self):
        buf = StringIO()

        rng = lrange(self.periods)
        for i in range(self.neqs):
            ppm = output.pprint_matrix(self.decomp[i], rng, self.names)

            buf.write('FEVD for %s\n' % self.names[i])
            buf.write(ppm + '\n')

        print(buf.getvalue())


    def plot(self, periods=None, figsize=(10, 10), **plot_kwds):
        """Plot graphical display of FEVD

        Parameters
        ----------
        periods : int, default None
            Defaults to number originally specified. Can be at most that number
        """
        import matplotlib.pyplot as plt

        k = self.neqs
        periods = periods or self.periods

        fig, axes = plt.subplots(nrows=k, figsize=figsize)

        #fig.suptitle('Forecast error variance decomposition (FEVD)')

        colors = ["black", "lightgray"]
        ticks = np.arange(periods)

        limits = self.decomp.cumsum(2)

        for i in range(k):
            ax = axes[i]

            this_limits = limits[i].T

            handles = []

            for j in range(k):
                lower = this_limits[j - 1] if j > 0 else 0
                upper = this_limits[j]
                handle = ax.bar(ticks, upper - lower, bottom=lower,
                                color=colors[j], label=self.names[j],
                                **plot_kwds)

                handles.append(handle)
            ax.axhline(y=0.5, color = 'red', ls = '--', lw=3)
            
            ax.set_title(self.names[i])

        # just use the last axis to get handles for plotting
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')
        plotting.adjust_subplots(right=0.85)
        sns.despine()
        return fig

df = df["1992-01-01":]
df[["Inflation", "gIh", "Own Interest rate", "Interest rate"]].to_csv(
    "../data/Data_yeojohnson.csv"
)


df[["Inflation", "gIh", "Own Interest rate", "Interest rate"]].to_csv(
    "../data/Data_yeojohnson_ascii.csv",
    encoding="ascii",
    header=[
        "infla",
        "gIh",
        "Own",
        "Interest rate",
    ],
)
df = df.dropna()

testes_raiz(df=df['gIh'])

testes_raiz(df['Own Interest rate'])

testes_raiz(df['Inflation'])

testes_raiz(df['Interest rate'], original_trend='ct')

print("VAR Order\n")

model = VAR(
    df[["gIh", 'Own Interest rate']])
print(model.select_order(maxlags=15, trend='ct').summary())

testes_coint(series=df[['gIh', 'Own Interest rate']], maxlag=9)

testes_coint(series=df[['gIh', 'Inflation']])

from statsmodels.tsa.vector_ar.vecm import select_order

#det = 'cili'
#det = 'coli'
#det = 'colo'
det = 'cilo'
#det = 'ci'
#det = 'nc'
#det= 'co'

order_vec = select_order(
    df[[
        #"Inflation", 
        "Own Interest rate", 
        "gIh"
    ]], 
    #exog=df[["Interest rate"]],
    #seasons=4,
    maxlags=15, deterministic=det)
order_sel = order_vec.summary().as_latex_tabular(tile = "Selação ordem do VECM") 
with open('./tabs/VECM_lag_order.tex','w') as fh:
    fh.write(order_sel)

print(order_sel)

model = VECM(
    endog = df[[
        #"Inflation", 
        "Own Interest rate", 
        "gIh"
    ]], 
    #exog=df[["Interest rate"]],
    #k_ar_diff=0,
    #k_ar_diff=1,
    #k_ar_diff=2,
    #k_ar_diff=3,
    k_ar_diff=4,
    #k_ar_diff=5,
    #k_ar_diff=6,
    #k_ar_diff=7,
    #k_ar_diff=8,
    deterministic=det, 
    #seasons=4,
)
results = model.fit()
adjust = results.summary().as_latex() 
with open('./tabs/VECM_ajuste.tex','w') as fh:
    fh.write(adjust)

print(adjust)

p = results.irf(20).plot(orth=True)
p.suptitle("")
sns.despine()


p.savefig("./figs/Impulse_VECMOrth.png", dpi = 300, bbox_inches = 'tight',
    pad_inches = 0.0, transparent = False,)
plt.close('all')

p = results.irf(20).plot(orth=False)
p.suptitle("")
sns.despine()


p.savefig("./figs/Impulse_VECM.png", dpi = 300, bbox_inches = 'tight',
    pad_inches = 0.0, transparent = False,)
plt.close('all')

fig = FEVD(results, periods=21).plot()
fig.savefig("./figs/FEVD_VECMpython_TxPropria.png", dpi = 300, bbox_inches = 'tight',
    pad_inches = 0.2, transparent = False,)
plt.close('all')

series = residuals.columns
print(results.test_granger_causality(causing=series[0], caused=series[1]).summary())
print(results.test_inst_causality(causing=series[0]).summary())

residuals = analise_residuos(results=results)

series = results.names
for serie in series:
    sns.scatterplot(x = residuals[serie], y = residuals[serie]**2)
    plt.ylabel(f"{serie}^2")
    sns.despine()
    
    plt.close('all')
    sns.scatterplot(
    y = residuals[serie], 
    x = residuals[serie].shift(-1), 
    color = 'darkred' 
    )
    sns.despine()
    plt.xlabel(f"{serie}(-1)")
    
    plt.close('all')

plt.tight_layout()
g.savefig("./figs/Residuals_4VECM.png", dpi = 300, bbox_inches = 'tight',
    pad_inches = 0.2, transparent = False,)
plt.close(g)

series = results.names
ax = sns.jointplot(
    x = series[0], 
    y = series[1], 
    data = residuals, color = 'darkred', kind="reg", 
)
plt.close('all')

fig = plot_lags(results=results, trimestres=[1,4])
fig.savefig("./figs/VEC_Defasagens.png", dpi = 300, bbox_inches = 'tight',
    pad_inches = 0.2, transparent = False,)
plt.close(fig)

testes_raiz(residuals['gIh'])

testes_raiz(residuals['Own Interest rate'])

model = VAR(
    df[["d_Own Interest rate", 'd_gIh']],
)
print(model.select_order(maxlags=15, trend='ct').summary())

results = model.fit(maxlags=4)
print(results.summary())

p = results.irf(20).plot(orth=True)
sns.despine()

p.savefig("./figs/Impulse_VAROrth.png", dpi = 300, bbox_inches = 'tight',
    pad_inches = 0.0, transparent = False,)

plt.close('all')

p = results.irf(20).plot(orth=False)
p.suptitle("")
sns.despine()


p.savefig("./figs/Impulse_VAR.png", dpi = 300, bbox_inches = 'tight',
    pad_inches = 0.0, transparent = False,)
plt.close('all')

p = results.irf(20).plot_cum_effects(orth=True)
sns.despine()
p.savefig("./figs/Impulse_Cum.png", dpi = 300)

p = results.fevd(20).plot()
sns.despine()
p.savefig("./figs/FEVD_VAR.png", dpi = 300)

series = residuals.columns
print(results.test_causality(causing = series[0], caused=series[1]).summary())
print(results.test_causality(causing = series[1], caused=series[0]).summary())

results.plot_acorr(nlags = 20)
sns.despine()
plt.show()
plt.close()

print("Estável:", results.is_stable(verbose=True))

residuals = analise_residuos(results=results)

series = results.names
sns.set_context('talk')
ax = sns.jointplot(
    x = series[0], 
    y = series[1], 
    data = residuals, color = 'darkred', kind="reg", 
)
plt.show()
plt.close('all')

g = sns.PairGrid(residuals, diag_sharey=False, height = 5, aspect=(8/5))
g.map_lower(sns.kdeplot, color = 'darkred')
g.map_upper(sns.scatterplot, color = 'darkred')
g.map_diag(sns.kdeplot, lw=3, color = 'darkred')
g.savefig("./figs/Residuals_4VAR.png", dpi = 600, )
plt.close('all')

series = results.names
for serie in series:
    sns.scatterplot(x = residuals[serie], y = residuals[serie]**2)
    sns.despine()
    
    sns.scatterplot(
    y = residuals[serie], 
    x = residuals[serie].shift(-1), 
    color = 'darkred' 
    )
    sns.despine()
    plt.xlabel(f"{serie}(-1)")

plt.close('all')

plot_lags(results=results)

testes_raiz(residuals['d_gIh'])

testes_raiz(residuals['d_Own Interest rate'])
