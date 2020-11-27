library(strucchange)
library(urca)
library(dplyr)

df <- read.csv(
  "./data/Complete_Data.csv",
  encoding="UTF-8", 
  stringsAsFactors=FALSE
  )
df <- ts(data = df, start = c(1987,01), frequency = 4)
df <- zoo::na.locf0(df)
colnames(df) <- c("X", "Infla", "gIh", "Own", "Interest rate")

## Taxa de crescimento do Residential investment


result = breakpoints(gIh~1, data=df)
result$breakpoints %>% unique() %>% na.omit() %>% c() -> breaks

for(i in breaks){
  print(paste0("Testando para i = ", index(df)[i]))
  strucchange::sctest(gIh~1, data=df, point=i, type="Chow") %>% print()
}


## Own Interest rate


result = breakpoints(Own~1, data=df)
result$breakpoints %>% unique() %>% na.omit() %>% c() -> breaks

for(i in breaks){
  print(paste0("Testando para i = ", index(df)[i]))
  strucchange::sctest(Own~1, data=df, point=i, type="Chow") %>% print()
}


## Interest rate


result = breakpoints(Interest rate~1, data=df)
result$breakpoints %>% unique() %>% na.omit() %>% c() -> breaks

for(i in breaks){
  print(paste0("Testando para i = ", index(df)[i]))
  strucchange::sctest(Interest rate~1, data=df, point=i, type="Chow") %>% print()
}


## Inflation


result = breakpoints(Infla~1, data=df)
result$breakpoints %>% unique() %>% na.omit() %>% c() -> breaks

for(i in breaks){
  print(paste0("Testando para i = ", index(df)[i]))
  strucchange::sctest(Infla~1, data=df, point=i, type="Chow") %>% print()
}
