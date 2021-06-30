extensions [ palette]


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
  min-land-price-share
  num-of-new-houses
  unshocked-houses
  max-initial-house-price
  min-initial-house-price
  price-difference
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
    set existing-time 0
    set shocked? false
    move-to one-of patches
    if count houses-here > 0 [
            let empty-sites patches with [not any? houses-here ]
            if any? empty-sites [ move-to one-of empty-sites ]
        ]

  if InitialGeography = "Random" or InitialGeography = "Clustered" [
    set price random (max-initial-house-price) + min-initial-house-price
  ]
  if InitialGeography = "Gradient" [  ;; price increase from bottom-left to top-right
   set price initial-house-price * ( xcor + ycor + 50) / 50
  ]
    if no-gui? = false [
    ; set shape "custom-house"

    paint-houses   ;; scale-paint houses based on log price
    ; set color brown
    set shape "house"
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

  set model-version "cluster-geo"
  ; set InitialGeography "Random"
  set price-difference 500  ;; in cluster mode, consider houses whose price is more than 5000 differ from their neighbor houses, belong to different clusters. Since: cluster-geo <2021-06-29 ter>
  set max-initial-house-price 20 * price-difference

  set min-land-price-share 0.9
  ; set no-gui? true
  if initial-density-ratio = 0 [set initial-density-ratio random 100 + 1] ;; just to initialize and create at least one house
  if initial-house-price = 0 [set initial-house-price random 5 + 1] ;; just to initialize

  if Locality = 0 [set Locality random 5 + 1] ;; just to initialize
  if land-house-price-share = 0 [set land-house-price-share (random (100 - (min-land-price-share * 100)) + (min-land-price-share * 100))/(100)] ;; just to initialize

  repeat (round (count patches * initial-density-ratio / 100)) [ build-house ]
   if InitialGeography = "Clustered" [ cluster ]   ;; move houses to the neighbors with similar prices

  repeat (round (count patches * (100 - initial-density-ratio ) / 100)) [ generate-land]
  ;; Find neighbors globaly to increase performance
  ;; Attention: this procedure assumes that other agents position is not relevant for this.
  find-neighbors houses
  ask patches [ set pcolor gray + 3 ]
  set exog-house-price-shock 0.01
  set initial-land-price land-house-price-share * (mean [price] of houses) ;; Since cluster-geo: <2021-06-29 ter> as initial house price varies.
  ask lands [
    set price initial-land-price
  ]
  set debug-setup "none" ;; For sanity check. Since: cluster-geo <2021-06-29 ter>



  ask one-of houses [set shocked? true set color yellow]
  set unshocked-houses houses with [shocked? = false]

end

to go
  if (ticks > 1000) or (not any? houses) [
    stop
    show (word "Execution finished in " timer " seconds")
]
  update-house-price
  tick
end

to update-house-price
  ask houses [
    update-age
    ifelse shocked? = false [
      ;; Ensure that only houses or lands are select for future compability
      ;; Temporary variable to reduce code size
      set price local-house-price-mean ;; This is now a procedure
      if no-gui? = false [
        paint-houses
        ]
      ]
   [ set price price * (1 + exog-house-price-shock)]
  ]
end
to update-age
  set existing-time (1 + existing-time)
end
to find-neighbors [agent]
  ask agent [
    set agents-around-here other turtles in-radius Locality with [breed = houses or breed = lands]
  ]
end


to cluster
;; cluster houses together based on price similarity

  repeat 5 [  ;;  cluster all all houses three times

    paint-houses   ;; scale-paint houses based on log price

    let houses-to-move sort-by [ [ house1 house2 ] ->  price-diff house1 > price-diff house2 ] houses  ;; new-version
    ;; reorder every house based on price-difference to its neighbor houses, largest first, smallest last


    foreach houses-to-move [  ;; loop each house

      x -> if price-diff x >= price-difference [  ;; if current house price is way too different from its surroundign houses

        let vacant-plot one-of patches with [  ;; get one of many empty patches, where

                                   not any? houses-here and not any? lands-here and  ;; there is no house built

                                   abs (local-price - [ price ] of x ) < 1000 ]  ;; where the surrounding house prices is similar to the current house

        if vacant-plot != nobody [  ;; if those empty patches do exist

          ask x [  ;; ask this current house

            ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
            ;; Temporarilly disabled
            ; if debug? or debug-setup = "6 cluster" [

            ;   pen-down set pen-size 2  ;; put pen down to draw a track

            ;   if is-owner? my-owner [

            ;     ask my-owner [ follow-me ]  ;; watch the owner ( can't use watch-me here)

            ;   ]
            ;   user-message (word "6 cluster : the house move with a track line, the owner is watched. " )
            ; ]
            ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

            move-to vacant-plot  ;; to move to one of the empty patch

            ;; Temporarilly disabled
            ; if is-owner? my-owner [  ;; whether it got an owner, if so

            ;   ask my-owner [ move-to myself ] ;; ask the owner move to where the house is
            ; ]

            ; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
            ; if debug? or debug-setup = "6 cluster" [

            ;    user-message (word "6 cluster : the house move with a track line, the owner is watched. " )

            ;    pen-up ;; pull pen up
            ; ]
            ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

           ]

          ]
        ]
      ]


  ]

end

to paint-houses

  let min-price precision [price] of min-one-of houses with [ price != 0 ] [price] 1
  let ln-min-price precision ln [price] of min-one-of houses with [ price != 0 ] [price] 1
  let max-price precision [price] of max-one-of houses with [  price != 0 ] [price] 1
  let ln-max-price precision ln [price] of max-one-of houses with [  price != 0 ] [price] 1

  ask houses with [ price != 0 and shocked? = false ] [  ;; maybe set empty house initial 0 price to "0" ?


    set color palette:scale-scheme "Sequential" "Reds" 7 (ln price) ln-min-price ln-max-price

    ; scale-scheme "Divergent" "RdYlBu" 10 ; the number 10 control how many different colors in between, 5 may be the best
    ; good color options:  "Spectral" "RdYlBu" "RdYlGn"
    ;; ok color options : PiYG PRGn PuOr RdBu RdGy
    ;; set color scale-color red ln price ln-min-price ln-max-price

  ]



end

to-report local-price

  let local-houses houses-on neighbors

  ifelse any? local-houses  ;; if `local-houses` is not empty

    [ report median [price] of local-houses ]  ;; report median price of all neighbor houses' prices to be `local-price`

    [ report 0 ] ;; if no neighbor houses, report 0 to be `local-price`

end

to-report price-diff [ a-house ]

  report abs ([price] of a-house - [local-price] of a-house) ;; Note the use [ local-price ] of a-house

end

to-report geral-house-price-mean
 report mean [price] of houses
end
to-report local-house-price-mean

  let local-agents other turtles in-radius Locality with [breed = houses or breed = lands]

  ifelse any? local-agents

    [ report mean [price] of local-agents ]

    [ report 0 ] ;; if no neighbor houses, report 0 to be `local-price`
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
<experiments>
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
</experiments>
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
