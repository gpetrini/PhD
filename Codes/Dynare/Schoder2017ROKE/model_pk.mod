% Estimating Keynesian models of business fluctuations using Bayesian Maximum Likelihood
% Christian Schoder
% November 2016

% This file replicates the estimation results for specification 1 in Schoder (2017 ROKE).

  % VARIABLES
var 
Y,                                                                   % output (everything in real terms)
Cr,                                                                  % rentier consumption 
Cw,                                                                  % worker consumption 
I,                                                                   % investment
G,                                                                   % government consumption
T,                                                                   % lump-sum taxes
Br,                                                                  % rentier wealth
Zr,                                                                  % rentier income
Nw,                                                                  % worker labor supply
L,                                                                   % firm labor demand
wp,                                                                  % real wage
varphi,                                                              % marginal costs=average variable costs
K,                                                                   % capital stock
Pip,                                                                 % price gross inflation
Piw,                                                                 % nominal wage gross inflation
u,                                                                   % unemployment rate
R,                                                                   % gross interest rate
nu,                                                                  % worker's relative bargaining power 
Dg,                                                                  % public debt
Piwe,                                                                % expected gross price inflation rate
Ye,                                                                  % expected sales, i.e. expected output
Va, Vg, Vr, Vc, Vn, Vi, Vnu,                                         % autoregressive shock processes
devlnY, devlnC, devlnI, devR, devPip, devPiw, devu;                  % observed variables

  % EXOGENOUS DISTURBANCES
varexo eg, ea, er, ec, en, ei, enu;

  % MODEL PARAMETERS
parameters 
Gama, pssi, alfa, epsilon, delta, xi, tc, tz, tw, 
Ybar, Crbar, Cwbar, Ibar, Gbar, Rbar, Piwbar, Nwbar, Kbar, nubar, Dgbar, Brbar, ubar, Lbar,
phiphipiw, phic, phiiy, phiir, phigy, phirpi, phiry, phinul, 
rhog, rhoa, rhor, rhoc, rhon, rhoi, rhonu, rhopipe, rhoye;

  % CALIBRATED 
Gama           = 1.0042;                                             % deterministic growth rate of the economy (all assuming that a period is one quarter)
pssi           = 0.1;                                                % fixed output-capital ratio
alfa           = 0.25;                                               % capital elasticity of output
epsilon        = 0.35;                                               % price mark-up
delta          = 0.025;                                              % capital depreciation rate
xi             = 0.2;                                                % the share of investment funded by new debt; 1-xi is the share of investment funded by retained earnings
tc             = 0.15;                                               % consumption tax rate
tz             = 0.15;                                               % distributed profit income tax rate
Ybar           = 1;                                                  % long-run output (will be normalized to 1 by the aid of an appropriate restriction on Vc, see below)                                  
Gbar           = 0.2;                                                % long-run government consumption
Rbar           = 1.007;                                              % long-run gross interest rate
Piwbar         = 1.005;                                              % long-run gross inflation rate (target by the central bank)
ubar           = 0.091;                                              % long-run unemployment rate
Dgbar          = 2.4;                                                % long-run public debt
Kbar           = Ybar/pssi;                                          % long-run capital stock
Ibar           = (1-(1-delta)*1/Gama)*Kbar;                          % long-run investment
Nwbar          = ((pssi^alfa*Ybar^(1-alfa))^(1/(1-alfa)))/(1-ubar);  % long-run labor supply; Nwbar such that u_ss=ubar using definition of unemployment and production function
Lbar           = (1-ubar)*Nwbar;                                     % long-run labor demand; which uses u_ss=1-L_ss/Nw_ss
nubar          = (1/(1-( ((Rbar*(((0 + (-1 + delta)*(1 + epsilon))*Piwbar + Rbar + epsilon*Rbar)/(alfa*Piwbar))^(1/(-1 + alfa)))/Piwbar^2) * ((1/(alfa*(1 + epsilon)*Piwbar))*(((-1 + delta)*epsilon^2 - alfa*Gama + alfa*(-1 + delta + Gama)*xi + epsilon*(-1 + 0 - alfa*0 + delta - alfa*Gama + alfa*(-1 + delta + Gama)*xi))*Piwbar + (1 + epsilon)*(alfa + epsilon)*Rbar)) )/( (-(((alfa + epsilon)*Rbar)/(alfa*Piwbar^2))) * (-(((-1 + alfa)*(((0 + (-1 + delta)*(1 + epsilon))*Piwbar + Rbar + epsilon*Rbar)/(alfa*Piwbar))^(alfa/(-1 + alfa)))/(1 + epsilon))) )));
                                                                     % long-run workers' bargaining power; nubar is such that Piwbar_ss is equal to Piwbar at Rbar using equation (14) in the paper evaluated at the steady state: [nubar = 1/(1-(Dw*p)/(Dp*w))] 
tw             = (Gbar+(Rbar/Piwbar*1/Gama-1)*Dgbar - tz*(Ybar-1/(1+epsilon)*(1-alfa)*(pssi)^(-alfa/(1-alfa))*Lbar-(1-xi)*Ibar) - tc*(Ybar-Ibar-Gbar))/(1/(1+epsilon)*(1-alfa)*(pssi)^(-alfa/(1-alfa))*Lbar);  
                                                                     % labor income tax rate; tw is such that the structural government budget is balanced, i.e. tw*wp_ss*L_ss+tz*Zr_ss+tc*(Cr_ss+Cw_ss)=Gbar+(Rbar/Piwbar*1/Gama-1)*Dgbar using Cr_ss+Cw_ss=Y_ss-I_ss-G_ss
Cwbar          = (1-tw)/(1+tc)*1/(1+epsilon)*(1-alfa)*(pssi)^(-alfa/(1-alfa))*Lbar;
                                                                     % long-run worker consumption; which uses (1+tc)*Cwbar=(1-tw)*wp_ss*L_ss 
Crbar          = Ybar-Cwbar-Ibar-Gbar;                               % long-run rentier consumption; which uses Y_ss=Cr_ss+Cw_ss+I_ss+G_ss
Brbar          = 1/(1-Rbar/Piwbar*1/Gama)*((1-tz)*(Ybar-1/(1+epsilon)*(1-alfa)*(pssi)^(-alfa/(1-alfa))*Lbar-(1-xi)*Ibar)-(1+tc)*Crbar);
                                                                     % long-run rentier wealth; which uses equation (2) and (17) evaluated at the steady state

% ESTIMATED (calibration will be overwritten during estimation procedure)
phiphipiw      = 1;                                                  % wage inflation elasticity of the markup (equation 7)
phic           = 0.5;                                                % income elasticity of rentier consumption
phiiy          = 1;                                                  % expected sales elasticity of investment
phiir          = 1;                                                  % (negative) interest rate elasticity of investment
phigy          = 0;                                                  % output elasticity of government consumption
phirpi         = 0;                                                  % inflation elasticity of the interest rate
phiry          = 0;                                                  % output elasticity of the interest rate
phinul         = 0;                                                  % employment elasticity of the workers' bargaining power
rhog           = 0.5;                                                % autoregressive coeffiecient for shock process
rhoa 	       = 0.5;                                                % autoregressive coeffiecient for shock process
rhor           = 0.5;                                                % autoregressive coeffiecient for shock process
rhoc           = 0.5;                                                % autoregressive coeffiecient for shock process
rhon           = 0.5;                                                % autoregressive coeffiecient for shock process
rhoi           = 0.5;                                                % autoregressive coeffiecient for shock process
rhonu          = 0.5;                                                % autoregressive coeffiecient for shock process
rhopipe        = 0.5;                                                % stickiness of expectations
rhoye          = 0.5;                                                % stickiness of expectations

model;

# Vcbar = (Ybar - Cwbar - Ibar - Gbar) / (((1-tz)*(Ybar-1/(1+epsilon)*(1-alfa)*(pssi)^(-alfa/(1-alfa))*Lbar-(1-xi)*Ibar))^phic*(Brbar)^(1-phic));
                                                                     %Vcbar such that Y_ss=1 using Y_ss-((1-tz)*Zr_ss)^phic*Br_ss^(1-phic)-Cw_ss-I_ss-Gbar=0 

  % RENTIER HOUSEHOLDS
Cr/Brbar = ((1-tz)*Zr/Brbar)^phic*Vc;                                % eq. (1)
(1+tc)*Cr + Br = (1-tz)*Zr + R(-1)/Pip*1/Gama*Br(-1);                % eq. (2)

  % WORKER HOUSEHOLDS
(1+tc)*Cw = (1-tw)*wp*L;                                             % eq. (3)                                                                       
Nw/Nwbar = Vn;                                                       % eq. (4)        
  
  % FIRMS
1 = Va*(L/Y)^(1-alfa)*(1/pssi)^(alfa);                               % eq. (5)
varphi = wp*1/Va*1/(1-alfa)*(pssi*1/Va)^(alfa/(1-alfa));             % eq. (6)
1 = (1+epsilon)*(Piwe/Piwbar)^(-phiphipiw)*varphi;                   % eq. (7)
I/Kbar = (1-(1-delta)*1/Gama)*(Ye/Ybar)^phiiy*(R/Rbar)^(-phiir)*Vi;  % eq. (8)
K = (1-delta)*1/Gama*K(-1) + I;                                      % eq. (9)

  % GOVERNMENT
T = tw*wp*L + tz*Zr + tc*(Cr+Cw);                                    % eq. (10)
G/Gbar = (Y/Ybar)^phigy*Vg;                                          % eq. (11)
Dg = G - T + R(-1)/Pip*1/Gama*Dg(-1);                                % eq. (12)

  % CENTRAL BANK
R/Rbar = (Pip/Piwbar)^phirpi*(Y/Ybar)^phiry*Vr;                      % eq. (13)

  % LABOR MARKET
0 = 1 + ((-1 + alfa)*(-1 + nu)*(alfa + epsilon)*(((-1 + delta)*(1 + epsilon))*Piw + Rbar + epsilon*Rbar))/(alfa*nu*((epsilon - delta*epsilon + epsilon^2 - delta*epsilon^2 + alfa*Gama + alfa*epsilon*Gama - alfa*(1 + epsilon)*(-1 + delta + Gama)*xi)*Piw - (1 + epsilon)*(alfa + epsilon)*Rbar));
                                                                     % eq. (14)
nu/nubar = (L/Lbar)^phinul*Vnu;	                                     % eq. (15)

  % MACROECONOMIC BALANCE CONDITION
Y = Cr + Cw + I + G;                                                 % eq. (16)                                                                      

  % MISC
Zr = Y - wp*L - (1-xi)*I;                                            % eq. (17)
u = 1 - L/Nw;                                                        % eq. (18)
wp/wp(-1)-1 = Piw - Pip;                                             % eq. (19)                                                            

  % EXPECTATIONS
Piwe/Piw = (Piwe(-1)/Piw)^rhopipe;                                   % eq. (20)
Ye/Y = (Ye(-1)/Y)^rhoye;                                             % eq. (21)

  % SHOCK PROCESSES
Vg = Vg(-1)^rhog*exp(eg);                                            % eq. (22)
Va = Va(-1)^rhoa*exp(ea);                                            % eq. (23)                                              
Vr = Vr(-1)^rhor*exp(er);                                            % eq. (24)
Vc/Vcbar = (Vc(-1)/Vcbar)^(rhoc)*exp(ec);                            % eq. (25)
Vn = Vn(-1)^rhon*exp(en);                                            % eq. (26)
Vi = Vi(-1)^rhoi*exp(ei);                                            % eq. (27)
Vnu = Vnu(-1)^rhonu*exp(enu);                                        % eq. (28)

  % MEASUREMENT EQUATIONS
devlnY = log(Y/Ybar)*100;                                            % eq. (29)
devlnC = log((Cr+Cw)/(Crbar+Cwbar))*100;                             % eq. (30)
devlnI = log(I/Ibar)*100;                                            % eq. (31) 
devR = (R-Rbar)*100;                                                 % eq. (32)
devPip = (Pip-Piwbar)*100;                                           % eq. (33)
devPiw = (Piw-Piwbar)*100;                                           % eq. (34)
devu = (u-ubar)*100;                                                 % eq. (35)
end;

steady;

check; 

model_diagnostics; 

shocks;
var eg; stderr 0.01;
var ea; stderr 0.01;
var er; stderr 0.01;
var ec; stderr 0.01;
var en; stderr 0.01;
var ei; stderr 0.01;
var enu; stderr 0.01;
end;

%stoch_simul(order=1,irf=40,nodisplay) devlnY devlnC devlnI devR devPip devPiw devu;

%/*
  % ESTIMATION

varobs devlnY devlnC devlnI devR devPip devPiw devu;

estimated_params;
phiphipiw,        gamma_pdf,             1,     0.5;
phic,             beta_pdf,              0.5,   0.2;
phiiy,            gamma_pdf,             1,     0.5;
phiir,            gamma_pdf,             1,     0.5;
phigy,            uniform_pdf,           ,      ,      -4,   4;
phirpi,           uniform_pdf,           ,      ,      -2,   2;
phiry,            uniform_pdf,           ,      ,      -1,   1;
phinul,           uniform_pdf,           ,      ,      -1,   1;
rhog,             beta_pdf,              0.5,   0.2;
rhoa,             beta_pdf,              0.5,   0.2;
rhor,             beta_pdf,              0.5,   0.2;
rhoc,             beta_pdf,              0.5,   0.2;
rhon,             beta_pdf,              0.5,   0.2;
rhoi,             beta_pdf,              0.5,   0.2;
rhonu,            beta_pdf,              0.5,   0.2;
rhopipe,          beta_pdf,              0.5,   0.2;
rhoye,            beta_pdf,              0.5,   0.2;
stderr eg,        inv_gamma_pdf,         0.01,  0.05;
stderr ea,        inv_gamma_pdf,         0.01,  0.05;
stderr er,        inv_gamma_pdf,         0.01,  0.05;
stderr ec,        inv_gamma_pdf,         0.01,  0.05;
stderr en,        inv_gamma_pdf,         0.01,  0.05;
stderr ei,        inv_gamma_pdf,         0.01,  0.05;
stderr enu,       inv_gamma_pdf,         0.01,  0.05;
%dsge_prior_weight,uniform_pdf,           ,      ,      0,    2;
end;

%identification(ar=1);

estimation(datafile=data_ea,first_obs=40,presample=4,mode_compute=6,mh_replic=50000,mh_nblocks=2,mh_jscale=0.5,nodisplay,mode_check,bayesian_irf) devlnY devlnC devlnI devR devPip devPiw devu;
%estimation(datafile=data_ea,first_obs=40,presample=4,mode_compute=6,mh_replic=50000,mh_nblocks=2,mh_jscale=0.5,nodisplay,mode_check,bayesian_irf,dsge_var);

stoch_simul(conditional_variance_decomposition=[1 4]) devlnY devlnC devlnI devR devPip devPiw devu;

shock_decomposition devlnY devlnC devlnI devR devPip devPiw devu;
%*/

