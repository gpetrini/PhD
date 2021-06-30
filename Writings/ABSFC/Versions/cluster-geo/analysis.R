library(tidyverse)
library(data.table)
library(stargazer)

metrics <- c(
  "geral-house-price-mean"
)

internals <- c(
  "[run number]",
  "[step]",
  "no-gui?",
  "debug-setup",
  "debug?"
)

df <- data.table::fread(
  "./output/baseline.csv",
  skip = 6
) %>%
  select(-c(all_of(metrics), all_of(internals))) %>%
  unique() %>%
  rename(
    `Density ratio` = `initial-density-ratio`
  ) %>%
  pander::pander(style = "grid")

df <- data.table::fread(
  "./output/baseline.csv",
  skip = 6
) %>%
  arrange(`[run number]`) %>%
  rename(
    time = `[step]`,
    `House price mean` = `geral-house-price-mean`,
    simulation = `[run number]`
  ) %>%
  filter(time > 0) %>%
  select(time, `House price mean`, simulation, InitialGeography) %>%
  mutate(
    simulation = factor(simulation),
    InitialGeography = factor(InitialGeography)
  )

initial_drop <- 100

df <- data.table::fread(
  "./output/baseline.csv",
  skip = 6
) %>%
  arrange(`[run number]`, `initial-density-ratio`, Locality) %>%
  rename(
    time = `[step]`,
    `House price mean` = `geral-house-price-mean`,
    simulation = `[run number]`
  ) %>%
  filter(time > 0) %>%
  mutate(
    simulation = factor(simulation),
    density = factor(`initial-density-ratio`),
    Locality = factor(Locality),
    InitialGeography = factor(InitialGeography)
  )



stats <- df %>%
  group_by(simulation) %>%
  filter(time > initial_drop, `House price mean` > `House price mean`[time == 1]) %>%
  mutate(tmp = 1:n()) %>%
  ungroup() %>%
  arrange(simulation, time) %>%
  group_by(InitialGeography, density, Locality) %>%
  summarise(
    `Mean` = mean(`House price mean`),
    `Price >= initial price` = mean(time[tmp == 1], na.rm = TRUE),
    ## `Min` = min(`House price mean`),
    `Median` = median(`House price mean`),
    `Max` = max(`House price mean`),
    `sd` = sd(`House price mean`)
  ) %>%
  ungroup() %>%
  mutate(
    density = density %>% as.character() %>% as.numeric(),
    Locality = Locality %>% as.character() %>% as.numeric(),
    InitialGeography = InitialGeography %>% as.character()
    ) %>%
  arrange(`Mean`) %>%
  suppressMessages()

stats %>%
  pander::pandoc.table(style = "grid")

df %>%
  ggplot(aes(x = time, y = log(`House price mean`), group = round(time / 50))) +
  facet_wrap(. ~ InitialGeography) +
  geom_boxplot() -> plot
ggsave('./figs/baseline_house_price_mean.png', plot)

metrics <- c(
  "geral-house-price-mean"
)

internals <- c(
  "[run number]",
  "[step]",
  "no-gui?",
  "debug?",
  "debug-setup"
)

df <- data.table::fread(
  "./output/exp-density-locality.csv",
  skip = 6
) %>%
  select(-c(all_of(metrics), all_of(internals))) %>%
  unique() %>%
  rename(
    `Density` = `initial-density-ratio`,
  ) %>%
  mutate(Exp = 1:n()) %>%
  relocate(Exp, .before = 1) %>%
  pander::pander(style = "grid")

initial_drop <- 100
variables <- c(
  "initial-density-ratio",
  "Locality",
  "min-land-price-share"
)

df <- data.table::fread(
  "./output/exp-density-locality.csv",
  skip = 6
) %>%
  arrange(`[run number]`, `initial-density-ratio`, Locality) %>%
  rename(
    time = `[step]`,
    `House price mean` = `geral-house-price-mean`,
    simulation = `[run number]`
  ) %>%
  filter(time > 0) %>%
  mutate(
    simulation = factor(simulation),
    density = factor(`initial-density-ratio`),
    Locality = factor(Locality),
    InitialGeography = factor(InitialGeography)
  )

experiments <- df %>%
  select(all_of(variables)) %>%
  unique() %>%
  mutate(Exp = 1:n())


df <- df %>%
  left_join(experiments) %>%
  suppressMessages()

stats <- df %>%
  group_by(Exp) %>%
  filter(time > initial_drop, `House price mean` > `geral-house-price`[time == 1]) %>%
  mutate(tmp = 1:n()) %>%
  ungroup() %>%
  arrange(simulation, time) %>%
  group_by(Exp, density, Locality, min_land_price) %>%
  summarise(
    `Mean` = mean(`House price mean`, na.rm = TRUE),
    `Price >= initial price` = mean(time[tmp == 1], na.rm = TRUE),
    ## `Min` = min(`House price mean`),
    ## `Median` = median(`House price mean`),
    `Max` = max(`House price mean`),
    `sd` = sd(`House price mean`)
  ) %>%
  ungroup() %>%
  mutate(
    density = density %>% as.character() %>% as.numeric(),
    Locality = Locality %>% as.character() %>% as.numeric(),
    InitialGeography = InitialGeography %>% as.character()
  ) %>%
  arrange(`Mean`) %>%
  suppressMessages() %>%
  pander::pandoc.table(style = "grid")

df %>%
  ggplot(aes(x = time, y = log(`House price mean`), group = round(time / 100))) +
  ## geom_vline(aes(xintercept = vline, group = simulation), df_first) +
  geom_hline(yintercept = log(1), color = 'red') +
  facet_grid(density ~ Locality) +
  geom_boxplot() -> plot
ggsave('./figs/densityxlocality_house_price_mean.png', plot)

df %>%
  ggplot(aes(x = time, y = log(`House price mean`), group = round(time / 100))) +
  ## geom_vline(aes(xintercept = vline, group = simulation), df_first) +
  geom_hline(yintercept = log(1), color = 'red') +
  facet_grid(min_land_price ~ density) +
  geom_boxplot() -> plot
ggsave('./figs/min_density_house_price_mean.png', plot)

df %>%
  ggplot(aes(x = time, y = log(`House price mean`), group = round(time / 100))) +
  ## geom_vline(aes(xintercept = vline, group = simulation), df_first) +
  geom_hline(yintercept = log(1), color = 'red') +
  facet_grid(min_land_price ~ Locality) +
  geom_boxplot() -> plot
ggsave('./figs/min_locality_house_price_mean.png', plot)

df %>%
  ggplot(aes(x = time, y = log(`House price mean`), group = round(time / 100))) +
  ## geom_vline(aes(xintercept = vline, group = simulation), df_first) +
  geom_hline(yintercept = log(1), color = 'red') +
  facet_wrap(~ Exp, ncol=5) +
  geom_boxplot() -> plot
ggsave('./figs/all_experiments.png', plot)

@#$#@#$#@
GRAPHICS-WINDOW
210
10
812
613
-1
-1
18.0
1
10
1
1
1
0
0
0
1
-16
16
-16
16
0
0
1
ticks
30.0

BUTTON
0
60
73
93
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
78
60
141
93
NIL
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
39
99
102
132
NIL
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SWITCH
29
159
138
192
no-gui?
no-gui?
1
1
-1000

SWITCH
5
377
139
410
debug?
debug?
1
1
-1000

CHOOSER
4
415
175
460
debug-setup
debug-setup
"none" "1 patches" "2 realtors" "2.5 build-a-house" "3 houses" "4 owners" "5 empty" "6 cluster" "7 quality" "9 realtors: my-houses, avg-price" "10 records" "11 paint-log-price"
0

CHOOSER
8
284
179
329
InitialGeography
InitialGeography
"Random" "Gradient" "Clustered"
0

@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
NetLogo 6.2.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@

@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@

<?xml version="1.0" encoding="utf-8"?>
  <experiment name="baseline-run" repetitions="5" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="1000"/>
    <exitCondition>not any? houses</exitCondition>
    <metric>geral-house-price-mean</metric>
    <enumeratedValueSet variable="no-gui?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial-density-ratio">
      <value value="70"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Locality">
      <value value="2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="InitialGeography">
      <value value="&quot;Random&quot;"/>
      <value value="&quot;Gradient&quot;"/>
      <value value="&quot;Clustered&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="debug-setup">
      <value value="&quot;none&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="debug?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>

<?xml version="1.0" encoding="utf-8"?>
  <experiment name="density-locality-run" repetitions="5" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="1000"/>
    <exitCondition>not any? houses</exitCondition>
    <metric>geral-house-price-mean</metric>
    <enumeratedValueSet variable="no-gui?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial-density-ratio">
      <value value="20"/>
      <value value="50"/>
      <value value="70"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Locality">
      <value value="1"/>
      <value value="2"/>
      <value value="5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="InitialGeography">
      <value value="&quot;Random&quot;"/>
      <value value="&quot;Gradient&quot;"/>
      <value value="&quot;Clustered&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="debug-setup">
      <value value="&quot;none&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="debug?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>

../../NetLogo/netlogo-headless.sh \
        --model cluster-geo.nlogo \
        --experiment random-baseline-run \
        --table ./output/baseline.csv \
        --threads 6

../../NetLogo/netlogo-headless.sh \
        --model cluster-geo.nlogo \
        --experiment density-locality-run \
        --table ./output/exp-density-locality.csv \
        --threads 6
