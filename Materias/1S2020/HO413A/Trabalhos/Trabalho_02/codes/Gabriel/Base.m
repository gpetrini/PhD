%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Micro-founded stock-flow consistent model

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

T = 500;                         % number of time periods
%%% 'micro-level' variables %%%%
h_t = zeros(1,T);               % valuation ratio                       % AUSENTE
Qbar_t = zeros(1,T);            % potential output AUSENTE
r_t = zeros(1,T);               % profit rate % AUSENTE
Ctheta_t = ones(1,T);           % consumption (managers)     AUSENTE    
Yw_t = ones(1,T);               % disposable income Y (workers) AUSENTE
Ytheta_t = ones(1,T);           % consumption income Y (managers) AUSENTE      
Mtheta_t = zeros(1,T);          % money capitalists
Mtheta_t(1)=1.5; % AUSENTE
Mw_t = ones(1,T);              % money workers % AUSENTE
Mw_t(1) = 100; % AUSENTE
G_t = zeros(1,T);                % capital gain % AUSENTE
Stheta_t = ones(1,T);           % total savings managers % AUSENTE
Sw_t = ones(1,T);               % total savings workers % AUSENTE
Wtheta_t = zeros(1,T);           % total wealth managers % AUSENTE
Wtheta_t(1)=1; %% Ausente
DenQ_t = zeros(1,T);            % step to obtaind aggregate demand AUSENTE
Qd=zeros(1,T); %% AUSENTE
Omega_t = ones(1,T);            % net worth of firms % AUSENTE
Omegaw_it = zeros(N,T);           % net worth of workers % AUSENTE
alpha = zeros(1,T);                  % multiplicative constant for Pk in the investment function AUSENTE
epsilon=0.9;                   %coefficient from eq (27) and (28)
% initialization % AUSENTE
rho_it= normrnd(1,0.2,[N,T]); %% AUSENTE
Omegaw_it(:,1)=1*rand(N,1); %% AUSENTE


W_it(1:.1*N,1)=75*rand(.1*N,1);%25 %%% REVER

E_it=zeros(N,T);
W_it=zeros(N,T);

E_t(1)=W_t(1)/Pe_t(1);%10000
E_it(1:.1*N,1)=E_t(1)/(.1*N);


initialT=250;
endT=T-1;
