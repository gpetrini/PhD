%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Micro-founded stock-flow consistent model

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tic
% initialization of the variables
clc
clear all;

N = 5000;                        % number of workers 
T = 500;                         % number of time periods
% randn('state',3)
% rand('state',1)

%%% 'micro-level' variables %%%%

c_it = zeros(N,T);              % consumption level of the workers
y_it = zeros(N,T);              % disposable income of the workers
ynet_it = zeros(N,T);           % disposable income of employed workers
s_it = zeros(N,T);              % net savings of the workers
d_it = zeros(N,T);              % debt held by workers
m_it = zeros(N,T); % money
II_t=zeros(1,T);     %  investment function component
auton=zeros(1,T);
V_t=zeros(1,T);
state_it = zeros(N,T);           % the state of worker i at time t (Inactive =0,Active=1)
state_it(1:N,1)=1;            %workers that are unemployed at t=1
state_b_it = zeros(N,T);           % the state of worker i at time t (nonborrowing=0,borrowing=1)
%state_b_it(1:L/2,1)=1;
Un_t=zeros(1,T);                %number of unemployed
Un_t(1,1)=N*0.1;
E_it=zeros(N,T);
tru_it=zeros(N,T);
W_it=zeros(N,T);
rho_it= random('norm',1,0.2,N,T);
W_t=zeros(1,T);
theta_it=zeros(N,T);
%g_it= random('unif',-0.05,0.05,L,T);



EL_t=zeros(1,T);              %employed workers
%i_t=zeros(1,T);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

numOfActiveWorkers_t = zeros(1,T);
numOfNonBorrWorkers_t = zeros(1,T);
numOfBorrowWorkers_t = zeros(1,T);
shareOfNonBorrWorkers_t = zeros(1,T);
shareOfBorrowWorkers_t = zeros(1,T);

unemploymentRatio_t = zeros(1,T);


% firm aggregates
temp=zeros(N,T);                %savings of the workers
h_t = zeros(1,T);               % valuation ratio                       
Pe_t = ones(1,T);               % investment ratio
I_t = zeros(1,T);               % total investment
I_t(1)=100;
S_t = zeros(1,T);               % total savings
K_t = zeros(1,T);                % total capital
Q_t = zeros(1,T);               % demand
Savings=zeros(1,T);             % total amount of savings
Qbar_t = zeros(1,T);            % potential output
r_t = zeros(1,T);               % profit rate
u_t = zeros(1,T);               % capacity utilization
E_t = ones(1,T);                % number of total equity
%W_t = ones(1,T);               % Wealth
A_t = ones(1,T);                % aggregate profits
scw = zeros(1,T);
scp = zeros(1,T);
scd = zeros(1,T);
sw = zeros(1,T);
sp = zeros(1,T);
sd = zeros(1,T);
B_t = zeros(1,T);               % government budget

%household aggregates
   
Ctheta_t = ones(1,T);           % consumption (managers)         
C_t = ones(1,T);                % total consumption
Yw_t = ones(1,T);               % disposable income Y (workers)
Ytheta_t = ones(1,T);           % consumption income Y (managers)    
Y_t = zeros(1,T);                % total income
D_t = zeros(1,T);               % debt workers  
Mtheta_t = zeros(1,T);          % money capitalists
Mtheta_t(1)=1.5;
Mw_t = ones(1,T);              % money workers
Mw_t(1) = 100;
G_t = zeros(1,T);                % capital gain
Stheta_t = ones(1,T);           % total savings managers
Sw_t = ones(1,T);               % total savings workers
Wtheta_t = zeros(1,T);           % total wealth managers
Wtheta_t(1)=1;
wbar = ones(1,T);               % wage of the mean worker
wbar(1)=15;%0.15;
wbarocc = 0.15*ones(1,T);               % wage of the mean occupied worker
wbarocc(1)=wbar(1);
w_it = zeros(N,T);
w_last = zeros(N,1);    %wage at the last employment
minsal_t = zeros(1,T);
minsal_t(1)=25;%0.25;%*wbar(1);%0.015;                       %minimum salary
gmin=-15;
gmax=15;
g_it=random('unif',gmin,gmax,N,T);
wmean = mean(w_it(:,1));
F_t=zeros(1,T);
TT_t = ones(1,T); % step to obtain demand of firms' shared from household
DenQ_t = zeros(1,T);            % step to obtaind aggregate demand
Qd=zeros(1,T);
wb=zeros(1,T);

C=ones(1,T);
D=ones(1,T);
Mw=ones(1,T);
Yw=ones(1,T);
Tax=zeros(1,T);
GiniY=zeros(1,T);
GiniYnet=zeros(1,T);
GiniW=zeros(1,T);
Giniw=zeros(1,T);
hru_it=zeros(N,T);

% financial sector aggregates


Omega_t = ones(1,T);            % net worth of firms
Omegaw_it = zeros(N,T);           % net worth of workers
b_it=zeros(N,T);                     %real unemployment benefit
price_t=ones(1,T);

% some constants
pie=0.035;                       %expected inflation
xi = .1;                         % output-labour ratio  % was 1 in the other code
mu = .8;                       % mark-up of the price
psi = 1.0 / (1.0 + mu);         % equation (9)
pi = mu / (1.0 + mu);           % equation (10)
lambda=0.02;
gamma = .455; %0.5                     %productivity of capital 1.4
alpha = zeros(1,T);                  % multiplicative constant for Pk in the investment function
Beta=6;                     %coefficient for Tobin's q in equation (2)
phi = 0.05;                    % multiplicative constant for debt in the consumption function
ud=0.8;                         % desired capacity utilization
spsi = 0.025;                    % propensity to save out of salary
Theta = 0.8;                    % share of distributed profits
tau_y=0.2;
epsilon=0.9;                   %coefficient from eq (27) and (28)
tau_w=0.02;                    % tax on wealth
eta = .5;                      % multiplicative for difference between median and specific wage in consumption
ibar = 0.035;                     % risk free interest rate
sigma=0.5;
delta = 0.01;  %0.025                % depreciation rate
a=.9;
b=0.08;%0.068;
I0=0; %0.5                         %autonomous investment
i0=0.1;%0.3;%0.06
mm=1;
% initialization 
u_t(1)=0.6;
Q_t(1)=55;
W_it(1:.1*N,1)=75*rand(.1*N,1);%25
W_t(1)=sum(W_it(:,1));
K_t(1)=2200;%2.2;%225
wb(1)=wbar(1);

Pe_t(1)=1.1;
E_t(1)=W_t(1)/Pe_t(1);%10000
E_it(1:.1*N,1)=E_t(1)/(.1*N);
w_it(:,1)= wbar(1)*2*rand(1,N);%0.7*rand(1,L);
m_it(:,1) = .25*rand(N,1);              
y_it(:,1) = 10*rand(N,1);
d_it(0.5*N:N,1) = 40*rand(0.5*N+1,1);
Omegaw_it(:,1)=1*rand(N,1);

mult=1/(b/xi+1-(1-spsi)*(1-tau_y)*(psi+Theta*pi));
price_t(1)=(1+mu)*(wbarocc(1)/xi);
% mult=1/(1-(1-spsi)*(1-tau_y)*(psi+Theta*pi));
%%%% Loop starts %%%%
for t = 2:T-1   
    % update the stage of workers from last period
    %state_it(:,t) = state_it(:,t-1);  % continue the state of workers from the previous state  
    %%%%%%%%% update workers' state %%%%%%%%%
    Active = find(state_it(:,t-1)==1);  
   
    

     
    % update salaries
      minsal_t(t)=minsal_t(t-1)*(1+pie);%(1+1*(price_t(t)-price_t(t-1))/price_t(t-1));%price_t(t))/price_t(t-1); 
  w_it(:,t)=w_last*(1+pie)+g_it(:,t)*minsal_t(t);%*(1+1*(price_t(t)-price_t(t-1))/price_t(t-1)))+g_it(:,t)*minsal_t(t);
%      w_it(:,t)=w_last+g_it(:,t);
%
    below=find(w_it(:,t)<minsal_t(t));
    w_it(below,t)=minsal_t(t);
    clear below
    w_last=w_it(:,t);
    wbar(t) = mean(w_it(:,t-1));
    
II_t(t)=Beta*Pe_t(t-1)*E_t(t-1)/(price_t(t-1)*K_t(t-1));
 I_t(t) = I0+(i0+a*(u_t(t-1)-ud)/ud)*K_t(t-1)+II_t(t);                %firms' investment
%    end
    if I_t(t)<0
       I_t(t)=0;
    end
    
    
    
    %equilibrium in goods market:   
    auton(t)=(I_t(t)+W_t(t-1)*(1-sigma)*(1-tau_w)/price_t(t-1)-phi*D_t(t-1)/price_t(t-1)+N*b);
%     if auton(t)<0
%         auton(t)=I_t(t);
%     end
    Q_t(t)=mult*auton(t);
     
    K_t(t) = (1-delta)*K_t(t-1)+I_t(t);  
    u_t(t)=Q_t(t)/(K_t(t)*gamma);
    if u_t(t)>1
        u_t(t)=1;
        Q_t(t)=K_t(t)*gamma;
        display('Warning: supply constraint')
    end

     %find number of occupied workers
    EL_t(t)=min(N,round(Q_t(t)/xi));
    if Q_t(t)>xi*N
        Q_t(t)=xi*N;
        display('Warning: labor supply constraint')
     
    end
    numocc=EL_t(t);
    %Eindex=randperm(L,numocc);
    temp1=randperm(N);
    Eindex=temp1(1:numocc);
    state_it(Eindex,t)=1;
    numOfActiveWorkers_t(t)=numocc;
    sizeunemployed = N-numocc;
    Un_t(t)=sizeunemployed;
    just_unemployed=find(state_it(:,t)==0);
    w_it(just_unemployed,t)=0;
    b_it(just_unemployed,t)=b;
    unemploymentRatio_t(t) = sizeunemployed/N;
    Active=Eindex;
     wbarocc(t)=mean(w_it(Active,t));
     wb(t)=mean(w_it(:,t));
     price_t(t)=(1+mu)*(wbarocc(t)/xi); % Eq(4)
        clear Eindex numocc temp1

        
        % workers
    y_it(:,t)=(1-tau_y)*(w_it(:,t)+theta_it(:,t-1)*Theta*pi*price_t(t)*Q_t(t)) - ibar*d_it(:,t-1)+b_it(:,t)*price_t(t);
    ynet_it(Active,t)=y_it(Active,t);
    c_it(:,t) = (1-spsi)*(1-tau_y)*(w_it(:,t)+theta_it(:,t-1)*Theta*pi*price_t(t)*Q_t(t)) + eta*(wb(t) - w_it(:,t)) + (1-sigma)*(1-tau_w)*W_it(:,t-1)+b_it(:,t)*price_t(t)- phi*d_it(:,t-1);
    indn=find(c_it(:,t)<0);
    c_it(indn,t)=0;
clear indn
      Tax(t)=tau_y*(psi+Theta*pi)*price_t(t)*Q_t(t)+tau_w*W_t(t-1);
      B_t(t)=B_t(t-1)+Tax(t)-sum(b_it(:,t))*price_t(t);
    C_t(t) = sum(c_it(:,t));
    
    %%%%%%%%%% update workers' state %%%%%%%%%(updated in version 6_2)
    temp(:,t) = y_it(:,t)-c_it(:,t);
    Savings(t)=sum(temp(:,t));
    index1=find(temp(:,t)<0);
    state_b_it((index1),t) = 1;                          
    Borrow = (index1);
        clear index1
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       

%  Mw_t(t) = sum(m_it(:,t));
 A_t(t) = (1-Theta)*(pi*price_t(t)*Q_t(t));
 Pe_t(t) =(1/E_t(t-1))*(W_t(t-1)*(1-tau_w)/(1+exp(-lambda*V_t(t-1)))-I_t(t)*price_t(t) + A_t(t));
 if Pe_t(t)<=0
     Pe_t(t)=1;%Pe_t(t-1);
 end


 
 E_t(t) = E_t(t-1) + (I_t(t)*price_t(t) - A_t(t))./ Pe_t(t);
 if E_t(t)<=0
     E_t(t)=E_t(t-1);
 end
 
    
    
  
     
     
             tru_it(:,t)=mm*W_it(:,t-1)*(1-tau_w)+(Pe_t(t)-Pe_t(t-1))*E_it(:,t-1)+temp(:,t)-d_it(:,t-1);
    jk=find(tru_it(:,t)>0);
    W_it(jk,t)=W_it(jk,t-1)*(1-tau_w)+(Pe_t(t)-Pe_t(t-1))*E_it(jk,t-1)+temp(jk,t)-d_it(jk,t-1);
     jm=find(tru_it(:,t)<=0);
     W_it(jm,t)=W_it(jm,t-1)*(1-tau_w)*(1-mm);
    
    
    hru_it(:,t)=d_it(:,t-1)-mm*W_it(:,t-1)*(1-tau_w)-(Pe_t(t)-Pe_t(t-1))*E_it(:,t-1)-temp(:,t);
     jl=find(hru_it(:,t)>0);
     d_it(jl,t)=d_it(jl,t-1)-mm*W_it(jl,t-1)*(1-tau_w)-(Pe_t(t)-Pe_t(t-1))*E_it(jl,t-1)-temp(jl,t);
     
        W_t(t)=sum(W_it(:,t));
 V_t(t)=(Theta*pi*price_t(t)*Q_t(t))/(Pe_t(t)*E_t(t));
 theta_it(:,t)=W_it(:,t)/W_t(t);
 E_it(:,t)=theta_it(:,t)*E_t(t);
 
     m_it(:,t)=W_it(:,t)-Pe_t(t)*E_it(:,t);   
    
     
     
    
    
    D_t(t) = sum(d_it(:,t));
    Y_t(t) = sum(y_it(:,t));
%          
 
    
    
   
    %%% update the number of firms    
    %numOfActiveWorkers_t(t) = size(find(state_it(:,t)==1|state_it(:,t)==2),1);
    numOfNonBorrWorkers_t(t) = size(find(state_b_it(:,t)==0),1);
    numOfBorrowWorkers_t(t) = size(find(state_b_it(:,t)==1),1); 
    shareOfNonBorrWorkers_t(t) = numOfNonBorrWorkers_t(t)/N;
    shareOfBorrowWorkers_t(t) = 1 - shareOfNonBorrWorkers_t(t);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    minna=min(y_it(:,t));
yp=y_it(:,t)+abs(minna);    
GiniY(t)=ginicoeff(yp);
clear yp
 minna=min(ynet_it(:,t));
yp=ynet_it(:,t)+abs(minna);    
GiniYnet(t)=ginicoeff(yp);   

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    GiniW(t)=ginicoeff(W_it(:,t));
   % end
    Giniw(t)=ginicoeff(w_it(:,t));
    
    rhow=corrcoef(y_it(Active,t),w_it(Active,t));
    rhow=rhow(1,2);
    stdevw=std(w_it(Active,t));
    stdevy=std(y_it(Active,t));
    m2y=(mean(y_it(Active,t)))^2;
    sw(t)=rhow*stdevw/stdevy;
    scw(t)=(rhow*stdevw*stdevy)/m2y;
    rhop=corrcoef(y_it(Active,t),theta_it(Active,t-1)*Theta*pi*price_t(t)*Q_t(t));
    rhop=rhop(1,2);
    stdevp=std(theta_it(Active,t-1)*Theta*pi*price_t(t)*Q_t(t));
    scp(t)=(rhop*stdevp*stdevy)/m2y;
    sp(t)=rhop*stdevp/stdevy;
    
    
    if isempty(d_it(:,t-1))==0
    rhod=corrcoef(y_it(:,t),-ibar*d_it(:,t-1));
    rhod=rhod(1,2);
    stdevd=std(-ibar*d_it(:,t-1));
    scd(t)=(rhod*stdevd*stdevy)/m2y;
    sd(t)=rhod*stdevd/stdevy;
    else
    scd(t)=0;
    sd(t)=0;
    end
   
end

 
    save SFineq_CDG7_4.mat

%%% Plot data %%%

initialT=250;
endT=T-1;
pip=diff(price_t);
inflation=pip./price_t(1:T-1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure
   
subplot(2,2,1);

plot(initialT:endT,Q_t(initialT:endT),'k');
xlabel('Time')
ylabel('Agg. demand')
%}
subplot(2,2,2);
plot(initialT:endT, unemploymentRatio_t(initialT:endT),'k');  
xlabel('Time')
ylabel('unemployment ratio')
%ylim([-0.1, 1.1]);
ha = axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0 
1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
text(0.5, 1,'\bf ABM simulation','HorizontalAlignment','center','VerticalAlignment', 'top')

subplot(2,2,3);
plot(initialT:endT,GiniY(initialT:endT),'r',initialT:endT,GiniW(initialT:endT),'k',initialT:endT,Giniw(initialT:endT),'b',initialT:endT,GiniYnet(initialT:endT),'g');
xlabel('Time')
ylabel('Gini coeff.')
legend('Y','W','w','Y emp.')
ylim([0, 1.001]);

subplot(2,2,4);
plot(initialT:endT,D_t(initialT:endT)./price_t(initialT:endT),'r',initialT:endT,W_t(initialT:endT)./price_t(initialT:endT),'k',initialT:endT,B_t(initialT:endT)./price_t(initialT:endT),'g');
xlabel('Time')
%ylabel('Real debt')
legend('D','W','B')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure
subplot(2,1,1);
plot(initialT:endT,sp(initialT:endT),'r',initialT:endT,sw(initialT:endT),'k',initialT:endT,sd(initialT:endT),'b');
xlabel('Time')
ylabel('Absolute effect')
legend('Profits','Wages','Debt')
%ylim([0, 1.1]);


subplot(2,1,2);
plot(initialT:endT,scp(initialT:endT),'r',initialT:endT,scw(initialT:endT),'k',initialT:endT,scd(initialT:endT),'b');
xlabel('Time')
ylabel('Relative effect')
legend('Profits','Wages','Debt')
%ylim([0, 1.1]);

