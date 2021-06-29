breed [houses house ]      ; a house, may be occupied and may be for sale
breed [owners owner ]      ; a household, may be living in a house, or may be seeking one
breed [realtors realtor ]  ; an estate agent
breed [records record ]    ; a record of a sale, kept by realtors

houses-own [
  my-owner            ; the owner who lives in this house
  local-realtors      ; the local realtors
  quality             ; index of quality of this house relative to its neighbours
  for-sale?           ; whether this house is currently for sale
  sale-price          ; the price of this house (either now, or when last sold)
  date-for-sale       ; when the house was put on the market
  my-realtor          ; if for sale, which realtor is selling it
  offered-to          ; which owner has already made an offer for this house
  offer-date          ; date of the offer (in ticks)
  end-of-life         ; time step when this house will be demolished
  ]


to setup

    repeat (count patches * Density / 100) [ build-house ]
    ;; Density=70% is a slider global variable for houses, 70 houses on 100 patches, use this ratio to create enough houses for this world
  
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    if debug? or debug-setup = "3 houses" [
      inspect max-one-of houses [who]
      user-message (word "3 houses : build a number of houses. Check which properties are initialized. " )
      stop-inspecting max-one-of houses [who]
    ]
   ; 3 create and distribute the houses

  set medianPriceOfHousesForSale median [sale-price] of houses  ;; get median price for all houses
  
     ask houses [
  
      set quality sale-price / medianPriceOfHousesForSale  ;; quality is sale-price/median-price
  
      if quality > 3 [set quality 3] if quality < 0.3 [set quality 0.3]  ;; quality is between 0.3 to 3
  
  
  ;    set color scale-color magenta quality 0 5  ;; quality by magenta scale
  
    ]
  
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    if debug? or debug-setup = "7 quality" [
  
      inspect max-one-of houses [ who ]
      user-message (word "7 quality: initialize quality of house, based on sale-price " )
      stop-inspecting max-one-of houses [ who ]
    ] ; 7 quality

end
