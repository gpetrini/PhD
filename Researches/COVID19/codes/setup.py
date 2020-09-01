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
corona_sp = '2020-03-24'
corona_sp_txt = "Início isolamento social em SP"

corona_60 = '2020-03-18'
corona_60_txt = "Mais de 60 casos de COVID-19"

base = "2014-12-01"


def interpolator(df):
    for col in df:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.resample('D').interpolate(method='time')

    return df

def line_format(label):
    """
    Convert time label to the format of pandas line plot
    """
    month = label.month_name()[:3]
    if month == 'Jan':
        month += f'\n{label.year}'
    return month

def rebase(df, base=base):
    for col in df:
        df[col] = df[col].apply(lambda x: (100*x)/df[col][base])
    return df
