#CÓDIGO MONOGRAFIA

install.packages("lmtest") 
install.packages('tseries') 
install.packages('FinTS')
install.packages("urca") 
install.packages("TTR")
install.packages("pillar")
install.packages("vars")
install.packages("lattice")

#Carregando pacotes
library(lmtest)
require(tseries)
require(stats)
library(FinTS)
library(urca)
library(TTR)
library(vars)
library(lattice)

#############leitura dos dados
####Gastos Autônomos
gastos_usa=ts(PIB_Trimestre_Anterior[,2], start=c(1993,1), freq=1)
plot(gastos_usa,main='Gastos Autônomos',ylab='Z',xlab='Trim/Ano',col='blue')
show(gastos_usa)

acf(gastos_usa)
Acf(gastos_usa) #Valores diferentes de 0, declinio suave que pode indicar não estacionariedade (dependencia temporal da série)

####INVESTIMENTO USA
inv_usa=ts(PIB_Trimestre_Anterior[,3], start=c(1993,1), freq=1)
plot(inv_usa,main='INVESTIMENTO USA',ylab='I',xlab='Trim/Ano',col='blue')
show(inv_usa)

acf(inv_usa)
Acf(inv_usa) #Valores diferentes de 0, declinio suave que pode indicar não estacionariedade (dependencia temporal da série)

#####################Testes de Raiz Unitária

####GASTOS AUTONOMOS USA

################## /KPSS - PP - ADF - Zivot-Andrews/  PARA SÉRIE ORIGINAL
kpss.gastos=ur.kpss(gastos_usa, type='tau', lags="short")
summary(kpss.gastos) #Valor da estatistica é maior do que os criticos... Reeita-se H0 - a série é não estácionaria
plot(kpss.gastos)

pp.gastos=ur.pp(gastos_usa, type="Z-tau", model="constant", lags="short")
summary(pp.gastos)
plot(pp.gastos)

adf.gastos=ur.df(gastos_usa, type="none", selectlags="AIC")
summary(adf.gastos)
plot(adf.gastos)

za.gastos=ur.za(gastos_usa, model="intercept")
summary(za.gastos)
plot(za.gastos)

#Numero de diffs necessarias para transformar em estacionária
ndiffs(gastos_usa)

############################### /KPSS - PP - ADF - Zivot-Andrews/ PARA 1 DIFF
#fazendo a primeira diferenciação
dgastos1=diff(gastos_usa)
plot(dgastos1)

#TESTES
kpss.gastos1=ur.kpss(dgastos1, type='tau', lags="short")
summary(kpss.gastos1) #Valor da estatistica é maior do que os criticos... Reeita-se H0 - a série é não estácionaria
plot(kpss.gastos1)

pp.gastos1=ur.pp(dgastos1, type="Z-tau", model="constant", lags="short")
summary(pp.gastos1)
plot(pp.gastos1)

adf.gastos1=ur.df(dgastos1, type="none", selectlags="AIC")
summary(adf.gastos1)
plot(adf.gastos1)

za.gastos1=ur.za(dgastos1, model="intercept")
summary(za.gastos1)
plot(za.gastos1)

############################### /KPSS - PP - ADF - Zivot-Andrews/ PARA 2 DIFF
#fazendo a segunda diferenciação
dgastos2=diff(gastos_usa, differences=2) 
plot(dgastos2)

#TESTES
kpss.gastos2=ur.kpss(dgastos2, type='tau', lags="short")
summary(kpss.gastos2) #Valor da estatistica é maior do que os criticos... Reeita-se H0 - a série é não estácionaria
plot(kpss.gastos2)

pp.gastos2=ur.pp(dgastos2, type="Z-tau", model="constant", lags="short")
summary(pp.gastos2)
plot(pp.gastos2)

adf.gastos2=ur.df(dgastos2, type="none", selectlags="AIC")
summary(adf.gastos2)
plot(adf.gastos)

za.gastos2=ur.za(dgastos2, model="intercept")
summary(za.gastos2)
plot(za.gastos2)

####INVESTIMENTO USA

################## /KPSS - PP - ADF - Zivot-Andrews/  PARA SÉRIE ORIGINAL
kpss.inv=ur.kpss(inv_usa, type='tau', lags="short")
summary(kpss.inv) #Valor da estatistica é maior do que os criticos... Reeita-se H0 - a série é não estácionaria
plot(kpss.inv)

pp.inv=ur.pp(inv_usa, type="Z-tau", model="constant", lags="short")
summary(pp.inv)
plot(pp.inv)

adf.inv=ur.df(inv_usa, type="none", selectlags="AIC")
summary(adf.inv)
plot(adf.inv)

za.inv=ur.za(inv_usa, model="intercept")
summary(za.inv)
plot(za.inv)

#Numero de diffs necessarias para transformar em estacionária
ndiffs(inv_usa)

################## /KPSS - PP - ADF - Zivot-Andrews/  PARA 1 DIFF
#Fazendo a primeira diff
dinv1=diff(inv_usa)
plot(dinv1)

###############TESTES
kpss.inv1=ur.kpss(dinv1, type='tau', lags="short")
summary(kpss.inv1) #Valor da estatistica é maior do que os criticos... Reeita-se H0 - a série é não estácionaria
plot(kpss.inv1)

pp.inv1=ur.pp(dinv1, type="Z-tau", model="constant", lags="short")
summary(pp.inv1)
plot(pp.inv1)

adf.inv1=ur.df(dinv1, type="none", selectlags="AIC")
summary(adf.inv1)
plot(adf.inv1)

za.inv1=ur.za(dinv1, model="intercept")
summary(za.inv1)
plot(za.inv1)

################## /KPSS - PP - ADF - Zivot-Andrews/  PARA 2 DIFF
#Fazendo a segunda diff
dinv2=diff(inv_usa, differences=2) 
plot(dinv2)

###############TESTES
kpss.inv2=ur.kpss(dinv2, type='tau', lags="short")
summary(kpss.inv2) #Valor da estatistica é maior do que os criticos... Reeita-se H0 - a série é não estácionaria
plot(kpss.inv2)

pp.inv2=ur.pp(dinv2, type="Z-tau", model="constant", lags="short")
summary(pp.inv2)
plot(pp.inv2)

adf.inv2=ur.df(dinv2, type="none", selectlags="AIC")
summary(adf.inv2)
plot(adf.inv2)

za.inv2=ur.za(dinv2, model="intercept")
summary(za.inv2)
plot(za.inv2)

########################################################## ESTIMAÇÃO MODELO VAR

#compactar dados em uma unica matriz PARA OS DADOS ORIGINAIS
    dados1 = cbind(inv_usa, gastos_usa)
    show(dados1)
    plot(inv_usa, col='blue')
    lines(gastos_usa, col='red')
    
    #Média movel para facilitar a visualização
    r=4 #Considerar o ano todo (ts em trimetre)
    INV <- SMA(inv_usa,r)
    plot(INV, col='blue')
    r=4 #Considerar o ano todo (ts em trimetre)
    GAS <- SMA(gastos_usa,r)
    lines(GAS, col='red')


#compactar dados em uma unica matriz com I original/Z primeira diff
dados2_ajuste = cbind(inv_usa, dgastos1)
dados2<-na.omit(dados2_ajuste)
show(dados2)
plot(dados2)

#compactar dados em uma unica matriz com I primeira diff/Z original
dados3_ajuste = cbind(dinv1, gastos_usa)
dados3<-na.omit(dados3_ajuste)
show(dados3)
plot(dados3)

#compactar dados em uma unica matriz para 1 DIFERENÇA
dados4 = cbind(dinv1, dgastos1)
show(dados4)

###############escolher os lags ótimos PARA OS DADOS ORIGINAIS
lagselection = VARselect(dados1, lag.max = 10, type='const')
lagselection$selection

######################escolher os lags ótimos para I original/Z primeira diff
lagselection = VARselect(dados2, lag.max = 10, type='const')
lagselection$selection

#####################escolher os lags ótimos para I primeira diff/Z original
lagselection = VARselect(dados3, lag.max = 10, type='const')
lagselection$selection

#####################escolher os lags ótimos para 1 DIFERENÇAS
lagselection = VARselect(dados4, lag.max = 10, type='const')
lagselection$selection


############################################## ESTIMAÇÃO DO MODELO VAR
Z_I1 = VAR(dados1, type = 'const', lag.max = 1)
summary(Z_I1)

Z_I2 = VAR(dados2, type = 'const', lag.max = 1)
summary(Z_I2)

Z_I3 = VAR(dados3, type = 'const', lag.max = 1)
summary(Z_I3)

Z_I4 = VAR(dados4, type = 'const', lag.max = 8)
summary(Z_I4)

################################ ESTIMAÇÃO GRANGER CAUSALITY (x ~ y) -> y granger-causa x
#Rejeitar H0 significa que y granger-causa x
#I original / Z original
grangertest(gastos_usa ~ inv_usa, order = 1) 
grangertest(gastos_usa ~ inv_usa, order = 2)
grangertest(gastos_usa ~ inv_usa, order = 3)
grangertest(gastos_usa ~ inv_usa, order = 4)
grangertest(gastos_usa ~ inv_usa, order = 5)
grangertest(gastos_usa ~ inv_usa, order = 6)
grangertest(gastos_usa ~ inv_usa, order = 7)
grangertest(gastos_usa ~ inv_usa, order = 8)
grangertest(gastos_usa ~ inv_usa, order = 9)
grangertest(gastos_usa ~ inv_usa, order = 10)
grangertest(inv_usa ~ gastos_usa, order = 1) 
grangertest(inv_usa ~ gastos_usa, order = 2)
grangertest(inv_usa ~ gastos_usa, order = 3)
grangertest(inv_usa ~ gastos_usa, order = 4)
grangertest(inv_usa ~ gastos_usa, order = 5)
grangertest(inv_usa ~ gastos_usa, order = 6)
grangertest(inv_usa ~ gastos_usa, order = 7)
grangertest(inv_usa ~ gastos_usa, order = 8)
grangertest(inv_usa ~ gastos_usa, order = 9)
grangertest(inv_usa ~ gastos_usa, order = 10)

#I original / Z primeira diff
grangertest(dgastos1 ~ inv_usa, order = 1) 
grangertest(dgastos1 ~ inv_usa, order = 2)
grangertest(dgastos1 ~ inv_usa, order = 3)
grangertest(dgastos1 ~ inv_usa, order = 4)
grangertest(dgastos1 ~ inv_usa, order = 5)
grangertest(dgastos1 ~ inv_usa, order = 6)
grangertest(dgastos1 ~ inv_usa, order = 7)
grangertest(dgastos1 ~ inv_usa, order = 8)
grangertest(dgastos1 ~ inv_usa, order = 9)
grangertest(dgastos1 ~ inv_usa, order = 10)
grangertest(inv_usa ~ dgastos1, order = 1) 
grangertest(inv_usa ~ dgastos1, order = 2)
grangertest(inv_usa ~ dgastos1, order = 3)
grangertest(inv_usa ~ dgastos1, order = 4)
grangertest(inv_usa ~ dgastos1, order = 5)
grangertest(inv_usa ~ dgastos1, order = 6)
grangertest(inv_usa ~ dgastos1, order = 7)
grangertest(inv_usa ~ dgastos1, order = 8)
grangertest(inv_usa ~ dgastos1, order = 9)
grangertest(inv_usa ~ dgastos1, order = 10)

#I primeira diff / Z original
grangertest(gastos_usa ~ dinv1, order = 1) 
grangertest(gastos_usa ~ dinv1, order = 2)
grangertest(gastos_usa ~ dinv1, order = 3)
grangertest(gastos_usa ~ dinv1, order = 4)
grangertest(gastos_usa ~ dinv1, order = 5)
grangertest(gastos_usa ~ dinv1, order = 6)
grangertest(gastos_usa ~ dinv1, order = 7)
grangertest(gastos_usa ~ dinv1, order = 8)
grangertest(gastos_usa ~ dinv1, order = 9)
grangertest(gastos_usa ~ dinv1, order = 10)
grangertest(dinv1 ~ gastos_usa, order = 1) 
grangertest(dinv1 ~ gastos_usa, order = 2)
grangertest(dinv1 ~ gastos_usa, order = 3)
grangertest(dinv1 ~ gastos_usa, order = 4)
grangertest(dinv1 ~ gastos_usa, order = 5)
grangertest(dinv1 ~ gastos_usa, order = 6)
grangertest(dinv1 ~ gastos_usa, order = 7)
grangertest(dinv1 ~ gastos_usa, order = 8)
grangertest(dinv1 ~ gastos_usa, order = 9)
grangertest(dinv1 ~ gastos_usa, order = 10)

#I primeira diff / Z primeira diff
grangertest(dgastos1 ~ dinv1, order = 1) 
grangertest(dgastos1 ~ dinv1, order = 2)
grangertest(dgastos1 ~ dinv1, order = 3)
grangertest(dgastos1 ~ dinv1, order = 4)
grangertest(dgastos1 ~ dinv1, order = 5)
grangertest(dgastos1 ~ dinv1, order = 6)
grangertest(dgastos1 ~ dinv1, order = 7)
grangertest(dgastos1 ~ dinv1, order = 8)
grangertest(dgastos1 ~ dinv1, order = 9)
grangertest(dgastos1 ~ dinv1, order = 10)
grangertest(dinv1 ~ dgastos1, order = 1) 
grangertest(dinv1 ~ dgastos1, order = 2)
grangertest(dinv1 ~ dgastos1, order = 3)
grangertest(dinv1 ~ dgastos1, order = 4)
grangertest(dinv1 ~ dgastos1, order = 5)
grangertest(dinv1 ~ dgastos1, order = 6)
grangertest(dinv1 ~ dgastos1, order = 7)
grangertest(dinv1 ~ dgastos1, order = 8)
grangertest(dinv1 ~ dgastos1, order = 9)
grangertest(dinv1 ~ dgastos1, order = 10)
################################ FUNÇÃO IMPULSO-RESPOSTA

plot(irf(Z_I1, impulse = 'gastos_usa', response='inv_usa', n.ahead = 10, ci = 0.95))
plot(irf(Z_I2, impulse = 'dgastos1', response='inv_usa', n.ahead = 10, ci = 0.95))
plot(irf(Z_I3, impulse = 'gastos_usa', response='dinv1', n.ahead = 10, ci = 0.95))
plot(irf(Z_I4, impulse = 'dgastos1', response='dinv1', n.ahead = 10, ci = 0.95))

plot(irf(Z_I1, impulse = 'inv_usa', response='gastos_usa', n.ahead = 10, ci = 0.95))
plot(irf(Z_I2, impulse = 'inv_usa', response='dgastos1', n.ahead = 10, ci = 0.95))
plot(irf(Z_I3, impulse = 'dinv1', response='gastos_usa', n.ahead = 10, ci = 0.95))
plot(irf(Z_I4, impulse = 'dinv1', response='dgastos1', n.ahead = 10, ci = 0.95))

plot(irf(Z_I1, impulse = 'gastos_usa', response='gastos_usa', n.ahead = 10, ci = 0.95))
plot(irf(Z_I1, impulse = 'inv_usa', response='inv_usa', n.ahead = 10, ci = 0.95))

################################ DECOMPOSIÇÃO DA VARIANCIA

fevd(Z_I1, n.ahead = 20)
fevd(Z_I2, n.ahead = 10)
fevd(Z_I3, n.ahead = 10)
fevd(Z_I4, n.ahead = 10)

################################ INSPEÇÃO DOS RESÍDUOS
#Teste de Heterocedasticidade
ArchTest(inv_usa, lag=25) # Teste ARCH - Teste p/ heteroc. condicional
ArchTest(gastos_usa, lag=25)
