import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

cols = ["Ativo", 'Nome', 'Situação|CVM', 'Data do Bal', 'Setor NAICS|ult disponiv', 'Receita| Em moeda orig| em milhares| no exercício| consolid:sim*', 'Lucro Bruto| Em moeda orig| em milhares| no exercício| consolid:sim*', 'EBIT| Em moeda orig| em milhares| no exercício| consolid:sim*', 'Lucro Liquido| Em moeda orig| em milhares| no exercício| consolid:sim*', 'Capex| Em moeda orig| em milhares| de 12 meses| consolid:sim*', 'Invest Cap $| Em moeda orig| em milhares| consolid:sim*', 'Patrim Liq| Em moeda orig| em milhares| consolid:sim*', 'Ativo Tot| Em moeda orig| em milhares| consolid:sim*', 'Div Tt Bruta| Em moeda orig| em milhares| consolid:sim*', 'AlaFin| de 12 meses| consolid:sim*', 'CapGir| Em moeda orig| em milhares| consolid:sim*', 'RecFin| Em moeda orig| em milhares| no exercício| consolid:sim*', 'Estoques| Em moeda orig| em milhares| consolid:sim*', 'Ano'
]

primeiroPeriodo = ['1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002']

basePrimeiroPeriodo = pd.concat(pd.read_excel(r"C:\Users\fechi\OneDrive\Documentos\Felipe M Barros\Graduação\Monografia\Bases de Dados\Periodo\setorEnergiaSeparado.xlsx", na_values='-', sheet_name= primeiroPeriodo, usecols=cols), ignore_index=True).dropna()

basePrimeiroPeriodo['Ano'] = basePrimeiroPeriodo['Ano'].apply(str)

basePrimeiroPeriodo['Nome_Ano'] = basePrimeiroPeriodo['Nome'] + basePrimeiroPeriodo['Ano']

basePrimeiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*'].quantile([0.25,0.5,0.75])

grande1 = []
for row in basePrimeiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']:
    if row > 6393536.5: grande1.append('Grande')
    elif row < 6393536.5: grande1.append('Pequena')

basePrimeiroPeriodo['Tamanho'] = grande1

basePrimeiroPeriodo['Capex%Ativo'] = basePrimeiroPeriodo['Capex| Em moeda orig| em milhares| de 12 meses| consolid:sim*'] / basePrimeiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
basePrimeiroPeriodo['LL%Ativo'] = basePrimeiroPeriodo['Lucro Liquido| Em moeda orig| em milhares| no exercício| consolid:sim*'] / basePrimeiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
basePrimeiroPeriodo['A. Financ.%Ativo'] = basePrimeiroPeriodo['AplFin| Em moeda orig| em milhares| consolid:sim*'] / basePrimeiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
basePrimeiroPeriodo['Fluxo Cx%Ativo'] = basePrimeiroPeriodo['CxGerOp| Em moeda orig| em milhares| no exercício| consolid:sim*'] / basePrimeiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
basePrimeiroPeriodo['Pgto. Div.%Ativo'] = basePrimeiroPeriodo['DivPag| Em moeda orig| em milhares| no exercício| consolid:sim*'] / basePrimeiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']

########################################################################################################################

segundoPeriodo = ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011']

baseSegundoPeriodo = pd.concat(pd.read_excel(r"C:\Users\fechi\OneDrive\Documentos\Felipe M Barros\Graduação\Monografia\Bases de Dados\Periodo\setorEnergiaSeparado.xlsx", na_values='-', sheet_name= segundoPeriodo, usecols=cols), ignore_index=True).dropna()

baseSegundoPeriodo['Ano'] = baseSegundoPeriodo['Ano'].apply(str)

baseSegundoPeriodo['Nome_Ano'] = baseSegundoPeriodo['Nome'] + baseSegundoPeriodo['Ano']

baseSegundoPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*'].quantile([0.25,0.5,0.75])

grande2 = []
for row in baseSegundoPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']:
    if row > 8990961.00: grande2.append('Grande')
    elif row < 8990961.00: grande2.append('Pequena')

baseSegundoPeriodo['Tamanho'] = grande2

baseSegundoPeriodo['Capex%Ativo'] = baseSegundoPeriodo['Capex| Em moeda orig| em milhares| de 12 meses| consolid:sim*'] / baseSegundoPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
baseSegundoPeriodo['LL%Ativo'] = baseSegundoPeriodo['Lucro Liquido| Em moeda orig| em milhares| no exercício| consolid:sim*'] / baseSegundoPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
baseSegundoPeriodo['A. Financ.%Ativo'] = baseSegundoPeriodo['AplFin| Em moeda orig| em milhares| consolid:sim*'] / baseSegundoPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
baseSegundoPeriodo['Fluxo Cx%Ativo'] = baseSegundoPeriodo['CxGerOp| Em moeda orig| em milhares| no exercício| consolid:sim*'] / baseSegundoPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
baseSegundoPeriodo['Pgto. Div.%Ativo'] = baseSegundoPeriodo['DivPag| Em moeda orig| em milhares| no exercício| consolid:sim*'] / baseSegundoPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']

########################################################################################################################


terceiroPeriodo = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

baseTerceiroPeriodo = pd.concat(pd.read_excel(r"C:\Users\fechi\OneDrive\Documentos\Felipe M Barros\Graduação\Monografia\Bases de Dados\Periodo\setorEnergiaSeparado.xlsx", na_values='-', sheet_name= terceiroPeriodo), ignore_index=True).dropna()

baseTerceiroPeriodo['Ano'] = baseTerceiroPeriodo['Ano'].apply(str)

baseTerceiroPeriodo['Nome_Ano'] = baseTerceiroPeriodo['Nome'] + baseTerceiroPeriodo['Ano']

baseTerceiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*'].quantile([0.25,0.5,0.75])

grande3 = []
for row in baseTerceiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']:
    if row > 14422229.00: grande3.append('Grande')
    elif row < 14422229.00: grande3.append('Pequena')

baseTerceiroPeriodo['Tamanho'] = grande3

baseTerceiroPeriodo['Capex%Ativo'] = baseTerceiroPeriodo['Capex| Em moeda orig| em milhares| de 12 meses| consolid:sim*'] / baseTerceiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
baseTerceiroPeriodo['LL%Ativo'] = baseTerceiroPeriodo['Lucro Liquido| Em moeda orig| em milhares| no exercício| consolid:sim*'] / baseTerceiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
baseTerceiroPeriodo['A. Financ.%Ativo'] = baseTerceiroPeriodo['AplFin| Em moeda orig| em milhares| consolid:sim*'] / baseTerceiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
baseTerceiroPeriodo['Fluxo Cx%Ativo'] = baseTerceiroPeriodo['CxGerOp| Em moeda orig| em milhares| no exercício| consolid:sim*'] / baseTerceiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']
baseTerceiroPeriodo['Pgto. Div.%Ativo'] = baseTerceiroPeriodo['DivPag| Em moeda orig| em milhares| no exercício| consolid:sim*'] / baseTerceiroPeriodo['Ativo Tot| Em moeda orig| em milhares| consolid:sim*']

basePrimeiroPeriodo.to_csv(r'C:\Users\fechi\OneDrive\Documentos\Felipe M Barros\Graduação\Monografia\Bases de Dados\Periodo\CSVs\1995a2002.csv')
baseSegundoPeriodo.to_csv(r'C:\Users\fechi\OneDrive\Documentos\Felipe M Barros\Graduação\Monografia\Bases de Dados\Periodo\CSVs\2003a2011.csv')
baseTerceiroPeriodo.to_csv(r'C:\Users\fechi\OneDrive\Documentos\Felipe M Barros\Graduação\Monografia\Bases de Dados\Periodo\CSVs\2012a2020.csv')