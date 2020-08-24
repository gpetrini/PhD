function [ys,check] = model_pk_steadystate(ys,exe)
global M_ lgy_

%% DO NOT CHANGE THIS PART.
%%
%% Here we load the values of the deep parameters in a loop.
%%
if isfield(M_,'param_nbr') == 1
    NumberOfParameters = M_.param_nbr;                            % Number of deep parameters.
for i = 1:NumberOfParameters                                  % Loop...
  paramname = deblank(M_.param_names(i,:));                   %    Get the name of parameter i. 
  eval([ paramname ' = M_.params(' int2str(i) ');']);         %    Get the value of parameter i.
end                                                           % End of the loop.  
check = 0;
end
%%
%% END OF THE FIRST MODEL INDEPENDENT BLOCK.


%% THIS BLOCK IS MODEL SPECIFIC.
%%
%% Here the user has to define the steady state.
%%

Vcbar = (Ybar - Cwbar - Ibar - Gbar) / (((1-tz)*(Ybar-1/(1+epsilon)*(1-alfa)*(pssi)^(-alfa/(1-alfa))*Lbar-(1-xi)*Ibar))^phic*(Brbar)^(1-phic));

nu_ss=nubar;
Nw_ss=Nwbar;
R_ss=Rbar;
G_ss=Gbar;
T_ss=G_ss+(Rbar/Piwbar*1/Gama-1)*Dgbar;
Piw_ss=Piwbar;
Pip_ss=Piwbar;
u_ss=ubar;
Y_ss=Ybar;
K_ss=Y_ss/pssi;
I_ss=Ibar;
varphi_ss=1/(1+epsilon);
wp_ss=varphi_ss*(1-alfa)*pssi^(-alfa/(1-alfa));
L_ss=Lbar;   
Cw_ss=Cwbar;
Zr_ss=Y_ss - wp_ss*Lbar - (1-xi)*I_ss;  
Cr_ss=Crbar;
Br_ss=Brbar;

wp=wp_ss;
Y=Y_ss;
K=K_ss;
I=I_ss;
Br=Br_ss;
Cr=Cr_ss;
Cw=Cw_ss;
Zr=Zr_ss;
Nw=Nw_ss;
L=L_ss;
u=u_ss;
varphi=varphi_ss;
Pip=Pip_ss;
Piw=Piw_ss;
G=G_ss;
T=T_ss;
R=R_ss;
nu=nu_ss;
Piwe=Pip_ss;
Ye=Y_ss;
Dg=Dgbar;

Va=1;
Vc=Vcbar;
Vn=1;
Vi=1;
Vg=1;
Vr=1;
Vnu=1;

devlnY=0; 
devlnC=0; 
devlnI=0; 
devR=0;
devPip=0;
devPiw=0;
devu=0;

%mpcz = phic*Cr_ss/Zr_ss 
%mpcb = (1-phic)*Cr_ss/Br_ss
%bz=Br_ss/Zr_ss
%mpiy = phiiy*I_ss/Y_ss


%%
%% END OF THE MODEL SPECIFIC BLOCK.


%% DO NOT CHANGE THIS PART.
%%
%% Here we define the steady state values of the endogenous variables of
%% the model.
%%

for iter = 1:length(M_.params)
  eval([ 'M_.params(' num2str(iter) ') = ' M_.param_names(iter,:) ';' ])
end

if isfield(M_,'param_nbr') == 1

if isfield(M_,'orig_endo_nbr') == 1
NumberOfEndogenousVariables = M_.orig_endo_nbr;
else
NumberOfEndogenousVariables = M_.endo_nbr;                   % Number of endogenous variables.
end
ys = zeros(NumberOfEndogenousVariables,1);                   % InitIization of ys (steady state).
for i = 1:NumberOfEndogenousVariables                        % Loop...
  varname = deblank(M_.endo_names(i,:));                     % Get the name of endogenous variable i
  eval(['ys(' int2str(i) ') = ' varname ';']);               % Get the steady state value of this variable.
end                                                          % End of the loop.
else
ys=zeros(length(lgy_),1);
for i = 1:length(lgy_)
    ys(i) = eval(lgy_(i,:));
end
check = 0;
end
end

%%
%% END OF THE SECOND MODEL INDEPENDENT BLOCK.
