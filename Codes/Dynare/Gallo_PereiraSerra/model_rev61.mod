	
  % VARIABLES
var 

Y,                                                                   % output (everything in real terms)
Cr,                                                                  % rentier consumption 
Cw,                                                                  % worker consumption 
wp,                                                                  % real wage
L,                                                                   % employment level
Nw,                                                                  % worker labor supply
I,                                                                   % investment
Mr,                                                                  % deposits
Mf,                                                                  % steady-state firms’ deposits
B,                                                                   % bank profits
Z,                                                                   % firms profits
Zr,                                                                  % rentier income
Zf,                                                                  % profits saved as deposits
rm,                                                                  % interest rate on deposits
Pip,                                                                 % price gross inflation
A,                                                                   % steady-state inventories
rd,                                                                  % steady-state interest on firms’ debt
K,                                                                   % capital stock
varphi,                                                              % unit labor cost
Piw,                                                                 % nominal wage gross inflation
u,                                                                   % unemployment rate
nu,                                                                  % worker's relative bargaining power 
D,                                                                   % firms' debt
Piwe,                                                                % expected gross price inflation rate
xi,																	 % share of investment financed by new loans
Ye,                                                                  % expected sales, i.e. expected output
Va, Vr, Vc, Vn, Vi, Vnu, Vinv,                                       % autoregressive shock processes
devlnY, devlnC, devlnI, devR, devPip, devlnA, devu;                  % observed variables

  % EXOGENOUS DISTURBANCES
varexo ea, ec, er, en, ei, enu, einv;

  % MODEL PARAMETERS
parameters 

Gama, pssi, alfa, epsilon, delta, Pipbar, Kbar, teta, %phic,
Ybar, Crbar, Cwbar, rmbar, Piwbar, Nwbar, nubar, Abar, varphibar, bheta, rdbar, ubar, phiphipiw, phicz, phicb, phicm, 
phixid, phiximf, phixird, phiim, phiid, phiir, phiivarphi, phiiy, phirpi, phiry, phinul, 
rhoa, rhor, rhoc, rhon, rhoi, rhonu, rhoinv, wpd, phiya, 
phipipe, phiye;

  % CALIBRATED 
Gama           = 1.006;                                             % deterministic growth rate of the economy (all assuming that a period is one quarter)
pssi           = 0.1;                                               % fixed output-capital ratio
alfa           = 0.35;                                               % capital elasticity of output
epsilon        = 0.01;                                               % price mark-up
delta          = 0.014;                                             % capital depreciation rate
Ybar           = 1;                                                 % long-run output (will be normalized to 1 by the aid of an appropriate restriction on Vc, see below)                                  
Abar           = 0.106;                                             % long-run steady-state inventories
varphibar 	   = 1/(1+epsilon);										% long-run unit labor cost
bheta 		   = 0.92;                                              % fraction of profits to rentier households
rmbar          = 0.0065;                                            % long-run gross interest rate  (rdbar=0.014)
teta 		   = 1.15;												% loans mark-up on deposits interest rate
rdbar          = (1+teta)*rmbar;                                    % long-run gross interest rate on firms’ debt
Piwbar         = 1.007; %1.007;                                     % long-run gross wage inflation rate (target by the central bank) [assuming 3% annual target] 
Pipbar         = Piwbar;                                            % long-run gross inflation rate (target by the central bank) [
ubar           = 0.043;                                             % long-run unemployment rate (FOMC Projection March 20, 2019)
Kbar           = Ybar/pssi;                                         % long-run capital stock
Nwbar          = (Ybar*pssi^(alfa/(1-alfa)))/(1-ubar);                                     % long-run labor supply; Nwbar such that u_ss=ubar using definition of unemployment and production function
Cwbar          = (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa)));                                        % long-run worker consumption; which uses Cwbar=wp_ss*L_ss 
Crbar          = Ybar-Cwbar-Kbar*(1-(1-delta)/Gama)-(Abar*(1-1/(Pipbar*Gama)));       	% long-run rentier consumption; which uses Y_ss=Cr_ss+Cw_ss+I_ss+G_ss
nubar          = 0.5;                                               % workers bargaing power
wpd            = (Piwbar-1)/nubar+(1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)));                       % long-run desired wage rate											 
																	 
phiximf        = 4.7;
phixid         = 4.7;												% calibrated to be compatible with Dbar = 2.00


% ESTIMATED (calibration will be overwritten during estimation procedure)

phixird        = 1;
phiphipiw      = 1;
                                               % wage inflation elasticity of the markup (equation 7)
%phic          = 0.5;                                               % income elasticity of rentier consumption
phicz          = 0.5;                                               % income elasticity of rentier consumption to firms' profits-deposit ratio
phicb          = 0.5;                                               % income elasticity of rentier consumption to banks' profits-deposit ratio
phicm          = 0.5;                                               % income elasticity of rentier consumption to deposits dynamics

phiim          = 0.5;                                               % elasticity of firms' deposits to investment 
phiid          = 0.5;                                               % elasticity of firms’ debt to investment 
phiir          = 0.5;                                               % elasticity of interest on firms’ debt to investment 
phiivarphi     = 0.5;                                               % elasticity of unit labor cost  to investment 
phiiy          = 0.5; 
                                              % expected sales elasticity of investment
phirpi         = 1;                                                 % inflation elasticity of the interest rate
phiry          = 1;                                                 % output elasticity of the interest rate
phinul         = 1;                                                 % employment elasticity of the workers' bargaining power
rhoa 	       = 0.5;                                               % autoregressive coeffiecient for shock process
rhoc 	       = 0.5;                                               % autoregressive coeffiecient for shock process
rhor           = 0.5;                                               % autoregressive coeffiecient for shock process
rhon           = 0.5;                                               % autoregressive coeffiecient for shock process
rhoi           = 0.5;                                               % autoregressive coeffiecient for shock process
rhonu          = 0.5;                                               % autoregressive coeffiecient for shock process
rhoinv         = 0.5;                                               % autoregressive coeffiecient for shock process
phipipe        = 0.5;                                               % stickiness of expectations
phiye          = 0.5;                                               % stickiness of expectations
phiya 		   = 0.05;												% elasticity of inventories to output

model;
# xibar 	   = (1/(Pipbar*Gama))^(-phiximf - phixid)-1;
# Ibar		   = Kbar*(1-(1-delta)/Gama);							% long-run investment 
# Lbar           = Ybar*pssi^(alfa/(1-alfa));                         % long-run labor demand; which uses u_ss=1-L_ss/Nw_ss
# wpbar = (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)));
# Dbar		   = ((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama));					% long-run steady-state firms’ debt
# Zbar 		   = (Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)));
# Zrbar 		   = bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama))));
# Zfbar 		   = (1-bheta)*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama))));
# Mfbar		   = Zfbar/(1-1/(Pipbar*Gama));							% long-run steady-state firms’ deposits
# Mrbar		   = (Zrbar-Crbar+(rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama)-(rmbar*Mfbar)/(Pipbar*Gama))/(1-1/(Pipbar*Gama));	 % long-run deposits of rentier households
# Bbar           = (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))) - (rmbar*(Mfbar+Mrbar)))/(Pipbar*Gama);
# Vcbar = (Ybar - Cwbar - Kbar*(1-(1-delta)/Gama)-Abar*(1-1/(Pipbar*Gama))) / ((bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))^phicz * ((rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))) - (rmbar*(Mfbar+Mrbar)))/(Pipbar*Gama))^phicb * Mrbar^(1-phicz-phicb) * ((1+rmbar)/(Pipbar*Gama))^phicm);


%Vcbar such that Y_ss=1 using Y_ss-(Zr_ss)^phic*Br_ss^(1-phic)-Cw_ss-I_ss-Gbar=0 


  % WORKER HOUSEHOLDS
Cw=wp*L;                                                             % eq. (1)  
Nw/Nwbar = Vn;                                                       % eq. (2)        
  
    % RENTIER HOUSEHOLDSF
Mr + Cr = Zr + B + (1+rm(-1))/Pip*(Mr(-1)/Gama);	               	 % eq. (3)
Cr/Mrbar = ((Zr/Mrbar)^phicz)*((B/Mrbar)^phicb)*((((1+rm(-1))/Pip)*(Mr(-1)/(Mrbar*Gama)))^phicm) * Vc;    
																	 % eq. (4)

  % FIRMS
L = Y/(Va)^(1/(1-alfa))*pssi^(alfa/(1-alfa));                        % eq. (5)
varphi = (wp/Va)*(1/(1-alfa))*(pssi/Va)^(alfa/(1-alfa));             % eq. (6)
1 = (1+epsilon)*(Piwe/Piwbar)^(-phiphipiw)*varphi;                   % eq. (7)
I/Kbar=(1-(1-delta)/Gama)*((Ye/Ybar)^phiiy)*((Mf(-1)/(Zfbar/(1-1/(Pipbar*Gama))))^(phiim))*((D(-1)/Dbar)^(-phiid))*((rd/rdbar)^(-phiir))*((varphi/varphibar)^(-phiivarphi)) * Vi;          			       % eq. (8)
K = (1-delta)*1/Gama*K(-1) + I;                        			     % eq. (9)                        
Z = Y - wp*L - (1-xi)*I-rd(-1)/(Pip*Gama)*D(-1) + (rm(-1))/(Pip*Gama)*Mf(-1) - (A - A(-1)*Vinv/(Pip*Gama));
																	 % eq. (10)
xi = ((Mf(-1)/(Pip*Gama))/(Zfbar/(1-1/(Pipbar*Gama))))^(-phiximf)*((D(-1)/(Pip*Gama)/Dbar))^(-phixid)*((rd)/rdbar)^(-phixird)-1;
																	 % eq. (11)
D - D(-1)/(Pip*Gama) = xi*I;										 % eq. (12)


  % COMMERCIAL BANKS

B = ((rd(-1))*D(-1))/(Pip * Gama)- ((rm(-1))*(Mr(-1)+Mf(-1)))/(Pip*Gama);% eq. (13)
rd = (1+teta)*rm;													 % eq. (14)

  % CENTRAL BANK
rm/rmbar = (Pip/Piwbar)^phirpi*(Y/Ybar)^phiry*Vr;                    % eq. (15)

  % LABOR MARKET
Piw=nu*(wpd-wp(-1))+1;                                               % eq. (16)
nu/nubar = (L/Lbar)^phinul*Vnu;	                                     % eq. (17)

  % MACROECONOMIC BALANCE CONDITION
A = Y - Cr - Cw - I + A(-1)*Vinv/(Pip*Gama);                         % eq.(18)                                                        
Y=Ye*(A(-1)/Abar)^(-phiya);											 % eq.(19)

  % MISC
Zr = bheta * Z;                                        			     % eq. (20)
Mf - (Mf(-1))/(Pip*Gama) = Zf;                                       % eq. (21)
Zf = (1-bheta)*Z;                                         		     % eq. (22)
u = 1 - L/Nw;                                                        % eq. (23)
wp/wp(-1)-1 = Piw - Pip;                                             % eq. (24)                                                           

  % EXPECTATIONS
Piwe/Piw = (Piwe(-1)/Piw)^phipipe;                                   % eq. (25)
Ye/Y = (Ye(-1)/Y)^phiye;	                            			 % eq. (26)

  % SHOCK PROCESSES
Va = Va(-1)^rhoa*exp(ea);                                            % eq. (27)                                              
Vr = Vr(-1)^rhor*exp(er);                                            % eq. (28)
Vc/Vcbar = (Vc(-1)/Vcbar)^(rhoc)*exp(ec);                       	 % eq. (29)
Vn = Vn(-1)^rhon*exp(en);                                            % eq. (30)
Vi = Vi(-1)^rhoi*exp(ei);                                            % eq. (31)
Vnu = Vnu(-1)^rhonu*exp(enu);                                        % eq. (32)
Vinv = Vinv(-1)^rhoinv*exp(einv);                                    % eq. (33)

  % MEASUREMENT EQUATIONS  
devlnY = log(Y/Ybar)*100;                                            % eq. (34)
devlnC = log((Cr+Cw)/(Crbar+Cwbar))*100;                             % eq. (35)
devlnI = log(I/Ibar)*100;                                            % eq. (36) 
devR= (rm-rmbar)*100;                                                % eq. (40)
devPip = (Pip-Pipbar)*100;                                           % eq. (37)
devlnA = log(A/Abar)*100;                                            % eq. (38)
devu = (u-ubar)*100;                                                 % eq. (39)
end;

steady_state_model;

nu_ss=nubar;
Nw_ss=Nwbar;
rm_ss=rmbar;
Piw_ss=Piwbar;
Pip_ss=Pipbar;
%xi_ss=(1/(Pipbar*Gama))^(-phiximf - phixid)-1;
u_ss=ubar;
Y_ss=Ybar;
K_ss=Y_ss/pssi;
varphi_ss=varphibar;
wp_ss=varphi_ss*(1-alfa)*pssi^(-alfa/(1-alfa));
Cw_ss=Cwbar;
Cr_ss=Crbar;
rd_ss = (1+teta) * rmbar;

Y=Y_ss;
Cr=Cr_ss;
Cw=Cw_ss;
Nw=Nw_ss;
u=u_ss;
varphi=varphi_ss;
Pip=Pip_ss;
Piw=Piw_ss;
nu=nu_ss;
Piwe=Pip_ss;
Ye=Y_ss;
A_ss=Abar;
rd=rd_ss;
rm=rm_ss;
A=A_ss;
K=K_ss;

Va=1;
Vn=1;
Vi=1;
Vr=1;
Vnu=1;
Vinv=1;

Vc = (Ybar - Cwbar - Kbar*(1-(1-delta)/Gama)-Abar*(1-1/(Pipbar*Gama))) / ((bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))^phicz * ((rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))) - (rmbar*((((1-bheta)*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))/(1-1/(Pipbar*Gama))+ ((bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))-Crbar+(rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama)-(rmbar*((1-bheta)*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))/(1-1/(Pipbar*Gama)))/(Pipbar*Gama))/(1-1/(Pipbar*Gama))))))/(Pipbar*Gama))^phicb * (((bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))-Crbar+(rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama)-(rmbar*(((1-bheta)*(Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama))))/(1-1/(Pipbar*Gama))))/(Pipbar*Gama))/(1-1/(Pipbar*Gama)))^(1-phicz-phicb) * ((1+rmbar)/(Pipbar*Gama))^phicm);

%Vc= (Ybar - Cwbar - Kbar*(1-(1-delta)/Gama)-Abar*(1-1/(Pipbar*Gama))) / ((bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))^phicz * ((rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))) - (rmbar*((((1-bheta)*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))/(1-1/(Pipbar*Gama)))+(((bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))-Crbar+(rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama)-(rmbar*(Zfbar/(1-1/(Pipbar*Gama))))/(Pipbar*Gama))/(1-1/(Pipbar*Gama))))))/(Pipbar*Gama))^phicb * (((bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))-Crbar+(rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama)-(rmbar*(Zfbar/(1-1/(Pipbar*Gama))))/(Pipbar*Gama))/(1-1/(Pipbar*Gama)))^(1-phicz-phicb) * ((1+rmbar)/(Pipbar*Gama))^phicm);

I = Kbar*(1-(1-delta)/Gama);

xi = (1/(Pipbar*Gama))^(-phiximf - phixid)-1;

L = Ybar*pssi^(alfa/(1-alfa));

wp= (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)));

D   = ((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama));					% long-run steady-state firms’ debt;
Z 		   = (Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)));
Zr 		   = bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama))));
Zf 		   = (1-bheta)*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama))));
Mf		   = ((1-bheta)*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))/(1-1/(Pipbar*Gama));

Mr		   = ((bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))-Crbar+(rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama)-(rmbar*(((1-bheta)*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))/(1-1/(Pipbar*Gama))))/(Pipbar*Gama))/(1-1/(Pipbar*Gama));	

B = (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))) - (rmbar*((((1-bheta)*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))/(1-1/(Pipbar*Gama)) + ((bheta*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))-Crbar+(rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama)-(rmbar*(((1-bheta)*((Ybar - (1/(1+epsilon))*(1-alfa)/(pssi^(alfa/(1-alfa)))*(Ybar*pssi^(alfa/(1-alfa))) - (1-((1/(Pipbar*Gama))^(-phiximf - phixid)-1))*Kbar*(1-(1-delta)/Gama) - (rdbar*(((1/(Pipbar*Gama))^(-phiximf - phixid)-1)*Kbar*(1-(1-delta)/Gama)/(1-1/(Pipbar*Gama))))/(Pipbar*Gama) - Abar*(1-1/(Pipbar*Gama)))/(1-rmbar/(Pipbar*Gama)*(1-bheta)/(1-1/(Pipbar*Gama)))))/(1-1/(Pipbar*Gama))))/(Pipbar*Gama))/(1-1/(Pipbar*Gama))))))/(Pipbar*Gama);

devlnY=0; 
devlnC=0; 
devlnI=0; 
devR=0;
devPip=0;
devlnA=0;
devu=0;
end;

steady(solve_algo=2,maxit=2000);

%steady;
resid(1);
check; 

model_diagnostics; 

shocks;
var ea; stderr 0.01;
var er; stderr 0.01;
var ec; stderr 0.01;
var en; stderr 0.01;
var ei; stderr 0.01;
var enu; stderr 0.01;
var einv; stderr 0.01;
end;

stoch_simul(order=1,irf=40,nodisplay) devlnY devlnC devlnI devR devPip devlnA devu;

%/*
  % ESTIMATION

%varobs devlnC devlnI devR devPip devu;
varobs devlnC devlnI devlnY devR devPip devu;


estimated_params;
%phiximf,         uniform_pdf,           ,      ,      1.7,    7.7;
%phixid,          uniform_pdf,           ,      ,      2.7,    6.7;
phixird,          gamma_pdf,             1,     0.5;

phiphipiw,        gamma_pdf,             1,     0.5;

phicz,            beta_pdf,              0.5,   0.2;
phicb,            beta_pdf,              0.5,   0.2;
phicm,            beta_pdf,              0.5,   0.2;

phiim,            uniform_pdf,           ,      ,      0,   1;
phiiy,            uniform_pdf,           ,      ,      0,   1;
phiivarphi,       uniform_pdf,           ,      ,      0,   1;
phiir,            uniform_pdf,           ,      ,      0,   1;
phiid,            uniform_pdf,           ,      ,      0,   1;

phiya,      	  uniform_pdf,           ,      ,      0,   0.1;

%% OK 
phirpi,           gamma_pdf,             1,     0.5;
phiry,            gamma_pdf,             1,     0.5;

phinul,           gamma_pdf,             1,     0.5;

%%% OK 
phipipe,          beta_pdf,              0.5,   0.2;
phiye,            beta_pdf,              0.5,   0.2;
rhoa,             beta_pdf,              0.5,   0.2;
rhoc,             beta_pdf,              0.5,   0.2;
rhor,             beta_pdf,              0.5,   0.2;
rhon,             beta_pdf,              0.5,   0.2;
rhoi,             beta_pdf,              0.5,   0.2;
rhonu,            beta_pdf,              0.5,   0.2;
rhoinv,           beta_pdf,              0.5,   0.2;
stderr ea,        inv_gamma_pdf,         0.01,  0.05;
stderr er,        inv_gamma_pdf,         0.01,  0.05;
stderr ec,        inv_gamma_pdf,         0.01,  0.05;
stderr en,        inv_gamma_pdf,         0.01,  0.05;
stderr ei,        inv_gamma_pdf,         0.01,  0.05;
stderr enu,       inv_gamma_pdf,         0.01,  0.05;

end;

%identification(ar=1);

%identification(advanced=1,max_dim_cova_group=3);

    write_latex_dynamic_model;
    write_latex_parameter_table;
    write_latex_definitions;

%estimation(datafile=data_1,mode_check,bayesian_irf) devlnC devlnI devR devPip devlnA devu;

%estimation(datafile=data_2,first_obs=40,presample=4,mode_compute=6,mh_replic=50000,mh_nblocks=2,mh_jscale=0.5,nodisplay,mode_check,bayesian_irf) devlnY devlnC devlnI devR devPip devlnA devu;
%estimation(datafile=data_ea,first_obs=40,presample=4,mode_compute=6,mh_replic=50000,mh_nblocks=2,mh_jscale=0.5,nodisplay,mode_check,bayesian_irf) devlnY devlnC devlnI devR devPip devlnA devu;

prior simulate;

options_.TeX=1 
stoch_simul(conditional_variance_decomposition=[1 4]) devlnY devlnC devlnI devR devPip devlnA devu;

%shock_decomposition devlnY devlnC devlnI devR devPip devlnA devu;
%*/

