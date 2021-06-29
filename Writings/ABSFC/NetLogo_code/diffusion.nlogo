extensions [palette]


breed [houses house ]      ; a house, may be occupied and may be for sale
breed [lands land ]        ; a land unit
breed [owners owner]       ; a house owner. No active role in this version


houses-own [
  occupied?
  for-sale?
  price            ; house current price
  my-owner
  ]


lands-own [
  occupied?
  price            ; house current price
  my-owner
  ]
owners-own [
  my-house
  income
]

globals [
  ;; these could become sliders
  ;; density-ratio ; Slider
  ;; prob-shock ; Slider
  exog-house-price-shock
  ;; Locality ; Slider
  ;; initial-house-price ; Slider
  VacancyRate
  edge-patches   ;; border patches where value should remain 0
  main-patches   ;; patches not on the border
  max-price
]


to build-house
  create-houses 1 [
    ; set shape "custom-house"
    set shape "house"
    set price initial-house-price
    set color brown
    set occupied? true
    ; hide-turtle
    move-to one-of patches
    if count houses-here > 1 [
            let empty-sites patches with [not any? houses-here ]
            if any? empty-sites [ move-to one-of empty-sites ]
        ]
    ]
end

to generate-land
  create-lands 1 [
    set shape "tree" ;; For aesthetics only
    set price  0
    set color green
    set occupied? false
    set my-owner nobody
    move-to one-of patches
    if count houses-here > 1 or count lands-here > 0 [
      let empty-space patches with [ not (any? houses-here or any? lands-here) ]
            if any? empty-space [ move-to one-of empty-space ]
        ]
      ]
end

to owns-house
  set-default-shape owners "dot"
  let occupied-houses n-of ((1 - VacancyRate) * count houses) houses
  ask occupied-houses [
    set for-sale? false
    set occupied? true
    hatch-owners 1 [
      set color red
      set size 0.7
      set my-house myself
      ask my-house [ set my-owner myself ]
    ]
  ]

end

to setup
  clear-all
  reset-ticks
  repeat (round (count patches * density-ratio / 100)) [ build-house ]
  repeat (round (count patches * (100 - density-ratio ) / 100)) [ generate-land]
  ask patches [ set pcolor gray + 3 ]
  set edge-patches patches with [count neighbors != 8]
  set main-patches patches with [count neighbors = 8]
  set prob-shock 0.03
  set exog-house-price-shock 0.01
  set VacancyRate 0.7
  set max-price 1000
  owns-house
end

to go
  if max [price] of houses > max-price [stop]
  update-house-price
  tick
end

to update-house-price
  ask houses [
    let shocked? random 100 < prob-shock
    ifelse not shocked? [
      let num-of-occ-houses count (houses-on neighbors)  with [ distance myself < Locality ]
      ifelse num-of-occ-houses > 1 [
        set price (mean [price] of (houses-on neighbors) with [ distance myself < Locality ])
        set color scale-color brown price ( max-price + 9 ) (initial-house-price - 9)
      ] [set price price set color blue ] ; For inspection
    ] [ set price price * (1 + exog-house-price-shock) set color yellow]
  ]
end

to do-plots
  set-current-plot "house price median"
  set-current-plot-pen "median"
  plot median [price] of houses
end

;
