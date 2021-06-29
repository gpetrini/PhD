globals[
  gini-index-reserve
  lorenz-points num-hholds
  cprice
  dp%
  stock-price

  salesfinalized
  foreclosedhomes]

breed[houses house] ; houses
houses-own [status foreclosed? forsale? rentprice occupant owner mortgage taxprice price askingprice bidlist tenure]

breed[loans loan] ; loans
loans-own [lender borrower cost remain intrate payment timeleft kind missedpayments asset]

;;;

breed[banks bank] ; commercial/retail bank
banks-own [firmbonds firmcredit hhmortgages hhcredit hhdeposits gbonds bbonds bankdeposits foreclosureproceeds currentaccount capitalaccount fbinterest fcinterest bdinterest hhminterest hhcinterest hhdinterest gbinterest bbinterest revenue expenses profit taxwithholdings bankdividends loanlist badloans]

breed[cbanks cbank] ; central bank
cbanks-own [gbonds bbonds bankdeposits gbinterest bbinterest bdinterest currentaccount revenue expenses profit taxwithholdings loanlist badloans]

breed[firms firm] ; consumption producing firms
firms-own [firmbonds firmcredit fbinterest fcinterest currentaccount wages fiscalspending consumption revenue expenses profit taxwithholdings bankdividends dividends employeelist loanlist]

breed[hholds hhold] ; households
hholds-own [status currentaccount hhmortgages hhcredit hhdeposits hhminterest hhmpayment hhcinterest hhdinterest consumption wages dividends capitalgains rentexpense rentincome income expenses taxwithholdings capitalaccount maxaffordability houselist renthouselist currentbidhouse currentbid loanlist stockowned]

breed[governments government]
governments-own[taxescollected cbprofits fiscalspending gbonds gbinterest currentaccount revenue expenses loanlist]


to set-up
  clear-all
  reset-ticks
  ask patches [set pcolor blue]

  init-houses
  init-agents

  setup-hholds
  setup-firms


  update-houses
  update-lorenz-and-gini
end

to go
  tick

  set foreclosedhomes 0

  ;QUARTERLY ACTIONS
  hholds-quarterly
  banks-quarterly
  firms-quarterly
  governments-quarterly

  ;MONTHLY ACTIONS
  repeat 3 [ ; three months in a quarter
    banks-interact
    government-interact
    firms-interact
    households-interact

    update-houses
  ]
  update-lorenz-and-gini
end

to init-houses
  set-default-shape houses "house"
  ask patches [
    sprout-houses 1]
  ask houses[
    set status "vacant"
    set occupant 0
    set owner 0
    set forsale? false
    set foreclosed? false
    set tenure 0
    set price 75000 + (3000 * count houses in-radius 3)
    set taxprice .9 * price
    set askingprice taxprice
    set rentprice taxprice * rentportion
    set bidlist (list)
    set mortgage 0] ; FIX LATER TO RANDOMIZE MORTGAGES
  update-houses
end

to init-agents
  create-hholds (.95 * count houses) [set hidden? true
  set loanlist (list)]
  create-cbanks 1 [set hidden? true
  set loanlist (list)]
  create-banks 1[
    set hidden? true
  set loanlist (list)]

  create-governments 1 [set hidden? true
  set loanlist (list)]
  create-firms 1 [set hidden? true
  set loanlist (list)]
end

to setup-hholds
  ask hholds [
    set status "homeless"
    set consumption .01 * wealth
    set rentexpense 0
    set currentaccount 20000
    set wages exp (random-normal 8.4 .3)
    set houselist (list)]

  ask houses [
    let temphouse self
    ask one-of hholds [
      set houselist lput temphouse houselist
      ask temphouse [set owner myself]]

    ;set up the random mortgages
    let thishouse self

    let myowner owner
    let myprice price
    let mymortgage 0

    ask myowner [ ; take out loan (mortgage) for the house
      let mortgagerate (cbankrate + .03) / 12

      let loanamount .8 * myprice

      if loanamount > 0 [
        hatch-loans 1 [
          set mymortgage self
          set lender one-of banks
          set borrower myself
          set cost loanamount
          set intrate mortgagerate
          set timeleft random 360
          set payment loanamount * (mortgagerate * ((1 + mortgagerate) ^ 360) / (((1 + mortgagerate) ^ 360) - 1))

          set remain ((cost * ((1 + mortgagerate) ^ timeleft)) - (payment * ((((1 + mortgagerate) ^ timeleft) - 1) / mortgagerate)))
          let tempremain remain

          set asset thishouse

          set kind "hhmortgage"

          ask lender [
            set hhmortgages hhmortgages + tempremain
            set capitalaccount capitalaccount - loanamount
            set loanlist lput myself loanlist]
          ask borrower [
            set hhmortgages hhmortgages + tempremain
            set loanlist lput myself loanlist]]]]


    set owner myowner

    set mortgage mymortgage

    set rentprice taxprice * rentportion]


  ask hholds [
    set houselist sort-on [(- prestige)] (turtle-set houselist)

    if empty? houselist = false [
      ask first houselist [
        set occupant myself
        set tenure 0
        set status "homeowner"]
      set status "homeowner"]]

  repeat 10000[
    ask one-of hholds [
      set stockowned stockowned + 1]]

end

to setup-firms
  ask firms [
    set currentaccount (exp (random-normal 13.1 .5))
  ]

end

;QUARTERLY ACTIONS
to hholds-quarterly
  set salesfinalized 0

  ask houses with [forsale? = true][
    let mybidderlist sort-on [(- currentbid)] bidlist
    ifelse empty? mybidderlist = false [
      let thishouse self
      set mybidderlist sort-on [(- currentbid)] bidlist
      let currentowner owner
      if foreclosed? = true [
        set currentowner one-of banks]
      let currentresident occupant
      let currentprice price
      let newowner first mybidderlist
      let newprice [currentbid] of newowner
      let newmortgage 0

      show currentowner

      ask newowner [ ; take out loan (mortgage) for the house
        let mortgagerate (cbankrate + .03) / 12
        let maxpayment income - expenses
        if maxpayment > debttoincome * income [set maxpayment debttoincome * income]

        set maxpayment maxpayment - (hhmpayment + hhcinterest)

        let maxloan maxpayment / (mortgagerate * ((1 + mortgagerate) ^ 360) / (((1 + mortgagerate) ^ 360) - 1))

        if maxloan > (capitalaccount / min-dpay) [set maxloan (capitalaccount / min-dpay)]

        let loanamount maxloan
        let downpayment currentprice - loanamount

        set capitalaccount capitalaccount - downpayment ; will pay the old owner this + loanamount from bank
        set hhdeposits hhdeposits - downpayment

        ask banks [
          set hhdeposits hhdeposits - downpayment
          set capitalaccount capitalaccount - downpayment]

        if loanamount > 0 [
          hatch-loans 1 [
            set newmortgage self
            set lender one-of banks
            set borrower myself
            set cost loanamount
            set remain loanamount
            set intrate mortgagerate
            set asset thishouse
            set payment loanamount * (mortgagerate * ((1 + mortgagerate) ^ 360) / (((1 + mortgagerate) ^ 360) - 1))
            set timeleft 360
            set kind "hhmortgage"
            set missedpayments 0
            ask lender [
              set hhmortgages hhmortgages + loanamount
              set capitalaccount capitalaccount - loanamount
              set loanlist lput myself loanlist]
            ask borrower [
              set hhmortgages hhmortgages + loanamount
              set loanlist lput myself loanlist]]]

        set houselist lput myself houselist]

      ifelse foreclosed? = false [
        ask currentowner [
          set currentaccount currentaccount + newprice
          set capitalgains capitalgains + (newprice - currentprice)

          if [status] of thishouse = "homeowner" and [tenure] of thishouse > 24 [
            set capitalgains capitalgains - 250000]

          set houselist remove myself houselist
          if status = "homeowner" [
            set status "homeless"]]][;if it is foreclosure then the bank gets the money
        ask currentowner [
          set currentaccount currentaccount + newprice
          set foreclosureproceeds foreclosureproceeds + newprice
      ]]
      if status = "homeowner" [
        set status "vacant"
        set occupant 0]

      set owner newowner
      set forsale? false

      set salesfinalized salesfinalized + 1

      if mortgage != 0 [
        ask mortgage [

          let tempremain remain
          ask lender [
            set capitalaccount capitalaccount + tempremain
            set hhmortgages hhmortgages - tempremain
            set loanlist remove myself loanlist]
          ask borrower[
            set currentaccount currentaccount - tempremain
            set hhmortgages hhmortgages - tempremain
            set loanlist remove myself loanlist]
          die]]

      set mortgage newmortgage

      set foreclosed? false

      ask bidlist [
        set currentbidhouse 0
        set currentbid 0]

      set bidlist (list)

      set price newprice
      set taxprice price * .9
      set rentprice taxprice * rentportion][;if nobody in list, decrease price by 5%
      set askingprice askingprice * .95]] ;

      ;if it's the most prestigious house they own, then the new owner will move into it (or will do in another section)

  show (word "Sales Finalized: " salesfinalized)

  ask hholds [
    ;move into their highest prestige house, or into a home they own (if renter)

    if status = "landlord" [
      if length houselist > 1 [

        let myhomes sort-on [(- prestige)] turtle-set houselist

        let newhome first myhomes

        if [status] of newhome = "renter" [
          let oldhome houses with [occupant = myself]
          let newoccupant self
          let oldoccupant [occupant] of newhome

          ask oldoccupant [
            set status "homeless"
            set rentexpense 0]

          ask oldhome [
            set tenure 0
            set status "vacant"
            set occupant 0]

          ask newhome [
            set tenure 0
            set status "homeowner"
            set occupant newoccupant]]

        if [status] of newhome = "vacant" [
          let oldhome houses with [occupant = myself]
          let newoccupant self

          ask oldhome [
            set tenure 0
            set status "vacant"
            set occupant 0]

          ask newhome [
            set tenure 0
            set status "homeowner"
            set occupant newoccupant]]]]

    if status = "homeowner" [
      if length houselist > 1 [

        let myhomes sort-on [(- prestige)] turtle-set houselist

        let newhome first myhomes

        if [status] of newhome = "renter" [
          let oldhome houses with [occupant = myself]
          let newoccupant self
          let oldoccupant [occupant] of newhome

          ask oldoccupant [
            set status "homeless"
            set rentexpense 0]

          ask oldhome [
            set tenure 0
            set status "vacant"
            set occupant 0]

          ask newhome [
            set tenure 0
            set status "homeowner"
            set occupant newoccupant]]

        if [status] of newhome = "vacant" [
          let oldhome houses with [occupant = myself]
          let newoccupant self

          ask oldhome [
            set tenure 0
            set status "vacant"
            set occupant 0]

          ask newhome [
            set tenure 0
            set status "homeowner"
            set occupant newoccupant]]]]


    if status = "renter" [
      if empty? houselist = false [
        let newhome first houselist

        if [status] of newhome = "renter" [
          let oldhome houses with [occupant = myself]
          let newoccupant self
          let oldoccupant [occupant] of newhome

          ask oldoccupant [
            set status "homeless"
            set rentexpense 0]

          ask oldhome [
            set tenure 0
            set status "vacant"
            set occupant 0]

          ask newhome [
            set tenure 0
            set status "homeowner"
            set occupant newoccupant]]

        if [status] of newhome = "vacant" [
          let oldhome houses with [occupant = myself]
          let newoccupant self

          ask oldhome [
            set tenure 0
            set status "vacant"
            set occupant 0]

          ask newhome [
            set tenure 0
            set status "homeowner"
            set occupant newoccupant]]

        set status "homeowner"]]








    ;list properties for sale

    set expenses (taxwithholdings / 3) + hhmpayment + consumption + rentexpense

    if hhcredit > 0 [
      if empty? houselist = false [
        if not any? (turtle-set houselist) with [forsale? = true][
          let temphouselist but-first houselist
          ifelse empty? temphouselist = false [ ;sell an investment property
            ask one-of temphouselist [
              set forsale? true
              set askingprice taxprice]][;sell their home
            ask one-of houselist [
              set forsale? true
              set askingprice taxprice]]]]]


    set currentbidhouse 0

    ;create list of properties each hhold can afford, list by prestigiousness
    if capitalaccount > 0 [
      ;;figure out how much they can afford 1) loan portion should be either the rest of the portion after paying downpayment or the most they can make payments on and 2) the current state of their capitalaccount
      let maxpayment income - expenses
      if maxpayment > .4 * income [set maxpayment .4 * income]

      let mortgagerate (cbankrate + .03) / 12
      let maxloan maxpayment / (mortgagerate * ((1 + mortgagerate) ^ 360) / (((1 + mortgagerate) ^ 360) - 1))

      if maxloan > (capitalaccount / min-dpay) [set maxloan (capitalaccount / min-dpay)]

      set maxaffordability maxloan + capitalaccount
      let tempmax maxaffordability

      let purchaselist sort-on [(- prestige)] (houses with [askingprice < tempmax and forsale? = true])

      ;take this list and bid randomly on one of the top 5

      if empty? purchaselist = false [
        let randomnumber 5
        if length purchaselist < 5 [set randomnumber length purchaselist]

        set currentbidhouse item (random randomnumber) purchaselist]]

  ;; the top bidder will get the house next turn, and the other bidders will have to look for another house to buy

  ;will look for new apartment if the current one is too expensive and cannot afford home
    if status = "homeless" [
      let myincome income

      let mylist houses with [status = "vacant" and owner != 0]
      let lowcostlist sort-on [(- prestige)] mylist with [rentprice < .3 * myincome]
      let mediumcostlist sort-on [(- prestige)] mylist with [rentprice >= (.3 * myincome) and rentprice <= (.4 * myincome)]
      let highcostlist sort-on [(- prestige)] mylist with [rentprice > (.4 * myincome) and rentprice < (1 * myincome)]

      let myrenthouse 0
      ifelse empty? mediumcostlist = false [ ;move into first of this list
        set myrenthouse first mediumcostlist
      ][;check lowcostlist
        ifelse empty? lowcostlist = false [ ;move into first of this list
          set myrenthouse first lowcostlist
        ][;move into the highcostlist
          if empty? highcostlist = false [
            set myrenthouse first highcostlist
      ]]]


      if myrenthouse != 0 [;if the housing lists showed something acceptable
        ask myrenthouse [
          set occupant myself
          set status "renter"
          set tenure 0]
        set status "renter"
        set rentexpense [rentprice] of myrenthouse]]

    if status = "homeowner" [
      let myhouses turtle-set houselist
      if any? myhouses with [status = "renter"] [
        set status "landlord"]]

    if status = "landlord" [
      let myhouses turtle-set houselist
      if not any? myhouses with [status = "renter"][
        set status "homeowner"]]
  ]

end

to banks-quarterly
  ; pay dividends to firms
  ask banks [
    if bankdividends > 0 [
      let tempdividends bankdividends
      set currentaccount currentaccount - tempdividends
      ask firms [
        set currentaccount currentaccount + tempdividends
        set bankdividends tempdividends]]]
end

to firms-quarterly
  ;turn short-term financing into long-term financing
  ask firms [
    if firmcredit > 0 [
      let bondamount firmcredit
      let interestrate (cbankrate + .04) / 12
      hatch-loans 1 [
        set lender one-of banks
        set borrower myself
        set cost bondamount
        set remain bondamount
        set intrate interestrate
        set payment (intrate / 12) * bondamount
        set timeleft 60
        set kind "firmbonds"
        ask lender [
          set firmcredit firmcredit - bondamount
          set firmbonds firmbonds + bondamount
          set loanlist lput myself loanlist]
        ask borrower [
          set firmcredit firmcredit - bondamount
          set firmbonds firmbonds + bondamount
          set loanlist lput myself loanlist]]]
    ;pay dividends to hholds
    ask hholds [set dividends 0]

    if dividends > 0 [
      let tempdividends dividends
      let EPS tempdividends / 10000

      set currentaccount currentaccount - tempdividends

      ask hholds [
        set dividends dividends + (EPS * stockowned)
        set currentaccount currentaccount + (EPS * stockowned)]

      set dividends 0]

    if bankdividends > 0 [
      let tempdividends bankdividends
      let EPS tempdividends / 10000

      set currentaccount currentaccount - tempdividends

      ask hholds [
        set dividends dividends + (EPS * stockowned)
        set currentaccount currentaccount + (EPS * stockowned)]

      set bankdividends 0]]
end

to governments-quarterly
  ;government collects withhelds taxes from banks, households and firms
  ask governments[
    let firmtaxes sum [taxwithholdings] of firms
    let hholdtaxes sum [taxwithholdings] of hholds
    let banktaxes sum [taxwithholdings] of banks

    set taxescollected firmtaxes + hholdtaxes + banktaxes

    set currentaccount currentaccount + taxescollected

    set revenue taxescollected

    set fiscalspending fiscalspending + (.1 * (revenue - expenses))

    ask firms[
      set currentaccount currentaccount - taxwithholdings
      set taxwithholdings 0]

    ask banks[
      set currentaccount currentaccount - taxwithholdings
      set taxwithholdings 0]

    ask hholds[
      let hhtaxes taxwithholdings
      set hhdeposits hhdeposits - taxwithholdings
      ask banks [
          set hhdeposits hhdeposits - hhtaxes
          set capitalaccount capitalaccount - hhtaxes]
      set taxwithholdings 0]]

end

;MONTHLY ACTIONS
to banks-interact
  ask firms[
    set fbinterest 0
    set fcinterest 0]
  ask hholds[
    set hhcinterest 0]

  ask cbanks[
    set bbinterest 0
    set bdinterest 0]

  ask banks[

    set fbinterest 0
    set fcinterest 0
    set hhcinterest 0

    ;banks collect interest on bonds and loans
    let temploans turtle-set loanlist
    ask temploans with [kind = "firmbonds"][
      let tempamount payment
      ask borrower [
        set currentaccount currentaccount - tempamount
        set fbinterest fbinterest + tempamount]
      ask lender [
        set currentaccount currentaccount + tempamount
        set fbinterest fbinterest + tempamount]

      let tempremain remain
      if timeleft = 0 [;they cash the bond
        ask lender [
          set capitalaccount capitalaccount + tempremain
          set firmbonds firmbonds - tempremain
          set loanlist remove myself loanlist]
        ask borrower[
          set currentaccount currentaccount - tempremain
          set firmbonds firmbonds - tempremain
          set loanlist remove myself loanlist]
        die]

      set timeleft timeleft - 1]]

  ask firms [
    let cintamount firmcredit * ((cbankrate + .08) / 12)

    set currentaccount currentaccount - cintamount
    set fcinterest fcinterest + cintamount

    ask banks [
      set currentaccount currentaccount + cintamount
      set fcinterest fcinterest + cintamount]]

  ask hholds [
    let cintamount hhcredit * ((cbankrate + .12) / 12)

    set currentaccount currentaccount - cintamount
    set hhcinterest hhcinterest + cintamount

    ask banks [
      set currentaccount currentaccount + cintamount
      set hhcinterest hhcinterest + cintamount]]

  ; banks pay interest to depositors

  ask hholds [
    let tempinterest (cbankrate / 12) * hhdeposits
    set hhdinterest tempinterest
    set currentaccount currentaccount + tempinterest
    ask banks [
      set hhdinterest hhdinterest + tempinterest
      set currentaccount currentaccount - tempinterest]]

  ask banks[
    ;banks pay interest to CB
  let temploans turtle-set loanlist
    ask temploans with [kind = "bbonds"][
      let tempamount payment
      ask borrower [
        set currentaccount currentaccount - tempamount
        set bbinterest bbinterest + tempamount]
      ask lender [
        set currentaccount currentaccount + tempamount
        set bbinterest bbinterest + tempamount]

      let tempremain remain
      if timeleft = 0 [;they cash the bond
        ask lender [
          set currentaccount currentaccount + tempremain
          set bbonds bbonds - tempremain
          set loanlist remove myself loanlist]
        ask borrower[
          set currentaccount capitalaccount - tempremain
          set bbonds bbonds - tempremain
          set loanlist remove myself loanlist]
        die]

      set timeleft timeleft - 1]
    ;collect interest from CB deposits

    if capitalaccount > 0[
      let tempinterest capitalaccount * cbankrate

      ask one-of cbanks [
        set currentaccount currentaccount - tempinterest
        set bdinterest bdinterest + tempinterest]

      set currentaccount currentaccount - tempinterest
      set bdinterest bdinterest + tempinterest]

    ;banks withhold taxes
    set revenue fbinterest + fcinterest + hhcinterest + hhminterest + gbinterest + bdinterest + foreclosureproceeds
    set expenses hhdinterest + bbinterest + badloans
    set profit revenue - expenses

    set taxwithholdings corporatetaxrate * profit

    set bankdividends (1 - corporatetaxrate) * profit

    set fbinterest 0
    set fcinterest 0
    set hhcinterest 0
    set hhminterest 0
    set gbinterest 0
    set bdinterest 0
    set foreclosureproceeds 0
    set hhdinterest 0
    set bbinterest 0
    set badloans 0

    ;if there is a profit, banks pay profits to firms to be given as dividends
    ;banks will shore up inadequate funds be reinvesting profits first, and then taking CB loans if that isn't sufficient

    if currentaccount < 0 [
      set capitalaccount capitalaccount + currentaccount
      set currentaccount currentaccount - currentaccount]


    if capitalaccount < 0 [;use profits to shore up capital needs
      let capitalneeded -1 * capitalaccount

      if bankdividends > capitalneeded [
        set currentaccount currentaccount - capitalneeded
        set capitalaccount capitalaccount + capitalneeded
        set bankdividends bankdividends - capitalneeded]

      if bankdividends < capitalneeded [
        set currentaccount currentaccount - bankdividends
        set capitalaccount capitalaccount + bankdividends
        set bankdividends bankdividends - bankdividends]

      if capitalaccount < 0 [
        let tempborrower self
        let templender one-of cbanks
        let bondamount -1 * capitalaccount
        let interestrate (cbankrate / 12)
        hatch-loans 1 [
          set lender templender
          set borrower tempborrower
          set cost bondamount
          set remain bondamount
          set intrate interestrate
          set payment (intrate / 12) * bondamount
          set timeleft 0
          set kind "bbonds"
          ask lender [
            set currentaccount currentaccount - bondamount
            set bbonds bbonds + bondamount
            set loanlist lput myself loanlist]
          ask borrower [
            set capitalaccount capitalaccount + bondamount
            set bbonds bbonds + bondamount
            set loanlist lput myself loanlist]]]]
  ]


end

to government-interact
  ;collect CB profits
  ask cbanks [

    set revenue gbinterest + bbinterest
    set expenses bdinterest
    set profit revenue - expenses

    if profit > 0 [
      let tempprofit profit
      set currentaccount currentaccount - tempprofit
      ask governments [
        set cbprofits tempprofit
        set currentaccount tempprofit]]

    set gbinterest 0
    set bbinterest 0
    set bdinterest 0]

  ;spends fiscal to firms
  ask governments [
    let tempfiscal fiscalspending

    set currentaccount currentaccount - tempfiscal

    ask firms [
      set fiscalspending tempfiscal
      set currentaccount currentaccount + tempfiscal]

  ;pays bond interest to CB and banks
    set gbinterest 0
    ask banks [
      set gbinterest 0]
    ask cbanks [
      set gbinterest 0]

    let temploans turtle-set loanlist

    ask temploans with [kind = "gbonds"][
      let tempamount payment
      ask borrower [
        set currentaccount currentaccount - tempamount
        set gbinterest gbinterest + tempamount]
      ask lender [
        set currentaccount currentaccount + tempamount
        set gbinterest gbinterest + tempamount]

      let tempremain remain
      if timeleft = 0 [;they cash the bond
        ask lender [
          set currentaccount currentaccount - tempremain
          set gbonds gbonds - tempremain]
        ask borrower[
          set currentaccount currentaccount + tempremain
          set gbonds gbonds - tempremain]
        die]

      set timeleft timeleft - 1]

  ;covers deficit by releasing bonds to CB

    if currentaccount < 0[
      let tempborrower self
      let templender one-of cbanks
      let bondamount -1 * currentaccount
      let interestrate (cbankrate / 12)
      hatch-loans 1 [
        set lender templender
        set borrower tempborrower
        set cost bondamount
        set remain bondamount
        set intrate interestrate
        set payment (intrate / 12) * bondamount
        set timeleft 12
        set kind "gbonds"
        ask lender [
          set currentaccount currentaccount - bondamount
          set gbonds gbonds + bondamount
          set loanlist lput myself loanlist]
        ask borrower [
          set currentaccount currentaccount - bondamount
          set gbonds gbonds + bondamount
          set loanlist lput myself loanlist]]]]


end

to firms-interact
  ;firms calculate profits from last turn
  ask firms [
    set revenue fiscalspending + consumption
    set expenses fbinterest + fcinterest + wages
    set profit revenue - expenses

    set taxwithholdings profit * corporatetaxrate
    ;determine withholdings for taxes
    set dividends profit - taxwithholdings

    ;take out credit if needed
    if currentaccount < 0 [
      let creditneeded -1 * currentaccount

      set currentaccount currentaccount + creditneeded
      set firmcredit firmcredit + creditneeded

      ask banks [
        set firmcredit firmcredit + creditneeded
        set capitalaccount capitalaccount - creditneeded]]

  ;pay workers (this is start of new turn)
    let totalwages sum [wages] of hholds

    set wages totalwages
    set currentaccount currentaccount - totalwages

    ask hholds [
      set currentaccount currentaccount + wages]

    set consumption 0
    set fiscalspending 0
    set fbinterest 0
    set fcinterest 0]

end

to households-interact
  ask houses [
    let thishouse self
    set bidlist hholds with [currentbidhouse = thishouse]]

  ask hholds [

    if not any? houses with [occupant = myself][
      set status "homeless"]
  ;set desired consumption based on wages, wealth, and **networks**
    set consumption (.3 * income) + 600 + (.001 * wealth) + (((random-poisson 1) / 3) * income)
  ;buy consumption from the firm
    let tempconsumption consumption
    set currentaccount currentaccount - tempconsumption
    ask firms [
      set currentaccount currentaccount + tempconsumption
      set consumption consumption + tempconsumption]

    set rentincome 0

    set hhminterest 0
    set hhmpayment 0]
  ;pay rent to landlords
  ask houses with [status = "renter"][
    let temprent rentprice

    ask occupant[
      set currentaccount currentaccount - temprent
      set rentexpense temprent]
    ask owner[
      set currentaccount currentaccount + temprent
      set rentincome rentincome + temprent]]

  ask loans with [kind = "hhmortgage"][

    let tempamount payment
    let tempinterest remain * intrate
    let tempprinciple payment - tempinterest

    ifelse tempamount < (([currentaccount] of borrower) + ([capitalaccount] of borrower)) [
      ask borrower [
        set currentaccount currentaccount - tempamount
        set hhmortgages hhmortgages - tempprinciple
        set hhmpayment hhmpayment + tempamount
        set hhminterest hhminterest + tempinterest]
      ask lender [
        set currentaccount currentaccount + tempinterest
        set hhminterest hhminterest + tempinterest
        set capitalaccount capitalaccount + tempprinciple
        set hhmortgages hhmortgages - tempprinciple]

      set remain remain - tempprinciple

      let tempremain remain
      if timeleft = 0 [;they cash the bond
        ask lender [
          set currentaccount currentaccount + tempremain
          set hhminterest hhminterest + tempremain
          set loanlist remove myself loanlist]
        ask borrower[
          set currentaccount currentaccount - tempremain
          set hhminterest hhminterest + tempremain
          set loanlist remove myself loanlist]
        ask asset[
          set mortgage 0]
        die]

      set missedpayments 0
      set timeleft timeleft - 1][
      ifelse missedpayments > 3[;start forclosure
        if remain > [taxprice] of asset [
          let thishouse asset
          let tempbad remain

          ask asset [
            set forsale? true
            set foreclosed? true
            set foreclosedhomes foreclosedhomes + 1
            set askingprice tempbad
            set mortgage 0
            set owner 0
            set status "vacant"

            if occupant != 0 [
              ask occupant [
                set status "homeless"]]
            set occupant 0]

          ask lender [
            set badloans badloans + tempbad
            set hhmortgages hhmortgages - tempbad
            set loanlist remove myself loanlist]

          ask borrower [
            set houselist remove thishouse houselist
            set loanlist remove myself loanlist]

          die
      ]][;don't start forclosure
        set missedpayments missedpayments + 1]]]




  ;calculate withholdings for income, and property taxes
  ask hholds [
    let propertyvalues sum [taxprice] of (turtle-set houselist)
    let propertytax (propertyvalues * propertytaxrate) / 12 ; what the monthly portion for the tax would be

    set income (dividends / 3) + wages + rentincome + hhdinterest

    let taxableincome income - 1733.33 ; taxableincome less the standard deduction and personal deductions
    let incometax 0

    let capitalgainstaxrate 0

    if taxableincome >= 0 and taxableincome < 1554.25 [ ; monthly brackets based on 2017 income tax brackets for Federal taxes
      set incometax 0 + 0.1 * (taxableincome - 0)]

    if taxableincome >= 1554.25 and taxableincome < 6325 [
      set incometax 155.42 + 0.15 * (taxableincome - 1554.25)]

    if taxableincome >= 6325 and taxableincome < 12758.42 [
      set incometax 1104.17 + 0.25 * (taxableincome - 6325)
      set capitalgainstaxrate .15]

    if taxableincome >= 12758.42 and taxableincome < 19445.92 [
      set incometax 4293.75 + 0.28 * (taxableincome - 12758.42)
      set capitalgainstaxrate .15]

    if taxableincome >= 19445.92 and taxableincome < 34725 [
      set incometax 9738.58 + 0.33 * (taxableincome - 19445.92)
      set capitalgainstaxrate .15]

    if taxableincome >= 34725 and taxableincome < 39225 [
      set incometax 21197.83 + 0.35 * (taxableincome - 34725)
      set capitalgainstaxrate .15]

    if taxableincome >= 39225 [
      set incometax 34926.58 + 0.396 * (taxableincome - 39225)
      set capitalgainstaxrate .2]

    let capitalgainstaxes 0
    if capitalgains > 0 [
      set capitalgainstaxes capitalgainstaxrate * capitalgains] ; capital gains tax rate depends on income tax bracket

    set capitalgains 0

    set taxwithholdings propertytax + incometax + capitalgainstaxes

    set currentaccount currentaccount - taxwithholdings
    set hhdeposits hhdeposits + taxwithholdings

    ;set taxwithholdings taxwithholdings + (capitalgainstaxes * capitalgains)
    ;put taxwithholdings into deposits

    let tempmoney (currentaccount)
    ;pay off credit with leftover money
    ;transfer leftover money to savings in capital account

    if currentaccount > 0 [;pay off credit with leftover money
      if hhcredit > 0 [
        let amountowed hhcredit
        ifelse amountowed < tempmoney [;if the hhold can pay it off right away
          set tempmoney tempmoney - amountowed
          set currentaccount currentaccount - amountowed
          set hhcredit hhcredit - amountowed
          ask banks [
            set hhcredit hhcredit - amountowed
            set capitalaccount capitalaccount + amountowed]][ ;if the hhold can only pay part of it
          set amountowed tempmoney
          set tempmoney tempmoney - amountowed
          set currentaccount currentaccount - amountowed
          set hhcredit hhcredit - amountowed
          ask banks [
            set hhcredit hhcredit - amountowed
            set capitalaccount capitalaccount + amountowed]]]]

    ;transfer the rest to capitalaccount

    if currentaccount > 0 [
      set tempmoney currentaccount
      set currentaccount currentaccount - tempmoney
      set hhdeposits hhdeposits + tempmoney
      ask banks [
          set hhdeposits hhdeposits + tempmoney
          set capitalaccount capitalaccount + tempmoney]
      set capitalaccount capitalaccount + tempmoney]


    if currentaccount < 0 [;set credit higher (short term solution)
      let creditneeded -1 * currentaccount

      set currentaccount currentaccount + creditneeded
      set hhcredit hhcredit + creditneeded
      ask banks [
        set hhcredit hhcredit + creditneeded
        set capitalaccount capitalaccount - creditneeded]]

    if hhcredit > 0 [
      if capitalaccount > 0 [
        set tempmoney capitalaccount
        let amountowed hhcredit

        ifelse amountowed < tempmoney [;if the hhold can pay it off right away
          set capitalaccount capitalaccount - amountowed
          set hhdeposits hhdeposits - amountowed
          set hhcredit hhcredit - amountowed
          ask banks [
            set hhdeposits hhdeposits - amountowed
            set capitalaccount capitalaccount - amountowed
            set hhcredit hhcredit - amountowed
            set capitalaccount capitalaccount + amountowed]
          ][ ;if the hhold can only pay part of it
          set amountowed capitalaccount
          set capitalaccount capitalaccount - amountowed
          set hhdeposits hhdeposits - amountowed
          ask banks [
            set hhdeposits hhdeposits - amountowed
            set capitalaccount capitalaccount - amountowed
            set hhcredit hhcredit - amountowed
            set capitalaccount capitalaccount + amountowed]
          set hhcredit hhcredit - amountowed]]]

    if capitalaccount < 0 [
      let creditneeded -1 * capitalaccount

      set capitalaccount capitalaccount + creditneeded
      set hhdeposits hhdeposits + creditneeded
      set hhcredit hhcredit + creditneeded
      ask banks [
        set hhdeposits hhdeposits + creditneeded
        set capitalaccount capitalaccount + creditneeded
        set hhcredit hhcredit + creditneeded
        set capitalaccount capitalaccount - creditneeded]]


    ;hholds will raise their bid each month until they are the top bidder
    if currentbidhouse != 0 [

      if capitalaccount > 0 [
        ;;figure out how much they can afford 1) loan portion should be either the rest of the portion after paying downpayment or the most they can make payments on and 2) the current state of their capitalaccount
        let maxpayment income - expenses
        if maxpayment > .4 * income [set maxpayment .4 * income]

        let mortgagerate (cbankrate + .03) / 12
        let maxloan maxpayment / (mortgagerate * ((1 + mortgagerate) ^ 360) / (((1 + mortgagerate) ^ 360) - 1))

        if maxloan > (capitalaccount / min-dpay) [set maxloan (capitalaccount / min-dpay)]

        set maxaffordability maxloan + capitalaccount

        let tempmax maxaffordability

        let tempbidlist [bidlist] of currentbidhouse
        set tempbidlist sort-on [(- currentbid)] tempbidlist

        if first tempbidlist != self [ ;if hhold is not the highest bidder, they will try and increase bid based on their maxaffordability
          let currenthighbid max [currentbid] of (turtle-set tempbidlist)
          if tempmax > currenthighbid [
            set currentbid currenthighbid + ((tempmax - currenthighbid) * .2)]]]]]
end

to update-lorenz-and-gini
  let sorted-wealths sort [wealth] of hholds
  let total-wealth sum sorted-wealths
  let wealth-sum-so-far 0
  let index 0
  set gini-index-reserve 0
  set num-hholds count hholds
  set lorenz-points []
  repeat num-hholds [
    set wealth-sum-so-far (wealth-sum-so-far + item index sorted-wealths)
    set lorenz-points lput ((wealth-sum-so-far / total-wealth) * 100) lorenz-points
    set index (index + 1)
    set gini-index-reserve gini-index-reserve + (index / num-hholds) - (wealth-sum-so-far / total-wealth)]
end

to update-houses
  ask houses [
    set tenure tenure + 1
    if status = "vacant" [set color red]
    if status = "renter" [set color green]
    if status = "homeowner" [set color brown]

    set taxprice mean [taxprice] of (houses in-radius 3)
  ]
end

to-report wealth
  let mywealth capitalaccount

  if houselist != 0 [
    let myhouses turtle-set houselist
    set mywealth mywealth + sum [taxprice] of myhouses]
  report mywealth
end

to-report prestige
  let deedneighbors (list houses in-radius 4)
  let myprestige taxprice / 100000
  if empty? deedneighbors = false [foreach deedneighbors [deedneighbor ->
    ask deedneighbor[
        let myowner occupant
        if status = "vacant" [
          set myprestige myprestige - 1]
      if myowner != 0 [
        if [status] of myowner = "renter" [
          set myprestige myprestige + 0]
        if [status] of myowner = "homeowner" [
          set myprestige myprestige + 1]
        if [status] of myowner = "landlord" [
          set myprestige myprestige + 2]]]]]
  report myprestige
end
@#$#@#$#@
GRAPHICS-WINDOW
118
19
474
376
-1
-1
13.95122
1
10
1
1
1
0
0
0
1
-12
12
-12
12
1
1
1
ticks
30.0

BUTTON
18
24
85
57
NIL
set-up
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
717
16
804
61
NIL
count houses
17
1
11

MONITOR
808
16
891
61
NIL
count hholds
17
1
11

PLOT
718
67
918
217
Wealth Gini
Pop %
Wealth %
0.0
100.0
0.0
100.0
false
true
"" ""
PENS
"Lorenz" 1.0 0 -13791810 true "" "if count hholds > 0 [\nplot-pen-reset\nset-plot-pen-interval 100 / (num-hholds)\nplot 0\nforeach lorenz-points plot]"
"Equal" 100.0 0 -7500403 true "plot 0\nplot 100" ""

BUTTON
15
77
78
110
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

PLOT
718
220
918
370
Gini vs time
NIL
NIL
0.0
10.0
0.0
1.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "if count hholds > 0 [plot gini-index-reserve / num-hholds]"

BUTTON
16
128
79
161
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

PLOT
722
386
922
536
average wealth
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot mean [wealth] of hholds"

SLIDER
96
666
268
699
minconsumption
minconsumption
.01
.99
0.25
.01
1
NIL
HORIZONTAL

SLIDER
96
632
268
665
networkinfluence
networkinfluence
.01
.99
0.53
.01
1
NIL
HORIZONTAL

MONITOR
930
72
1096
117
NIL
mean [income] of hholds
17
1
11

SLIDER
269
632
441
665
minimumwage
minimumwage
7.25
20.00
7.25
.25
1
NIL
HORIZONTAL

MONITOR
930
124
1097
169
NIL
max [income] of hholds
17
1
11

MONITOR
928
23
1096
68
NIL
min [income] of hholds
17
1
11

SLIDER
923
304
1095
337
min-dpay
min-dpay
0
1
0.2
.01
1
NIL
HORIZONTAL

SLIDER
923
267
1102
300
max-payment-ratio
max-payment-ratio
0
1
0.14
.01
1
NIL
HORIZONTAL

SLIDER
923
341
1095
374
cbankrate
cbankrate
0
.15
0.0825
.0025
1
NIL
HORIZONTAL

SLIDER
924
378
1096
411
rentportion
rentportion
.001
.01
0.005
.001
1
NIL
HORIZONTAL

SLIDER
926
415
1098
448
corporatetaxrate
corporatetaxrate
0
1
0.35
.005
1
NIL
HORIZONTAL

SLIDER
924
227
1096
260
propertytaxrate
propertytaxrate
.0025
.0225
0.01
.0025
1
NIL
HORIZONTAL

PLOT
515
220
715
370
Average House Price vs Time
Time
Average House price
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot mean [price] of houses"

PLOT
515
67
715
217
Households by type
NIL
NIL
0.0
10.0
0.0
1.0
true
false
"" ""
PENS
"Homeowners" 1.0 0 -10402772 true "" "plot count hholds with [status = \"homeowner\"] / count hholds"
"Renters" 1.0 0 -13210332 true "" "plot count hholds with [status = \"renter\"] / count hholds"
"Homeless" 1.0 0 -2674135 true "" "plot count hholds with [status = \"homeless\"] / count hholds"
"Landlords" 1.0 0 -11783835 true "" "plot count hholds with [status = \"landlord\"] / count hholds"

SLIDER
927
453
1099
486
debttoincome
debttoincome
.01
1
0.4
.01
1
NIL
HORIZONTAL

@#$#@#$#@
## WHAT IS IT?

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.0.2
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="Interest Rate" repetitions="20" runMetricsEveryStep="true">
    <setup>set-up</setup>
    <go>go</go>
    <timeLimit steps="100"/>
    <metric>count hholds with [status = "landlord"] / count hholds</metric>
    <metric>count hholds with [status = "homeowner"] / count hholds</metric>
    <metric>count hholds with [status = "renter"] / count hholds</metric>
    <metric>count hholds with [status = "homeless"] / count hholds</metric>
    <metric>count houses with [status = "vacant"]</metric>
    <metric>mean [wealth] of hholds</metric>
    <metric>mean [taxprice] of houses</metric>
    <metric>mean [price] of houses</metric>
    <metric>count houses with [foreclosed? = true]</metric>
    <enumeratedValueSet variable="rentportion">
      <value value="0.005"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="debttoincome">
      <value value="0.4"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="min-dpay">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="propertytaxrate">
      <value value="0.01"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="cbankrate">
      <value value="0.0025"/>
      <value value="0.0125"/>
      <value value="0.0225"/>
      <value value="0.0325"/>
      <value value="0.0425"/>
      <value value="0.0525"/>
      <value value="0.0625"/>
      <value value="0.0725"/>
      <value value="0.0825"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="corporatetaxrate">
      <value value="0.35"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="Tax Rate" repetitions="20" runMetricsEveryStep="true">
    <setup>set-up</setup>
    <go>go</go>
    <timeLimit steps="100"/>
    <metric>count hholds with [landlord? = true] / count hholds</metric>
    <metric>count hholds with [homeowner? = true] / count hholds</metric>
    <metric>count hholds with [renter? = true] / count hholds</metric>
    <metric>count hholds with [homeless? = true] / count hholds</metric>
    <metric>count houses with [vacant? = true]</metric>
    <metric>mean [wealth] of hholds</metric>
    <metric>mean [taxprice] of houses</metric>
    <metric>mean [price] of houses</metric>
    <metric>count houses with [foreclosed? = true]</metric>
    <enumeratedValueSet variable="rentportion">
      <value value="0.005"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="debttoincome">
      <value value="0.4"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="min-dpay">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="propertytaxrate">
      <value value="0.0025"/>
      <value value="0.0075"/>
      <value value="0.0125"/>
      <value value="0.0175"/>
      <value value="0.0225"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="cbankrate">
      <value value="0.015"/>
      <value value="0.035"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="corporatetaxrate">
      <value value="0.35"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="Down Payment" repetitions="20" runMetricsEveryStep="true">
    <setup>set-up</setup>
    <go>go</go>
    <timeLimit steps="100"/>
    <metric>count hholds with [status = "landlord"] / count hholds</metric>
    <metric>count hholds with [status = "homeowner"] / count hholds</metric>
    <metric>count hholds with [status = "renter"] / count hholds</metric>
    <metric>count hholds with [status = "homeless"] / count hholds</metric>
    <metric>count houses with [status = "vacant"]</metric>
    <metric>mean [wealth] of hholds</metric>
    <metric>mean [taxprice] of houses</metric>
    <metric>mean [price] of houses</metric>
    <metric>count houses with [foreclosed? = true]</metric>
    <enumeratedValueSet variable="rentportion">
      <value value="0.005"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="debttoincome">
      <value value="0.4"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="min-dpay">
      <value value="0.05"/>
      <value value="0.1"/>
      <value value="0.15"/>
      <value value="0.2"/>
      <value value="0.25"/>
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="propertytaxrate">
      <value value="0.01"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="cbankrate">
      <value value="0.0125"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="corporatetaxrate">
      <value value="0.35"/>
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
