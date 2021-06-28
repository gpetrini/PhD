import pandas as pd
import xmltodict
import xml.etree.ElementTree as ET

library(tidyverse)
library(data.table)
library(stargazer)

metrics <- c(
  "mean [price] of houses"
)

internals <- c(
  "[run number]",
  "[step]",
  "no-gui?"
)

df <- data.table::fread(
  "./output/baseline.csv",
  skip = 6
) %>%
  first() %>%
  select(-c(all_of(metrics), all_of(internals))) %>%
  rename(
    `Initial house price` = `initial-house-price`,
    `Density ratio` = `initial-density-ratio`,
    `Land/House price (%)` = `land-house-price-share`
  ) %>%
  pander::pander(style = "grid")

df <- data.table::fread(
  "./output/baseline.csv",
  skip = 6
) %>%
  arrange(`[run number]`) %>%
  rename(
    time = `[step]`,
    `House price mean` = `mean [price] of houses`,
    simulation = `[run number]`
  ) %>%
  filter(time > 0) %>%
  select(time, `House price mean`, simulation) %>%
  mutate(simulation = factor(simulation))

initial_drop <- 100

df <- data.table::fread(
  "./output/baseline.csv",
  skip = 6
) %>%
  arrange(`[run number]`, `initial-density-ratio`, Locality) %>%
  rename(
    time = `[step]`,
    `House price mean` = `mean [price] of houses`,
    simulation = `[run number]`
  ) %>%
  filter(time > 0) %>%
  mutate(
    simulation = factor(simulation),
    density = factor(`initial-density-ratio`),
    Locality = factor(Locality)
  )



stats <- df %>%
  group_by(simulation) %>%
  filter(time > initial_drop, `House price mean` > `initial-house-price`) %>%
  mutate(tmp = 1:n()) %>%
  ungroup() %>%
  arrange(simulation, time) %>%
  group_by(density, Locality) %>%
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
    Locality = Locality %>% as.character() %>% as.numeric(Locality)
    ) %>%
  arrange(`Mean`) %>%
  suppressMessages()

stats %>%
  pander::pandoc.table(style = "grid")

df %>%
  ggplot(aes(x = time, y = log(`House price mean`), group = round(time / 50))) +
  geom_boxplot() -> plot
ggsave('./figs/baseline_house_price_mean.png', plot)

metrics <- c(
  "mean [price] of houses"
)

internals <- c(
  "[run number]",
  "[step]",
  "no-gui?"
)

df <- data.table::fread(
  "./output/exp-density-locality.csv",
  skip = 6
) %>%
  select(-c(all_of(metrics), all_of(internals))) %>%
  unique() %>%
  rename(
    `Initial house price` = `initial-house-price`,
    `Density` = `initial-density-ratio`,
    `Land/House price (%)` = `land-house-price-share`
  ) %>%
  mutate(Exp = 1:n()) %>%
  relocate(Exp, .before = 1) %>%
  pander::pander(style = "grid")

initial_drop <- 100
variables <- c(
  "density",
  "Locality"
)

df <- data.table::fread(
  "./output/exp-density-locality.csv",
  skip = 6
) %>%
  arrange(`[run number]`, `initial-density-ratio`, Locality) %>%
  rename(
    time = `[step]`,
    `House price mean` = `mean [price] of houses`,
    simulation = `[run number]`
  ) %>%
  filter(time > 0) %>%
  mutate(
    simulation = factor(simulation),
    density = factor(`initial-density-ratio`),
    Locality = factor(Locality)
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
  filter(time > initial_drop, `House price mean` > `initial-house-price`) %>%
  mutate(tmp = 1:n()) %>%
  ungroup() %>%
  arrange(simulation, time) %>%
  group_by(Exp, density, Locality) %>%
  summarise(
    `Mean` = mean(`House price mean`),
    `Price >= initial price` = mean(time[tmp == 1], na.rm = TRUE),
    ## `Min` = min(`House price mean`),
    ## `Median` = median(`House price mean`),
    `Max` = max(`House price mean`),
    `sd` = sd(`House price mean`)
  ) %>%
  ungroup() %>%
  mutate(
    density = density %>% as.character() %>% as.numeric(),
    Locality = Locality %>% as.character() %>% as.numeric(Locality)
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

breed [houses house ]      ; a house, may be occupied and may be for sale
breed [lands land ]        ; a land unit

globals [
  ;; these could become sliders
  ; no-gui? ;; Slider
  model-version
  initial-density-ratio
  exog-house-price-shock
  shocked-house
  Locality
  initial-house-price
  land-house-price-share
  initial-land-price
  min-land-price
  num-of-new-houses
  unshocked-houses
]

houses-own [
  price            ; house current price
  shocked?
  existing-time
  agents-around-here
  ]


lands-own [
  price            ; house current price
  agents-around-here
  ]

to build-house
  create-houses 1 [
    if no-gui? = false [
    ; set shape "custom-house"
    set color brown
    set shape "house"
    ]
    set existing-time 0
    set price initial-house-price
    set shocked? false
    move-to one-of patches
    if count houses-here > 0 [
            let empty-sites patches with [not any? houses-here ]
            if any? empty-sites [ move-to one-of empty-sites ]
        ]
    ]
end

to generate-land
  create-lands 1 [
    if no-gui? = false [
    set shape "tree" ;; For aesthetics only
    set color green
    ]
    set price  initial-land-price
    move-to one-of patches
    if count houses-here > 0 or count lands-here > 0 [
      let empty-space patches with [ not (any? houses-here or any? lands-here) ]
            if any? empty-space [ move-to one-of empty-space ]
        ]
      ]
end

to setup
  clear-all
  reset-ticks
  set model-version "no-diffusion"
  set min-land-price 0.9
  ; set no-gui? true
  if initial-density-ratio = 0 [set initial-density-ratio random 100 + 1] ;; just to initialize and create at least one house
  ; if initial-house-price = 0 [set initial-house-price random 5 + 1] ;; just to initialize
  set initial-house-price 1
  if Locality = 0 [set Locality random 5 + 1] ;; just to initialize
  if land-house-price-share = 0 [set land-house-price-share (random (100 - (min-land-price * 100)) + (min-land-price * 100))/(100)] ;; just to initialize

  repeat (round (count patches * initial-density-ratio / 100)) [ build-house ]
  repeat (round (count patches * (100 - initial-density-ratio ) / 100)) [ generate-land]
  ;; Find neighbors globaly to increase performance
  ;; Attention: this procedure assumes that other agents position is not relevant for this.
  find-neighbors houses
  ask one-of houses [set shocked? true set color yellow]
  set unshocked-houses houses with [shocked? = false]
  ask patches [ set pcolor gray + 3 ]
  set exog-house-price-shock 0.01
  set initial-land-price land-house-price-share * initial-house-price
  ask lands [
    set price initial-land-price
  ]
end

to update-age
  set existing-time (1 + existing-time)
end

to update-house-price
  ask houses [
    update-age
    ifelse shocked? = false [
      ;; Ensure that only houses or lands are select for future compability
      ;; Temporary variable to reduce code size
      set price (mean [price] of agents-around-here)
      if no-gui? = false [
        set color scale-color brown ln (price + 0.001) (ln max [price] of unshocked-houses + 1 ) (ln (min [price] of unshocked-houses + 1) )
        ]
      ]
   [ set price price * (1 + exog-house-price-shock)]
  ]
end

to go
  if (ticks > 1000) or (not any? houses) [
    stop
    show (word "Execution finished in " timer " seconds")
]
  update-house-price
  tick
end

to find-neighbors [agent]
  ask agent [
    set agents-around-here other turtles in-radius Locality with [breed = houses or breed = lands]
  ]
end

to do-plots
  set-current-plot "House price statistics"
  set-current-plot-pen "median"
  plot median [price] of houses
  set-current-plot-pen "mean"
  plot mean [price] of houses
end

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
27
201
161
234
debugger?
debugger?
1
1
-1000
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
  <experiment name="baseline-run" repetitions="20" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="1000"/>
    <exitCondition>not any? houses</exitCondition>
    <metric>mean [price] of houses</metric>
    <!-- <metric>mean [price] of houses with [shocked? = false]</metric> -->
    <enumeratedValueSet variable="no-gui?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial-density-ratio">
      <value value="70"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial-house-price">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Locality">
      <value value="2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="land-house-price-share">
      <value value="70"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="min-land-price">
      <value value="0.9"/>
    </enumeratedValueSet>
  </experiment>

<?xml version="1.0" encoding="utf-8"?>
  <experiment name="density-locality-run" repetitions="50" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="1000"/>
    <exitCondition>not any? houses</exitCondition>
    <metric>mean [price] of houses</metric>
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
    <enumeratedValueSet variable="land-house-price-share">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial-house-price">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="min-land-price">
      <value value="0.2"/>
      <value value="0.5"/>
      <value value="0.99"/>
    </enumeratedValueSet>
  </experiment>

../../NetLogo/netlogo-headless.sh \
        --model one-diffusion.nlogo \
        --experiment baseline-run \
        --table ./output/baseline.csv \
        --threads 6

../../NetLogo/netlogo-headless.sh \
        --model one-diffusion.nlogo \
        --experiment density-locality-run \
        --table ./output/exp-density-locality.csv \
        --threads 6
