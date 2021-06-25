import pandas as pd

experiment = pd.DataFrame.from_dict(
)

breed [houses house ]      ; a house, may be occupied and may be for sale
breed [lands land ]        ; a land unit

globals [
  ;; these could become sliders
  ; no-gui? ;; Slider
  model-version
  density-ratio
  exog-house-price-shock
  shocked-house
  Locality
  initial-house-price
  initial-land-price
  num-of-new-houses
  unshocked-houses
]

houses-own [
  price            ; house current price
  shocked?
  existing-time
  ]


lands-own [
  price            ; house current price
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
  ; set no-gui? true
  if density-ratio = 0 [set density-ratio random 100 + 1] ;; just to initialize and create at least one house
  if initial-house-price = 0 [set initial-house-price random 5 + 1] ;; just to initialize
  if Locality = 0 [set Locality random 5 + 1] ;; just to initialize

  repeat (round (count patches * density-ratio / 100)) [ build-house ]
  repeat (round (count patches * (100 - density-ratio ) / 100)) [ generate-land]
  ask one-of houses [set shocked? true set color yellow]
  set unshocked-houses houses with [shocked? = false]
  ask patches [ set pcolor gray + 3 ]
  set exog-house-price-shock 0.01
  set initial-land-price 0
end

to update-age
  set existing-time (1 + existing-time)
end

to update-house-price
  ask houses [
    update-age
    ifelse shocked? = false [
      ;; Ensure that only houses or lands are select for future compability
      let agents-around-here other turtles in-radius Locality with [breed = houses or breed = lands]
      ;; Temporary variable to reduce code size
      set price (mean [price] of agents-around-here)
      if no-gui? = false [
        set color scale-color brown ln price (ln max [price] of unshocked-houses + 1 ) (ln min [price] of unshocked-houses - 1 )
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
  ; set num-of-new-houses houses with [existing-time = 0]
  update-house-price
  tick
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
    <enumeratedValueSet variable="density-ratio">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial-house-price">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Locality">
      <value value="1"/>
    </enumeratedValueSet>
  </experiment>

<?xml version="1.0" encoding="utf-8"?>
  <experiment name="density-locality-run" repetitions="20" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="1000"/>
    <exitCondition>not any? houses</exitCondition>
    <metric>mean [price] of houses</metric>
    <enumeratedValueSet variable="no-gui?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="density-ratio">
      <value value="20"/>
      <value value="50"/>
      <value value="70"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial-house-price">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Locality">
      <value value="1"/>
      <value value="2"/>
      <value value="5"/>
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

library(tidyverse)
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

── [1mAttaching packages[22m ────────────────────────────────────────────────────────────────────────────────────────────── tidyverse 1.3.0 ──
[32m✔[39m [34mggplot2[39m 3.3.3     [32m✔[39m [34mpurrr  [39m 0.3.4
[32m✔[39m [34mtibble [39m 3.0.6     [32m✔[39m [34mdplyr  [39m 1.0.4
[32m✔[39m [34mtidyr  [39m 1.1.2     [32m✔[39m [34mstringr[39m 1.4.0
[32m✔[39m [34mreadr  [39m 1.4.0     [32m✔[39m [34mforcats[39m 0.5.1
── [1mConflicts[22m ───────────────────────────────────────────────────────────────────────────────────────────────── tidyverse_conflicts() ──
[31m✖[39m [34mdplyr[39m::[32mfilter()[39m masks [34mstats[39m::filter()
[31m✖[39m [34mdplyr[39m::[32mlag()[39m    masks [34mstats[39m::lag()

df %>%
  ggplot(aes(x = time, y = `House price mean`, group = round(time / 50))) +
  geom_boxplot() -> plot
ggsave('./figs/baseline_house_price_mean.png', plot)

library(tidyverse)
df <- data.table::fread(
  "./output/exp-density-locality.csv",
  skip = 6
) %>%
  arrange(`[run number]`, `density-ratio`, Locality) %>%
  rename(
    time = `[step]`,
    `House price mean` = `mean [price] of houses`,
    simulation = `[run number]`
  ) %>%
  filter(time > 0) %>%
  mutate(
    simulation = factor(simulation),
    density = factor(`density-ratio`),
    Locality = factor(Locality)
    )



df %>%
  ggplot(aes(x = time, y = `House price mean`, group = round(time / 50))) +
  facet_grid(density ~ Locality) +
  geom_boxplot() -> plot
ggsave('./figs/densityxlocality_house_price_mean.png', plot)
