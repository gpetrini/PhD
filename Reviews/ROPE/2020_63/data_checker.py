import pandas as pd
import numpy as np
from scipy.stats import kurtosis
import os

print(f"Your current path is {os.getcwd()}")
file_path = input("What is the file path? ")#'./Reviews/ROPE/2020_63/data.xlsx'# Change here according necesity

df = pd.read_excel(file_path,
                   parse_dates=True, index_col=[0],
                   skiprows=1)
df.index.name = ''

#'Checking for level variables'
print(df.describe()) # Does not match provided table 1


#Checking for growth variables (pct change from previous quarter)
print(df.pct_change().describe()*100) # Does not match provided table 1

#Checking for growth variables (pct change from same quarter of previous year)
print(df.pct_change(4).describe()*100) # Does not match provided table 1


print(f"Checking skewness (level)\n{df.skew()}")

print(f"Checking skewness (pct change)\n{df.pct_change().skew()}")

print(f"Checking skewness (pct change, same quarter from previous year)\n{df.pct_change(4).skew()}")

for var in df.columns:
    print("Checking Kurtosis (Level)")
    print(f"Kurtosis for {var} = {kurtosis(df[var])}\n")
    print("Checking Kurtosis (pct change)")
    print(f"Kurtosis for {var} = {kurtosis(df[var].pct_change().dropna())}\n")
    print("Checking Kurtosis (pct change from previous year)")
    print(f"Kurtosis for {var} = {kurtosis(df[var].pct_change(4).dropna())}\n")

print(df)


df = df.apply(lambda x: np.log(x))
#'Checking for level variables'
print(df.describe()) # MATCHES provided table 1


#Checking for growth variables (pct change from previous quarter)
print(df.pct_change().describe()*100) # Does not match provided table 1

#Checking for growth variables (pct change from same quarter of previous year)
print(df.pct_change(4).describe()*100) # Does not match provided table 1


print(f"Checking skewness (level)\n{df.skew()}")

print(f"Checking skewness (pct change)\n{df.pct_change().skew()}")

print(f"Checking skewness (pct change, same quarter from previous year)\n{df.pct_change(4).skew()}")

for var in df.columns:
    print("Checking Kurtosis (Level)")
    print(f"Kurtosis for {var} = {kurtosis(df[var])}\n")
    print("Checking Kurtosis (pct change)")
    print(f"Kurtosis for {var} = {kurtosis(df[var].pct_change().dropna())}\n")
    print("Checking Kurtosis (pct change from previous year)")
    print(f"Kurtosis for {var} = {kurtosis(df[var].pct_change(4).dropna())}\n")
