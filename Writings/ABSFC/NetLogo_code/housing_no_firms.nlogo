extensions [palette]


breed [houses house ]      ; a house, may be occupied and may be for sale
breed [lands land ]        ; a land unit

houses-own [
  my-x-cord           ; house x coordinate
  my-y-cord           ; house y coordinate
  my-price            ; house current price
  shocked?            ; If a house will be shocked
  ]


land-own [
  my-x-cord           ; house x coordinate
  my-y-cord           ; house y coordinate
  my-price            ; house current price
  ]
