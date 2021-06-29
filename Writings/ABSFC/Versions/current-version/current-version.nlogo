extensions [palette]


breed [houses house ]      ; a house, may be occupied and may be for sale
breed [lands land ]        ; a land unit


houses-own [
  price            ; house current price
  shocked?
]


lands-own [
  price            ; house current price
]


globals [
  ;; these could become sliders
  ;; density-ratio ; Slider
  exog-house-price-shock
  shocked-house
  ;; Locality ; Slider
  ;; initial-house-price ; Slider
  initial-land-price
]

to build-house
  create-houses 1 [
                                ; set shape "custom-house"
    set shape "house"
    set price initial-house-price
    set color brown
    move-to one-of patches
    if count houses-here > 0 [
      let empty-sites patches with [not any? houses-here ]
      if any? empty-sites [ move-to one-of empty-sites ]
        ]
    ]
end

to generate-land
  create-lands 1 [
    set shape "tree" ;; For aesthetics only
    set price  initial-land-price
    set color green
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
  ask one-of houses [set shocked? true set color yellow]
  repeat (round (count patches * density-ratio / 100)) [ build-house ]
  repeat (round (count patches * (100 - density-ratio ) / 100)) [ generate-land]
  ask patches [ set pcolor gray + 3 ]
  set exog-house-price-shock 0.01
  set land-initial-price 0
end

to go
  if tick > 1000 [stop]
  update-house-price
  tick
end

to update-house-price
  ask houses [
    let shocked?
    ifelse not shocked? [
      let num-of-occ-houses count (houses-on neighbors)  with [ distance myself < Locality ]
      ifelse num-of-occ-houses > 1 [
        set price (mean [price] of (houses-on neighbors) with [ distance myself < Locality ])
        set color scale-color brown price 0 10
      ] [set price price set color blue ] ; For inspection
    ] [ set price price * (1 + exog-house-price-shock)]
  ]
end

to do-plots
  set-current-plot "House price statistics"
  set-current-plot-pen "median"
  plot median [price] of houses
  set-current-plot-pen "mean"
  plot mean [price] of houses
end

;
